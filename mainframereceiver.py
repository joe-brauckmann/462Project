#Team Hac
#Project 5 - Reciever 
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
################################ Define Code Constants ##############################
Pn_seq_length = 2**21-1

################ Open the file & read it using SCIPY library ################
RxTransposed = np.transpose(scipy.io.loadmat('SignalWithNoise.mat')['NoiseSignal']).tolist()

############################### Remove Cyclic Prefix ################################
# Remove first 70 bits and store remaining 1024 into an array of lists
# Each list is 1024 bytes 
noPrefix = []
for i in range(len(RxTransposed)):
    noPrefix += RxTransposed[1094*i+70:1094*i+1094]

noPrefix = np.reshape(noPrefix, -1)

################ Save output to matlab file ################
scipy.io.savemat('RxOFDMSymb.mat', dict(OFDMSymbStream=np.array((noPrefix))), do_compression=True, oned_as='row')

#################### Open IFFT OFDM Symbol Stream ######################
OFDMSymb = []
OFDMSymb = scipy.io.loadmat("RxOFDMSymb.mat")['OFDMSymbStream'][0].tolist()

#################### Use FFT function ######################
fftList = []
for i in range(math.ceil(len(OFDMSymb)/1024)):
    temp = OFDMSymb[1024*i:1024*i+1024]
    temp = np.fft.fftn(temp)
    fftList.append(temp)

################### Create 2-D array for output ########################
fftList = np.transpose(fftList)

################### Save 2-D array to matlab file ######################
scipy.io.savemat('FFTSymb.mat', dict(FFTSymb=np.array((fftList))), do_compression=True, oned_as='row')

################## OFDM Modulation to Encrypted Data ##########################
INarray = []
INarray = scipy.io.loadmat("FFTSymb.mat")['FFTSymb']

INarray = np.transpose(INarray)
INarray = np.reshape(INarray, -1)

output = []
for i in range(len(INarray)):
    if (INarray[i].real < 0):
        if((INarray[i].imag) < 0):
            x = 1
            y = 1
            output.append(x)
            output.append(y)
        else:
            x = 1
            y = 0
            output.append(x)
            output.append(y)
    elif (INarray[i].real > 0):
        if(INarray[i].imag < 0):
            x = 0
            y = 1
            output.append(x)
            output.append(y)
        else:
            x = 0
            y = 0
            output.append(x)
            output.append(y)

#####################################  SSRG Encryption ############################################
#Polynomial were using, f(x) = 1 + x^3 + x^31 
Registers = [1] + [0 for i in range(20)]
PnSeq = []
Encrypt =[]
for i in range(Pn_seq_length):
    PnSeq.append(Registers[0] ^ Registers[7])
    tmpReg = Registers[1]^Registers[20]
    Registers = [tmpReg] + Registers[:20]

for i in range(len(bitstream)):
    Encrypt.append(bitstream[i]^PnSeq[i%(Pn_seq_length)])
    
scipy.io.savemat('PnSeq.mat', dict(PnSeq=np.array([float(x) for x in PnSeq])), do_compression=True, oned_as='row')
scipy.io.savemat('EncryptedData.mat', dict(Encrypt=np.array([float(x) for x in Encrypt])), do_compression=True, oned_as='row')
