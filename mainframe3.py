#Project Part 3
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

#################### Open IFFT OFDM Symbol Stream ######################
OFDMSymb = []
OFDMSymb = scipy.io.loadmat("ProjectIFFTOfdmSymbolStream.mat")['OFDMSymbStream'][0].tolist()

#################### Use FFT function ######################
fftList = []
for i in range(math.ceil(len(OFDMSymb)/1024)):
    temp = OFDMSymb[1024*i:1024*i+1024]
    temp = np.fft.fftn(temp)
    fftList.append(temp)

################### Create 2-D array for output ########################
fftList = np.reshape(fftList, (1024,10000))

################### Save 2-D array to matlab file ######################
scipy.io.savemat('FFTSymb.mat', dict(FFTSymb=np.array((fftList))), do_compression=True, oned_as='row')
