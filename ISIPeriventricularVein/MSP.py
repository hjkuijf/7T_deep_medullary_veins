from mevis import *
import os

def do():  
  ctx.field("MidsagittalPlane.update").touch()
  
  with open(getOutputFilename(), "w") as planeFile:
    planeFile.write(ctx.field("MidsagittalPlane.outPlane").stringValue())

  getOutput()

def getOutputFilename():
  
  return MLABFileManager.normalizePath( os.path.join(ctx.field("outputDir").stringValue(), "MSP.plane") )


def getOutput():
  with open(getOutputFilename(), "r") as planeFile:
    ctx.field("outputPlane").setStringValue(planeFile.readline())
    