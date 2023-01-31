#----------------------------------------------------------------------------------
#! Macro module PeriventricularVeinDetection
#/*!
# \file    PeriventricularVeinDetection.py
# \author  Hugo
# \date    2014-08-07
#
# 
# */
#----------------------------------------------------------------------------------

from mevis import *
import os


def do():
  subjectDir = MLABFileManager.normalizePath( ctx.field("subjectDir").stringValue() )
  
  print('start')
  
  if not MLABFileManager.isDir(subjectDir):
    MLAB.logError("Output dir not valid")
    return
  
  # Load the images
  T1Filename = MLABFileManager.normalizePath( os.path.join(subjectDir, ctx.field("t1Filename").stringValue() ) )
  if not MLABFileManager.exists(T1Filename):
    MLAB.logError("T1 not found")
    return
  ctx.field("T1.fileName").setStringValue(T1Filename)
  
  E2Filename = MLABFileManager.normalizePath( os.path.join(subjectDir, ctx.field("e2Filename").stringValue() ) )
  if not MLABFileManager.exists(E2Filename):
    MLAB.logError("E2 not found")
    return
  ctx.field("E2.fileName").setStringValue(E2Filename)
  
  
  
  doThing("SPM", subjectDir)
  
  doThing("MNI", subjectDir)
  
  doThing("VSurface", subjectDir)
  
  doThing("MSP", subjectDir)
  
  doThing("LowerROI", subjectDir)
  
  doThing("Seedpoints", subjectDir)
  
  doThing("Tracking", subjectDir)
  
  doThing("SeedpointsToMNI", subjectDir)
  
  
  
  
  print('eind')
  


def doThing(what, subjectDir):
  whatOutputDir = MLABFileManager.normalizePath( os.path.join(subjectDir, what) )
  MLABFileManager.mkdir(whatOutputDir)
  ctx.module(what).field("outputDir").setStringValue(whatOutputDir)
  if ctx.field("do"+ what).boolValue():
    ctx.module(what).field("update").touch()
  else:
    # When skipping computation, still update the output from a previous run
    ctx.module(what).field("getOutput").touch()
  

def subjectDirChanged():
  subjectDir = ctx.field("subjectDir").stringValue()
  
  subjectDirContents = MLABFileManager.contentOfDirectory(subjectDir, "*.mlimage")
  for item in subjectDirContents:
    if "T1" in item:
      ctx.field("t1Filename").setStringValue(item)
    if "E2" in item:
      ctx.field("e2Filename").setStringValue(item)
      
def init():
  subjectDir = ctx.field("subjectDir").stringValue()
  if len(subjectDir) > 0:
    subjectDirChanged()