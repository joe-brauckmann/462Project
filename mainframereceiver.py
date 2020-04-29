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
#INarray = scipy.io.loadmat("Proj1ModSymb.mat")['ModSymb']

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


######################## Decrypting Sequence ######################
#Polynomial were using, f(x) = 1 + x + x^2 + x^ 5 + x^19
reg1 = 1
reg2 = 0
reg3 = 0
reg4 = 0
reg5 = 0
reg6 = 0
reg7 = 0
reg8 = 0
reg9 = 0
reg10 = 0
reg11 = 0
reg12 = 0
reg13 = 0
reg14 = 0
reg15 = 0
reg16 = 0
reg17 = 0
reg18 = 0
reg19 = 0

PnSeq = []
Decrypt =[]
for i in range(2**19-1):
    PnSeq.append(reg19) 
    reg1,reg2,reg3,reg4,reg5,reg6,reg7,reg8,reg9,reg10,reg11,reg12,reg13, reg14,reg15,reg16,reg17,reg18,reg19  = reg19, (reg1+reg19)%2, (reg2+reg19)%2, reg3, reg4, (reg5+reg19)%2, reg6, reg7, reg8, reg9, reg10, reg11, reg12, reg13, reg14, reg15, reg16, reg17, reg18   
for i in range(len(output)):
    Decrypt.append(output[i]^PnSeq[i%(2**19-1)])


scipy.io.savemat('DecryptedData.mat', dict(DecryptedData=np.array([float(x) for x in Decrypt])), do_compression=True, oned_as='row')
