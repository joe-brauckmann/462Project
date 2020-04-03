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
#Rxstream = scipy.io.loadmat('ProjectRxSymbStream.mat')['RxSymbStream']
RxTransposed = np.transpose(scipy.io.loadmat('ProjRxSymbStream.mat')['RxSymbStream']).tolist()


################ Cyclic Prefix ################
# Remove first 70 bits and store remaining 1024 into an array of lists
# Each list is 1024 bytes 
noPrefix = []
for i in range(len(RxTransposed)):
    noPrefix += RxTransposed[i][70:]


################ Save output to matlab file ################
scipy.io.savemat('RxOFDMSymb.mat',dict(OFDMSymbStream=np.array(noPrefix)),oned_as='row')
