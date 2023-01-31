from mevis import *
import os, string, subprocess, winreg

outputFilename = "T1.nii"

class MatlabNotFoundError(Exception):
  pass

def getMatlabPath():
  # The location of matlab.exe is stored in:
  # HKEY_LOCAL_MACHINE\SOFTWARE\MathWorks\MATLAB\[version]

  # Open the MATLAB registry
  registry = winreg.ConnectRegistry(None, winreg.HKEY_LOCAL_MACHINE)
  matlabKey = winreg.OpenKey(registry, "SOFTWARE\MathWorks\MATLAB")
  
  # Find the latest Matlab version
  matlabVersion = str(0)        
  for i in range(1000):
    try:
      currentMatlabVersion = winreg.EnumKey(matlabKey, i)
      if currentMatlabVersion > matlabVersion:
        matlabVersion = currentMatlabVersion
    except WindowsError:
      # Since you cannot determine the number of keys, you must
      # loop until error
      break
  
  if matlabVersion == str(0):
    raise MatlabNotFoundError
  
  # Registry key of latest Matlab version
  currentMatlabKey = winreg.OpenKey(matlabKey, currentMatlabVersion)
  
  # Find the tag MATLABROOT
  matlabRoot = ""
  for i in range(1000):
    try:
      value = winreg.EnumValue(currentMatlabKey, i)                
      # value = ('MATLABROOT', path, datatype (=string))

      if value[0] == "MATLABROOT":
        matlabRoot = value[1]        
    except WindowsError:
      break
      
      
  matlabPath = os.path.join(matlabRoot, 'bin', 'matlab.exe')
  
  if not os.path.exists(matlabPath):
    raise MatlabNotFoundError
      
  return MLABFileManager.normalizePath( matlabPath )

def do():
  global outputFilename
  outputDir = MLABFileManager.normalizePath( ctx.field("outputDir").stringValue() )
  
  if not MLABFileManager.isDir(outputDir):
    MLAB.logError("Output dir not valid")
    return
  
  matlabPath = ""
  try:
    matlabPath = getMatlabPath()
  except MatlabNotFoundError:
    MLAB.logError("Matlab not found")
    return
    
  spmPath = MLABFileManager.normalizePath( os.path.join(ctx.networkPath(), 'spm12b_6080') )
  
  # Save T1 image as nifti
  ctx.field("T1Save.fileName").setStringValue(os.path.join(outputDir, outputFilename))
  ctx.field("T1Save.save").touch()
  
  
  args = []
  args.append(matlabPath)
  args.extend(['-nodesktop', '-nosplash', '-wait']) # , '-singleCompThread'
    
  spmCommands = []
  spmCommands.append("spmPath='"+spmPath+"'")
  spmCommands.append("addpath(spmPath)")
  spmCommands.append("subjectDir='"+outputDir+"'")
  spmCommands.append("run('"+ MLABFileManager.normalizePath( os.path.join(ctx.networkPath(), "SPM.m") ) +"')")
  
  args.extend(['-r', ';'.join(spmCommands)+';'])
  
  MLAB.log("SPM started with arguments: " + str(args) )
  subprocess.call(args) 
  
  getOutput()
  
  
def getOutput():
  global outputFilename
  outputDir = MLABFileManager.normalizePath( ctx.field("outputDir").stringValue() )
  
  for i in ['c1', 'c2', 'c3', 'c4', 'c5', 'c6']:
    cFilename = MLABFileManager.normalizePath( os.path.join(outputDir, i+outputFilename) )
    
    ctx.module(i).field("fileName").setStringValue(cFilename)
  
  