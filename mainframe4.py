#Project Part 4
#Python3
#Team Hac
#Brandon Bastian
#Gavin Fisher
#Sean Sacchetti
#Joe Brauckmann
#Chris Magtibay
#Max Zhang

#################### Import Numpy and Scipy libraries for matlab file reading/saving ###########################
import numpy as np
import scipy.io
import math

INarray = []
INarray = scipy.io.loadmat("FFTSymb.mat")['FFTSymb'].tolist()

INarray = np.reshape(INarray, -1)
output = []

for i in range(len(INarray)):
    if (np.real(INarray[i]) < 0):
        if(np.imag(INarray[i]) < 0):
            x = 1
            y = 1
            output.append(x)
            output.append(y)
        else:
            x = 1
            y = 0
            output.append(x)
            output.append(y)
    elif (np.real(INarray[i]) > 0):
        if(np.imag(INarray[i]) < 0):
            x = 0
            y = 1
            output.append(x)
            output.append(y)
        else:
            x = 0
            y = 0
            output.append(x)
            output.append(y)


scipy.io.savemat('EncryptedData.mat', dict(EncryptedData=np.array(output)), do_compression=True, oned_as='row')
