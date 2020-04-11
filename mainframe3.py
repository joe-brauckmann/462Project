#Project Part 3
#Python3
#Team Hac
import numpy as np
import scipy.io
import math

OFDMSymb = []
OFDMSymb = scipy.io.loadmat("RxOFDMSymb.mat")['OFDMSymbStream'][0].tolist()

fftList = []
fftList = np.fft.fft(OFDMSymb)

scipy.io.savemat('FFTSymb.mat', dict(FFTSymb=np.array((fftList))), do_compression=True, oned_as='row')
