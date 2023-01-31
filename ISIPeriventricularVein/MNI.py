from mevis import *
import os

def do():
  outputDir = MLABFileManager.normalizePath( ctx.field("outputDir").stringValue() )
  
  tempDir = MLABFileManager.normalizePath( os.path.join(outputDir, "temp") )
  MLABFileManager.mkdir(tempDir)
  
  vFilename, roiFilename, t1AtSWIFilename = getOutputFilename()
  
  # Register the T1 to the E2 (affine)
  T1_to_E2_Dir = MLABFileManager.normalizePath( os.path.join(tempDir, "t12e2") )
  MLABFileManager.mkdir(T1_to_E2_Dir)
  ctx.field("T1_to_E2.temporaryDirectory").setStringValue(T1_to_E2_Dir)  
  ctx.field("T1_to_E2.update").touch()
  ctx.field("T1_to_E2.resultingTransformationFileCopy").setStringValue( os.path.join(outputDir, "T1_to_E2.txt") )
  ctx.field("T1_to_E2.saveResultingTransformationFileCopy").touch()  
  ctx.field("T1_at_SWI_Save.fileName").setStringValue(t1AtSWIFilename)
  ctx.field("T1_at_SWI_Save.save").touch()
  
  # Register the MNI to the T1 (affine + bspline)
  MNI_to_T1_Dir = MLABFileManager.normalizePath( os.path.join(tempDir, "mni2t1") )
  MLABFileManager.mkdir(MNI_to_T1_Dir)
  ctx.field("MNI_to_T1.temporaryDirectory").setStringValue(MNI_to_T1_Dir)  
  ctx.field("MNI_to_T1.update").touch()
  ctx.field("MNI_to_T1.resultingTransformationFileCopy").setStringValue( os.path.join(outputDir, "MNI_to_T1.txt") )
  ctx.field("MNI_to_T1.saveResultingTransformationFileCopy").touch()
  
  
  # Transform the MNI-CSF atlas to the T1.
  ctx.field("Transformix.workingDirectory").setStringValue(MNI_to_T1_Dir)
  ctx.field("Transformix.update").touch()
  
  # Transform the Ventricle mask from the T1 to the E2
  ctx.field("Transformix1.workingDirectory").setStringValue(T1_to_E2_Dir)
  ctx.field("Transformix1.update").touch()  
  
  
  # Save them shizzle !  
  ctx.field("MLImageFormatSave.fileName").setStringValue( vFilename )
  ctx.field("MLImageFormatSave.save").touch()
  
  
  
  # Transform the lower ROI points from MNI to T1
  ctx.field("Transformix2.workingDirectory").setStringValue(MNI_to_T1_Dir)
  ctx.field("Transformix2.update").touch()
  ctx.field("Transformix3.workingDirectory").setStringValue(MNI_to_T1_Dir)
  ctx.field("Transformix3.update").touch()
  ctx.field("LowerROIPointsSave.fileName").setStringValue( roiFilename )
  ctx.field("LowerROIPointsSave.save").touch()
  
  
  
  getOutput()
  
  # Clean
  MLABFileManager.recursiveRemoveDir(tempDir)
  


def getOutputFilename():
  outputDir = MLABFileManager.normalizePath( ctx.field("outputDir").stringValue() )

  return MLABFileManager.normalizePath( os.path.join(outputDir, "V.mlimage")), MLABFileManager.normalizePath( os.path.join(outputDir, "LowerROIPoints.mlimage")), MLABFileManager.normalizePath( os.path.join(outputDir, "T1_at_SWI.mlimage"))

def getOutput():  
  vFilename, roiFilename, t1AtSWIFilename = getOutputFilename()
  ctx.field("V.fileName").setStringValue(vFilename)
  ctx.field("LowerROIPointsImage.fileName").setStringValue(roiFilename)
  ctx.field("T1_at_SWI.fileName").setStringValue(t1AtSWIFilename)
  
  
  outputDir = MLABFileManager.normalizePath( ctx.field("outputDir").stringValue() )
  ctx.field("outputMNI_to_T1").setStringValue(os.path.join(outputDir, "MNI_to_T1.txt"))
  ctx.field("outputT1_to_E2").setStringValue(os.path.join(outputDir, "T1_to_E2.txt"))
  