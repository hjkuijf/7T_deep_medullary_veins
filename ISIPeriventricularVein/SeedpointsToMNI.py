from mevis import *
import os
import fileinput

def updateInitialTransform(transformFile):
  newPath = os.path.split(ctx.field("inputMNI_to_T1").stringValue())[0]
  
  for line in fileinput.input(transformFile, inplace=True):
    if "InitialTransformParametersFileName" in line:
      oldPath = line.split('"')[1]
      basename = os.path.basename(oldPath)
      
      print('(InitialTransformParametersFileName "'+ os.path.join(newPath, basename).replace("\\", "/") +'")')
    else:
      print(line.strip())



def doTransforms(tempDir):
  # elastix may have run on a different PC. Update paths
  updateInitialTransform(ctx.field("inputMNI_to_T1").stringValue())
  
  # First transform the point from the E2 back to the T1.
  ctx.field("Transformix.workingDirectory").setStringValue(tempDir)
  ctx.field("Transformix.transformationFile").setStringValue(ctx.field("inputT1_to_E2").stringValue())
  ctx.field("Transformix.update").touch()
  
  # Then, transform the points from T1 to MNI
  ctx.field("Transformix1.workingDirectory").setStringValue(tempDir)
  ctx.field("Transformix1.transformationFile").setStringValue(ctx.field("inputMNI_to_T1").stringValue())
  ctx.field("Transformix1.update").touch()

def do():
  outputDir = MLABFileManager.normalizePath( ctx.field("outputDir").stringValue() )
  mni, definite, roi, points, wml = getOutputFilename()
  
  tempDir = MLABFileManager.normalizePath( os.path.join(outputDir, "temp") )
  MLABFileManager.mkdir(tempDir)
  
  ctx.field("Transformix.inputXMarkerList").connectFrom(ctx.field("BaseBypass.baseOut0"))
  doTransforms(tempDir)
  
  ctx.field("SaveBase.filename").setStringValue(mni)
  ctx.field("SaveBase.save").touch()
    
  
  
  # TRY TO TRANSFORM DEFINITE
  definiteFilename = os.path.normpath(os.path.join(outputDir, "..", "Seedpoints", "final.definite.xml"))
  if MLABFileManager.exists(definiteFilename):
    ctx.field("Definite.filename").setStringValue(definiteFilename)
    
    ctx.field("Transformix.inputXMarkerList").connectFrom(ctx.field("Definite.outObject"))    
    
    doTransforms(tempDir)
    
    ctx.field("SaveBase2.filename").setStringValue(definite)
    ctx.field("SaveBase2.save").touch()
    
    ctx.field("XMarkerListRadiusSearch.inRadius").setDoubleValue(15)
    ctx.field("XMarkerListRadiusSearch.update").touch()
    
    ctx.field("SaveBase1.filename").setStringValue(roi)
    ctx.field("SaveBase1.save").touch()
    
  # TRANSFORM VESSEL POINTS    
  ctx.field("Transformix.inputXMarkerList").connectFrom(ctx.field("VesselPoints.baseOut0")) 
  doTransforms(tempDir)  
  ctx.field("SaveBase3.filename").setStringValue(points)
  ctx.field("SaveBase3.save").touch()
  
  # TRY TO TRANSFORM WML
  wmlFilename = os.path.normpath(os.path.join(outputDir, "..", "WMH_reg.mlimage"))
  if MLABFileManager.exists(wmlFilename):
    ctx.field("WML.fileName").setStringValue(wmlFilename)
    ctx.field("MaskToMarkers.update").touch()
    ctx.field("Transformix.inputXMarkerList").connectFrom(ctx.field("MaskToMarkers.outputXMarkerList")) 
    doTransforms(tempDir)  
    ctx.field("MarkerToMask.update").touch()
    ctx.field("MLImageFormatSave.fileName").setStringValue(wml)
    ctx.field("MLImageFormatSave.save").touch()
    
    
  getOutput()  
  
  # Clean
  MLABFileManager.recursiveRemoveDir(tempDir)

def getOutputFilename():
  outputDir = MLABFileManager.normalizePath( ctx.field("outputDir").stringValue() )
  
  return os.path.join(outputDir, "final.mni.xml"), os.path.join(outputDir, "final.definite.mni.xml"), os.path.join(outputDir, "final.definite.roi.mni.xml"), os.path.join(outputDir, "vessel.points.mni.xml"), os.path.join(outputDir, "wmh.mni.mlimage")

def getOutput():  
  mni, definite, roi, points, wml = getOutputFilename()
  
  ctx.field("LoadBase.filename").setStringValue(mni)
  ctx.field("LoadBase.load").touch()
  
  ctx.field("LoadBase1.filename").setStringValue(definite)
  ctx.field("LoadBase1.load").touch()
  
  ctx.field("LoadBase2.filename").setStringValue(roi)
  ctx.field("LoadBase2.load").touch()
  
  ctx.field("LoadBase3.filename").setStringValue(points)
  ctx.field("LoadBase3.load").touch()
  
  ctx.field("MLImageFormatLoad.fileName").setStringValue(wml)
  