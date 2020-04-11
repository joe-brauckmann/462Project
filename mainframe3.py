#Project Part 3
#Python3
#Team Hac
import numpy as np
import scipy.io
import math

OFDMSymb = []
OFDMSymb = scipy.io.loadmat("RxOFDMSymb.mat")['OFDMSymbStream'][0].tolist()

fftList = []
for i in range(math.ceil(len(OFDMSymb)/1024)):
    temp = OFDMSymb[1024*i:1024*i+1024]
    temp = np.fft.fft(temp)
    fftList.append(temp)

np.reshape(fftList, -1)
scipy.io.savemat('FFTSymb.mat', dict(FFTSymb=np.array((fftList))), do_compression=True, oned_as='row')
