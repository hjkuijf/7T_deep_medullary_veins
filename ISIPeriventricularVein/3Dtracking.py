from mevis import *
import os

def do():  
  outputDir = MLABFileManager.normalizePath( ctx.field("outputDir").stringValue() )
  
  # Load definite seedpoints
  definiteFilename = os.path.join(ctx.field("seedpointDir").stringValue(), "final.definite.xml")
  if not MLABFileManager.exists(definiteFilename):
    MLAB.logError("Definite markers for "+ outputDir +" do not exist!!!")
    return
  ctx.field("Definite.filename").setStringValue(definiteFilename)
  
  ctx.field("TubularTracking.update").touch()
  
  graphFilename, pointsFilename = getOutputFilename()
  ctx.field("VesselGraph.filename").setStringValue(graphFilename)
  ctx.field("VesselPoints.filename").setStringValue(pointsFilename)
  ctx.field("VesselGraph.save").touch()
  ctx.field("VesselPoints.save").touch()

  getOutput()

def getOutputFilename():
  graphFilename  = os.path.join(ctx.field("outputDir").stringValue(), "graph.xml")
  pointsFilename = os.path.join(ctx.field("outputDir").stringValue(), "points.xml")
  
  return graphFilename, pointsFilename


def getOutput():
  graphFilename, pointsFilename = getOutputFilename()
  
  ctx.field("LoadVesselGraph.filename").setStringValue(graphFilename)
  ctx.field("LoadVesselPoints.filename").setStringValue(pointsFilename)
    