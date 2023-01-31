from mevis import *
import os

def do():
  outputDir = MLABFileManager.normalizePath( ctx.field("outputDir").stringValue() )
    
  ctx.field("EuclideanDTF.update").touch()
  
  maskFilename, surfFilename = getOutputFilename()
  ctx.field("VMaskSave.fileName").setStringValue(maskFilename)
  ctx.field("VMaskSave.save").touch()
  
  ctx.field("VSurfaceSave.fileName").setStringValue(surfFilename)
  ctx.field("VSurfaceSave.save").touch()
  
  getOutput()


def getOutputFilename():
  outputDir = MLABFileManager.normalizePath( ctx.field("outputDir").stringValue() )
  
  maskFilename = MLABFileManager.normalizePath(os.path.join(outputDir, "VMask.mlimage"))
  surfFilename = MLABFileManager.normalizePath(os.path.join(outputDir, "VSurface.mlimage"))
  
  return maskFilename, surfFilename



def getOutput():  
  maskFilename, surfFilename = getOutputFilename()
  
  ctx.field("VMask.fileName").setStringValue(maskFilename)
  ctx.field("VSurface.fileName").setStringValue(surfFilename)