import pickle
import modelgen
import argparse
import sklearn
import configparser
import imageio
import sklearn_json as skljson
import numpy as np
from skimage import io

class vidparse:
    def __init__(self, modelFile, game, config="configs/config.ini"):
        ext = modelFile.split(sep='.')[-1]
        self.model = None
        self.game = game
        if(config==None):
            self.config = "configs/config.ini"
        else:
            self.config = config
        if(ext=="json"):
            self.model = (skljson.from_json(modelFile))
        elif(ext=="pickle"):
            with open(modelFile, 'rb') as f:
                self.model = pickle.load(f)
        else:
            print("Unknown extention")

    def classifyImg(self,img):
        config = configparser.ConfigParser()
        config.read(self.config)

        res = [int(x) for x in config["GENERAL"]["BaseRes"].split(sep=':')]

        Box_X = config[self.game]["Box_X"]
        XMin = int(Box_X.split(sep=':')[0])
        XMax = int(Box_X.split(sep=':')[1])

        Box_Y = config[self.game]["Box_Y"]
        YMin = int(Box_Y.split(sep=':')[0])
        YMax = int(Box_Y.split(sep=':')[1])

        imgList = []

        processedImg = img[YMin:YMax,XMin:XMax]
        imgList.append(processedImg)

        processedImg = img[YMin:YMax,(res[0] - XMax):(res[0] - XMin)]
        processedImg = processedImg[:,::-1]
        imgList.append(processedImg)
        imgList = np.array(imgList).reshape((2,-1))
        return(self.model.predict(imgList))
        
    def classifyImgFromFile(self,filePath):
        img = io.imread(filePath)
        return self.classifyImg(img)

    def classifyVideo(self,videoPath):
        vid = imageio.get_reader(videoPath, 'ffmpeg')
        frames = round(vid.get_meta_data()['fps'] * vid.get_meta_data()['duration'])-1
        for i in range(0,frames):
            print(self.classifyImg(vid.get_data(i)))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("modelFile", help="The model file to use")
    parser.add_argument("game", help="The game in the processed video")
    parser.add_argument("video", help="The video to parse")
    parser.add_argument("-c","--config", help="The config file to read from")
    args = parser.parse_args()
    frame = vidparse(args.modelFile,args.game.upper())
    frame.classifyVideo(args.video)