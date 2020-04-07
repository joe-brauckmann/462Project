#Team Hac
#Project 2
#Brandon Bastian
#Gavin Fisher
#Joe Brauckman
#Christopher Magtibay
#Max Zhang
#Sean Sacchetti


#Python3
import numpy as np
import scipy.io
import math

################ Open the file & read it using SCIPY library ################
RxTransposed = np.transpose(scipy.io.loadmat('Proj2RxSymbStream.mat')['RxSymbStream']).tolist()


################ Cyclic Prefix ################
# Remove first 70 bits and store remaining 1024 into an array of lists
# Each list is 1024 bytes 
noPrefix = []
for i in range(len(RxTransposed)):
    noPrefix += RxTransposed[1094*i+70:1094*i+1094]

noPrefix = np.reshape(noPrefix, -1)


################ Save output to matlab file ################
scipy.io.savemat('RxOFDMSymb.mat', dict(OFDMSymbStream=np.array((noPrefix))), do_compression=True, oned_as='row')
