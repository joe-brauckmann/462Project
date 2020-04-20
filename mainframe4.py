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


######################## Decrpyting Sequence ######################
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
