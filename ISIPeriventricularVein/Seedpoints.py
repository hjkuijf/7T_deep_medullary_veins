from mevis import *
import os


def init():
  ctx.field("E2.noBypass").setBoolValue(True)
  ctx.field("V.noBypass").setBoolValue(True)
  ctx.field("VSurface.noBypass").setBoolValue(True)



def do():
  # Load the images
  ctx.field("E2.noBypass").setBoolValue(False)
  ctx.field("V.noBypass").setBoolValue(False)
  ctx.field("VSurface.noBypass").setBoolValue(False)
  
  
  # First, set the clipping planes
  inputMSP = ctx.field("inputMSP").vectorValue()
  inputLowerROI = ctx.field("inputLowerROI").vectorValue()
  
  leftPlane = list(inputMSP)
  leftPlane[3] -= 7.5
  
  rightPlane = list(inputMSP)
  rightPlane[3] += 7.5
  
  ctx.field("ClipLeft.plane").setVectorValue(leftPlane)
  ctx.field("ClipRight.plane").setVectorValue(rightPlane)
  ctx.field("ClipBottom.plane").setVectorValue(inputLowerROI)
  
  
  # Now, update EuclidianDTF. Do this after the planes, so the auto-computes goes well :-)
  ctx.field("EuclideanDTF.update").touch()
  
  # Pull all computations through the network by updating MaskToMarkers
  ctx.field("MaskToMarkers.update").touch()
  
  
  # Now for the fancy stuff: filtering with TubularTracking
  numMarkers = ctx.field("XMarkerAtIndex.numMarkers").intValue()
  
  results = []  
  ctx.field("Definite.deleteAll").touch()  
  
  for i in range(numMarkers):
    ctx.field("XMarkerAtIndex.index").setIntValue(i)
    
    ctx.field("TubularTracking.update").touch()
    
    ctx.field("MarkerToMask.update").touch()
    
    neighbourValue = ctx.field("MinMaxScan.trueMaxValue").doubleValue()
    
    data = []
    data.append(ctx.field("WorldVoxelConvert2.voxelX").intValue())
    data.append(ctx.field("WorldVoxelConvert2.voxelY").intValue())
    data.append(ctx.field("WorldVoxelConvert2.voxelZ").intValue())
    data.append(neighbourValue)
    
    results.append(map(str, data))
    
    if neighbourValue > 0.04:
      ctx.field("Definite.insert").touch()
  
  ctx.field("SaveBase.filename").setStringValue( getOutputFilename() )
  ctx.field("SaveBase.save").touch()
  
  getOutput()


def getOutputFilename():
  outputDir = MLABFileManager.normalizePath( ctx.field("outputDir").stringValue() )
  
  
  
  return MLABFileManager.normalizePath( os.path.join(outputDir, "final.xml") )



def getOutput():  
  
  ctx.field("LoadBase.filename").setStringValue( getOutputFilename() )
  ctx.field("LoadBase.load").touch()
  pass