# CMPEN 462 Project Part 5
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

################Open File################
bitstream = []
bitstream = scipy.io.loadmat("Proj1InputData.mat")['InputData'][0].tolist()
    
#print(bitstream)



#Polynomial were using, f(x) = 1 + x^2 + x^5 + x^13 + x^21
############  MSRG  ####################
#print("\nMSRG OUTPUT\n")
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
reg20 = 0
reg21 = 0

PnSeq = []
Encrypt =[]
for i in range(2**21-1):
    PnSeq.append(reg21)
    ##print("ITERATION #%d - reg1: %d   reg2: %d   reg3: %d   reg4: %d   reg5: %d  reg6: %d reg7: %d reg8: %d reg9: %d reg10: %d reg11: %d reg12: %d reg13: %d reg14: %d reg15: %d reg16: %d reg17: %d reg18: %d reg19: %d "% (i, reg1, reg2, reg3, reg4, reg5, reg6, reg7, reg8, reg9, reg10, reg11, reg12, reg13, reg14, reg15, reg16, reg17, reg18, reg19)) 
    reg1,reg2,reg3,reg4,reg5,reg6,reg7,reg8,reg9,reg10,reg11,reg12,reg13, reg14,reg15,reg16,reg17,reg18,reg19,reg20,reg21  = reg21, (reg1+reg21)%2, (reg2+reg21)%2, reg3, reg4, (reg5+reg21)%2, reg6, reg7, reg8, reg9, reg10, reg11, reg12, (reg13+reg21)%2, reg14, reg15, reg16, reg17, reg18, reg19, reg20   
for i in range(len(bitstream)):
    Encrypt.append(bitstream[i]^PnSeq[i%(2**21-1)])
    
scipy.io.savemat('PnSeq.mat', dict(PnSeq=np.array([float(x) for x in PnSeq])), do_compression=True, oned_as='row')
scipy.io.savemat('EncryptedData.mat', dict(Encrypt=np.array([float(x) for x in Encrypt])), do_compression=True, oned_as='row')
