import random
import numpy as np
from bitarray import bitarray

class Discriminator: 

    def __init__(self, entrySize, tupleSize, data=None):
        
        self.entrySize = entrySize
        self.tupleSize = tupleSize
        self.numRams = entrySize // tupleSize + (entrySize % tupleSize > 0)
        self.tuplesMapping = list(range(entrySize))  
        
        print((self.numRams))
        # gerar aleatório
        
        random.shuffle(self.tuplesMapping)

        #print(self.tuplesMapping)

        self.rams = []

        for i in range(self.numRams):
            ram = bitarray(tupleSize)

            self.rams.append(ram)

        print(self.rams)

    def train(self,data):
    
        k = 0
        for i in range(self.numRams):

            addr_pos = self.tupleSize-1
            addr = 0
            
            for j in range (self.tupleSize):
                i1 = self.tuplesMapping[k] >> 6
                i2 = self.tuplesMapping[k] & 0x3F
            
                addr |= ((int(data[i1]) & (1 << i2)) >> i2) << addr_pos
                addr_pos -= 1
                k += 1

            #print(self.rams[i][addr])
        

    def train_vector(self, data):

        k = 0

        for i in range (self.numRams):
            addr_pos = self.tupleSize -1
            addr = 0

            for j in range (self.tupleSize):
                if k < self.entrySize:
                    addr |= (data[self.tupplesMapping[k]]<<addr_pos)
                    addr_pos -=1
                    k+=1
            
            #self.rams[i][addr] = 1
            print(self.rams)

    def rank(self, data):
        rank = 0
        k = 0

        for i in range(self.numRams):
            addr_pos = self.tupleSize - 1
            addr = 0

            for j in range(self.tupleSize):
                i1 = self.tuplesMapping[k] >> 6  # Divide by 64 to find the bitarray id
                i2 = self.tuplesMapping[k] & 0x3F  # Obtain remainder to access the bitarray position

                addr |= ((data[i1] & (1 << i2)) >> i2) << addr_pos
                addr_pos -= 1
                k += 1

            i1 = addr >> 6  # Divide by 64 to find the bitarray id
            i2 = addr & 0x3F  # Obtain remainder to access the bitarray position
            rank += (self.rams[i]['bitarray'][i1] & (1 << i2)) >> i2

        return rank

    def rank_vector(self, data):
        rank = 0
        k = 0

        for i in range(self.numRams):
            addr_pos = self.tupleSize - 1
            addr = 0

            for j in range(self.tupleSize):
                if k < self.entrySize:
                    addr |= (data[self.tuplesMapping[k]] << addr_pos)
                    addr_pos -= 1
                    k += 1

            i1 = addr >> 6  # Divide by 64 to find the bitarray id
            i2 = addr & 0x3F  # Obtain remainder to access the bitarray position
            rank += (self.rams[i]['bitarray'][i1] & (1 << i2)) >> i2

        return rank

    def info():
    
        totalBits = 0
        print("Entry = ", self.entrySize, ", Tuples = ",self.tupleSize, ", RAMs = ",self.numRams,", RAM size = ",len(self.rams)," bits\n")
        
        for i in range (self.numRams):

            print("RAM ",i," - ",self.rams[i]," bits\n")
            totalBits += self.rams[i]

        print("Total Bits = ", totalBits)
    

    def reset():
    
        #Generating pseudo-random mapping

        for i in range (self.entrySize):
            self.tuplesMapping[i] = i
        
        
        random.shuffle(self.tuplesMapping)

        for i in range(self.numRams):
            for j in range(self.rams[i].bitarray_size):
                self.rams[i].bitarray[j] = 0
            

    def getRamBits(): 
        return len(self.rams)
    

    def getNumRams():
        return self.numRams

####### main #######

disc = Discriminator(1024, 16)
data = np.zeros(1024, dtype=bool)

for i in range(1024):
    data[i] = i&1

print(data)
#está imprimindo em true e false, modificar
    
#Não estou conseguindo executar daqui para frente
disc.train(data)

print("Rank= " ,disc.rank(data), "\n")
disc.info()

# del disc

