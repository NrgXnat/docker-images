import gdcm
import sys
import shutil

def decompress(inFile, outFile):
  print("Extract (or copy) %s to %s" % (inFile, outFile))
  try:
    reader = gdcm.ImageReader()
    reader.SetFileName( inFile )
    if not reader.Read():
      raise Exception("Unable to read %s with gdcm.ImageReader()" % inFile)

    change = gdcm.ImageChangeTransferSyntax()
    change.SetTransferSyntax( gdcm.TransferSyntax(gdcm.TransferSyntax.ImplicitVRLittleEndian) )
    change.SetInput( reader.GetImage() )
    if not change.Change():
      raise Exception("Unable to change %s with gdcm.ImageChangeTransferSyntax()" % inFile)

    writer = gdcm.ImageWriter()
    writer.SetFileName( outFile )
    writer.SetFile( reader.GetFile() )
    writer.SetImage( change.GetOutput() )
    if not writer.Write():
      raise Exception("Unable to write %s with gdcm.ImageWriter()" % outFile)

  except Exception as e:
    sys.stderr.write("%s, copying instead" % str(e))
    if inFile is not outFile:
        shutil.copyfile(inFile, outFile)

if __name__ == "__main__":
  inFile = sys.argv[1] # input filename
  outFile = sys.argv[2] # output filename
  decompress(inFile, outFile)
