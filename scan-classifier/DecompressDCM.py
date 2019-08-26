import gdcm
import sys

def decompress(inFile, outFile):
  print("Decompressing %s to %s" % (inFile, outFile))
  reader = gdcm.ImageReader()
  reader.SetFileName( inFile )

  if not reader.Read():
    sys.stderr.write("Unable to read %s" % inFile)
    sys.exit(1)

  change = gdcm.ImageChangeTransferSyntax()
  change.SetTransferSyntax( gdcm.TransferSyntax(gdcm.TransferSyntax.ImplicitVRLittleEndian) )
  change.SetInput( reader.GetImage() )
  if not change.Change():
    sys.stderr.write("Unable to change %s" % inFile)
    sys.exit(1)

  writer = gdcm.ImageWriter()
  writer.SetFileName( outFile )
  writer.SetFile( reader.GetFile() )
  writer.SetImage( change.GetOutput() )

  if not writer.Write():
    sys.stderr.write("Unable to write %s" % outFile)
    sys.exit(1)

if __name__ == "__main__":
  inFile = sys.argv[1] # input filename
  outFile = sys.argv[2] # output filename
  decompress(inFile, outFile)
