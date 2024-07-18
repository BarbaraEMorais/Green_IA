#wisard.py finalizado = conversão de .cc

import numpy as np

from discriminator import Discriminator

#from bloomwisard.core.src.discriminator import Discriminator


class Wisard:

    def __init__(self, entrySize, tupleSize, numDiscriminator):
        self.entrySize = entrySize
        self.tupleSize = tupleSize
        self.numDiscriminator = numDiscriminator
        self.discriminators = []
        for i in range (self.numDiscriminators):    
            self.discriminators.append(Discriminator(self.entrySize,self.tupleSize))
        

    def addDiscriminator(self):
        self.discriminators.append(Discriminator(self.entrySize, self.tupleSize))


    def train(self, data, label):

        for i in range (len(label)):
            self.discriminators[label[i]].train(data[i])
        
    
    def rank(self,data):
        label = np.zeros(len(data), dtype=int)  

        for i in range(len(data)):
            max_resp = 0
            for j in range(len(self.discriminators)):
                resp = self.discriminators[j].rank(data[i])

                if resp > max_resp:
                    max_resp = resp
                    label[i] = j

        return label


    def info(self):

        print("Número de Discriminadores", self.numDiscriminator, "\n")

        for i in range (self.numDiscriminator):
            print("Discriminator ", i, ": ")
            self.discriminators[i].info()
        
    
    def stats(self):

        stats = np.zeros(4, dtype=np.uint64)

        numRams = self.discriminators[0].getNumRams()
        ramSize = self.discriminators[0].getRamBits()
        totalRamBits = numRams * ramSize
        totalBits = len(self.discriminators) * totalRamBits

        stats[0] = numRams
        stats[1] = ramSize
        stats[2] = totalRamBits
        stats[3] = totalBits

        return stats

    def reset(self):
        
        for i in range (self.numDiscriminator):
            self.discriminators[i].reset()
            

#testando o código
disc = Discriminator(1024, 16)

data = np.zeros(1024, dtype=bool)

for i in range (1024):
    data[i] = i&1
    print(data[i])
    

disc.train(data)

print("Rank= ", disc.rank(data), "\n")
disc.info()
del disc
