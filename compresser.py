import argparse
import os
from skimage import io

class compressor:
    def __init__(self):
        pass

    def cloneCompress(self,dirHandle):
        compressions = [20,50,75,85]
        with open(dirHandle,'r') as f:
            for line in f:
                dir = line.split(sep=':')[-1].rstrip() + '/'
                for img in os.listdir(dir):
                    ext = img.split(sep='.')[1]
                    imgArr = io.imread(dir+img)
                    if((ext != "jpg") & (ext != "jpeg")):
                        img += ".jpg"
                    for compression in compressions:
                        io.imsave(dir+'_'+str(compression)+'_'+img,imgArr,quality=compression)
                    
        pass

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("dictionaryFile", help="The same kind of dictionary file that leads to character images")

    args = parser.parse_args()

    frame = compressor()
    frame.cloneCompress(args.dictionaryFile)