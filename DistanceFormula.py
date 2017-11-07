import math
import collections

class distancecalculator:

    earthradius = 6371
    leastdistance = None
    leastvaluekey = None

    def getequirectangulardistance(self, source, destinationset):
        try:
            sourcelat = math.radians(source[0])
            sourcelong = math.radians(source[1])
            distance = dict()
            for destination in destinationset:
                destlat = destination[1][0]
                destlong = destination[1][1]

                if not (destlat == None):
                    destlat = math.radians(destlat)
                    destlong = math.radians(destlong)
                    d = self.__getdistancebyequiangularformula(destlong,sourcelong,destlat,sourcelat)
                    print("Distance is {}".format(d))
                    distance[destination[0]] = d
                    self.__setleastKeyandValue(d,destination[0])
                    print("Done")
            print("Least distance Pincode is {} among the set at a distance of {}kms from source.".format(self.leastvaluekey,self.leastdistance))
        except Exception as err:
            print ("Exception occurred : {}".format(err.message))

    def __getdistancebyequiangularformula(self,destlong,sourcelong,destlat,sourcelat):
        X = (destlong - sourcelong) * math.cos((destlat + sourcelat) / 2)
        Y = destlat - sourcelat
        return self.earthradius * math.sqrt(X * X + Y * Y)

    def __setleastKeyandValue(self,distance, key):
        if (self.leastdistance == None or distance < self.leastdistance):
            self.leastdistance = distance
            self.leastvaluekey = key

        print (self.leastdistance)


distance = distancecalculator()
