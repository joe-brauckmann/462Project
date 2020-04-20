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


PnSeq = []
Bitstream = []
PnSeq = scipy.io.loadmat("EncryptedData.mat")['EncryptedData'].tolist()

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

for i in range(2**19-1):
    PnSeq.append(reg19)
    ##print("ITERATION #%d - reg1: %d   reg2: %d   reg3: %d   reg4: %d   reg5: %d  reg6: %d reg7: %d reg8: %d reg9: %d reg10: %d reg11: %d reg12: %d reg13: %d reg14: %d reg15: %d reg16: %d reg17: %d reg18: %d reg19: %d "% (i, reg1, reg2, reg3, reg4, reg5, reg6, reg7, reg8, reg9, reg10, reg11, reg12, reg13, reg14, reg15, reg16, reg17, reg18, reg19)) 
    reg1,reg2,reg3,reg4,reg5,reg6,reg7,reg8,reg9,reg10,reg11,reg12,reg13, reg14,reg15,reg16,reg17,reg18,reg19  = reg19, (reg1+reg19)%2, (reg2+reg19)%2, reg3, reg4, (reg5+reg19)%2, reg6, reg7, reg8, reg9, reg10, reg11, reg12, reg13, reg14, reg15, reg16, reg17, reg18   
    for i in range(len(EncryptedData)):
    Bitstream.append(EncryptedData[i]^PnSeq[i%(2**19-1)])
    
    scipy.io.savemat('BitStream.mat', dict(Bitstream=np.array([float(x) for x in Bitsrean])), do_compression=True, oned_as='row')
