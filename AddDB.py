import math
import os
import pandas as pd
import csv
import numpy as np
import geogoogleapiwrapper as googleapi
import geopywrapper as geopywrap


class geolocation:

    inputfileextension = ".csv"
    inputfolder = 'input/'
    outputfolder = 'output/'
    outputfile = 'output.csv'
    pincodecolumnname = "pincode"
    inputset = set()
    outputset = set()
    differenceset = set()
    GOOGLEAPIPROVIDER = "googleapi"
    GEOPYWRAPPER = "geopywrapper"
    wrappertouse = ""
    outfileFound = False

    def __init__(self,wrapper="googleapi"):
        try:
            self.wrappertouse=wrapper
            files = os.listdir(self.inputfolder)
            for file in files:
                iterate = 1

                if os.path.splitext(file)[1]==self.inputfileextension and iterate == 1:
                    print(os.path.splitext(file)[0])
                    filetoload = str(self.inputfolder) + str(file)
                    self.inputdf = pd.read_csv(filetoload)
                    iterate= iterate + 1

            if (self.__fileexists(self.outputfolder, self.outputfile)):
                self.outputdf = pd.read_csv(self.outputfolder+ self.outputfile)
                print("output file exists, data loaded")
                self.outfileFound = True
            print("outptut found is : {}".format(self.outfileFound))
        except Exception as err:
            print('Class initiation failed due to exception : {}'.format(err.message))

    def __fileexists(self, filepath, filename):
        files = os.listdir(filepath)
        print("files count is {}".format(len(files)))
        for file in files:
            print("{} is the file now".format(os.path.basename(file)))
            if os.path.basename(file) == filename:
                return True
        return False

    def __dataexists(self):
        filehasContent = False

        if self.outfileFound:
            print ("reading into dataexists method")
            with open(self.outputfolder+ self.outputfile, 'rb') as r:
                oreader = csv.reader(r)
                for row in oreader:
                    if not (row == None):
                        filehasContent = True
                        print("File is not empty, append")
                        break
                r.close()
        return filehasContent

    """update or create the file if it doesnt exist"""
    def __updateorcreatefile(self, folderpath, file, dictionarylist, headercolumns):
        if self.outfileFound:
            with open(folderpath + file, 'a') as w:
                owriter = csv.writer(w)
                if not (self.__dataexists()):
                    owriter.writerow(headercolumns)
                for row in dictionarylist:
                    #print(row)
                    owriter.writerow(row)
                    print("file appended and wrote")
                w.close()
        else:
            with open(folderpath + file, 'wb') as w:
                owriter = csv.writer(w)
                owriter.writerow(headercolumns)
                for row in dictionarylist:
                    owriter.writerow(row)
                    print("file new row added and wrote")
                w.close()

    def writelatandlong(self,refreshAllPincodes=False ):
        dictionarylist = list()
        errordictlist = list()
        csvcolumns = ['pincode','latitude','longitude','aname']
        print('started')

        if not refreshAllPincodes:
            self.inputset = set(np.unique(x for x in self.inputdf[self.pincodecolumnname]))
            if self.outfileFound:
                self.outputset = set(np.unique(x for x in self.outputdf[self.pincodecolumnname]))
                self.differenceSet = self.inputset.difference(self.outputset)
                print("Difference set to be created,count of {}".format(len(self.differenceSet)))

            else:
                self.differenceSet = self.inputset
                print("Difference set same as input set since no file output found, count of {}".format(len(self.differenceSet)))
        elif refreshAllPincodes:
            print("Refreshing all pinsets")
            self.differenceSet = set(np.unique(x for x in self.inputdf[self.pincodecolumnname]))
