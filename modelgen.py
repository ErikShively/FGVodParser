import configparser
import argparse
import pickle
import numpy as np
import pickle
from skimage import io
from os import listdir
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB
import sklearn_json as skljson

class IDmodel:
    def __init__(self, game="TEMPLATE", modelType="UNTRAINED",inModel=None):
        self.game = game
        self.modelType = modelType
        self.model = inModel
        self.trainDict = dict()

    def readConfig(self, configFile="configs/config.ini"):
        if(configFile == None):
            configFile = "configs/config.ini"
        config = configparser.ConfigParser()
        config.read(configFile)

        res = [int(x) for x in config["GENERAL"]["BaseRes"].split(sep=':')]

        Box_X = config[self.game]["Box_X"]
        XMin = int(Box_X.split(sep=':')[0])
        XMax = int(Box_X.split(sep=':')[1])

        Box_Y = config[self.game]["Box_Y"]
        YMin = int(Box_Y.split(sep=':')[0])
        YMax = int(Box_Y.split(sep=':')[1])

        with open(config[self.game]["charDict_L"], "r") as f:
            for line in f:
                charName = (line.split(sep=':')[0])
                directory = line.split(sep=':')[-1].rstrip() + '/'
                imgList = []
                for img in listdir(directory):
                    processedImg = io.imread(directory + img)
                    processedImg = processedImg[YMin:YMax,XMin:XMax]
                    imgList.append(processedImg)
                self.trainDict[charName] = imgList

        with open(config[self.game]["charDict_R"], "r") as f:
            for line in f:
                charName = (line.split(sep=':')[0])
                directory = line.split(sep=':')[-1].rstrip() + '/'
                imgList = []
                for img in listdir(directory):
                    processedImg = io.imread(directory + img)
                    processedImg = processedImg[YMin:YMax,(res[0] - XMax):(res[0] - XMin)]
                    processedImg = processedImg[:,::-1]
                    imgList.append(processedImg)
                self.trainDict[charName] = imgList

    def train(self,mType,outName=None, useJSON=False) -> bool:
        trainTarget = []
        trainPred = []
        self.modelType = mType
        for target,pred in self.trainDict.items():
            for img in pred:
                trainTarget.append(target)
                trainPred.append(img)
        n = len(trainPred)
        trainPred = np.array(trainPred).reshape((n,-1))
        if(mType.lower()=="svm"):
            model = SVC(gamma=0.001)
            model.fit(X=trainPred,y=trainTarget)
        elif(mType.lower()=="gnb"):
            model = GaussianNB()
            model.fit(X=trainPred,y=trainTarget)
        else:
            print("Supported types: GNB, SVM.")
            return False
        if(outName==None):
            outName = "models/" + self.game+mType.lower()
        if(useJSON):
            outName+=".json"
            skljson.to_json(model,outName)
        else:
            outName+=".pickle"
            with open(outName,'wb') as f:
                pickle.dump(model,f,protocol=pickle.HIGHEST_PROTOCOL)
        return True
        



if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Generates a model to identify images/videos")
    parser.add_argument("game", help="The game to build the model from")
    parser.add_argument("modelType", help="The model to use. Supported models are: GNB,SVM")
    parser.add_argument("-c","--config", help="The config file to read from")
    parser.add_argument("-o","--output", help="The handle of the output file. Automatically appends extention.")
    parser.add_argument("-j","--json", help="Saves model as JSON and not pickle. JSON files are safer than pickle files if you distribute the models. However, the plugin to save the models is inconsistent. USE AT YOUR OWN RISK.", action="store_true")

    args = parser.parse_args()

    frame = IDmodel(game=args.game)
    frame.readConfig(configFile=args.config)
    frame.train(mType=args.modelType, outName=args.output, useJSON=args.json)
        
