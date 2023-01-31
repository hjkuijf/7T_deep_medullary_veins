from mevis import *
import os

def getPoint(point):
  
  #boundingBoxWorld = map(float, ctx.module(point).field("boundingBoxWorld").stringValue().split())
  boundingBoxWorld = [float(x) for x in ctx.module(point).field("boundingBoxWorld").stringValue().split()]
  
  x = (boundingBoxWorld[0] + boundingBoxWorld[6] ) / 2.0
  y = (boundingBoxWorld[1] + boundingBoxWorld[7] ) / 2.0
  z = (boundingBoxWorld[2] + boundingBoxWorld[8] ) / 2.0
  
  return (x, y, z)


def do():
  
  msp = ctx.field("inputMSP").vectorValue()
  
  point1 = getPoint("Point1")
  point2 = getPoint("Point2")
  
  point3 = [sum(x) for x in zip(point1, msp[:3])] # Add the normal of MSP to point1 to create a third point on the plane
  
  ctx.field("ComposePlaneFromPoints.inPoint1").setVectorValue(point1)
  ctx.field("ComposePlaneFromPoints.inPoint2").setVectorValue(point2)
  ctx.field("ComposePlaneFromPoints.inPoint3").setVectorValue(point3)
  
  
  with open(getOutputFilename(), "w") as planeFile:
    planeFile.write(ctx.field("ComposePlaneFromPoints.outPlane").stringValue())

  getOutput()


def getOutputFilename():  
  return MLABFileManager.normalizePath( os.path.join(ctx.field("outputDir").stringValue(), "LowerROI.plane") )


def getOutput():
  with open(getOutputFilename(), "r") as planeFile:
    ctx.field("outputPlane").setStringValue(planeFile.readline())