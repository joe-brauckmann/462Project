#Team Hac
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

#Data submission: PN seq, 


################Open File################
bitstream = []
bitstream = scipy.io.loadmat("Proj1InputData.mat")['InputData'][0].tolist()
    
#print(bitstream)



#Polynomial were using, f(x) = 1 + x + x^2 + x^ 5 + x^19
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

PnSeq = []
Encrypt =[]
for i in range(2**19-1):
    PnSeq.append(reg19)
    ##print("ITERATION #%d - reg1: %d   reg2: %d   reg3: %d   reg4: %d   reg5: %d  reg6: %d reg7: %d reg8: %d reg9: %d reg10: %d reg11: %d reg12: %d reg13: %d reg14: %d reg15: %d reg16: %d reg17: %d reg18: %d reg19: %d "% (i, reg1, reg2, reg3, reg4, reg5, reg6, reg7, reg8, reg9, reg10, reg11, reg12, reg13, reg14, reg15, reg16, reg17, reg18, reg19)) 
    reg1,reg2,reg3,reg4,reg5,reg6,reg7,reg8,reg9,reg10,reg11,reg12,reg13, reg14,reg15,reg16,reg17,reg18,reg19  = reg19, (reg1+reg19)%2, (reg2+reg19)%2, reg3, reg4, (reg5+reg19)%2, reg6, reg7, reg8, reg9, reg10, reg11, reg12, reg13, reg14, reg15, reg16, reg17, reg18   
for i in range(len(bitstream)):
    Encrypt.append(bitstream[i]^PnSeq[i%(2**19-1)])
    
scipy.io.savemat('PnSeq.mat', dict(PnSeq=np.array([float(x) for x in PnSeq])), do_compression=True, oned_as='row')
scipy.io.savemat('EncryptedData.mat', dict(Encrypt=np.array([float(x) for x in Encrypt])), do_compression=True, oned_as='row')

#########QPSK Symbols##############
complexSym = []
for j in range(int(len(Encrypt)/2)):
    if Encrypt[j*2] == 0:
        if Encrypt[j*2 + 1] == 0:
            x = np.cos(math.pi/4)
            y = np.sin(math.pi/4)
        else:
            x = np.cos(math.pi*7/4)
            y = np.sin(math.pi*7/4)
    else:
        if Encrypt[j*2 + 1] == 0:
            x = np.cos(math.pi*3/4)
            y = np.sin(math.pi*3/4)
        else:
            x = np.cos(math.pi*5/4)
            y = np.sin(math.pi*5/4)
            
    complexSym.append(complex(x,y))


scipy.io.savemat('ComplexSymbol.mat', dict(complexSym=np.array(complexSym)), do_compression=True, oned_as='row')
print(complexSym[0])
################IFFT#########################
ifftList = []
i = [0]
for k in range(math.ceil(len(complexSym)/1024)):
    l = complexSym[1024*k:1024*k+1024]
    ifftList.append(np.fft.ifft(l))

ifftdummy = np.reshape(ifftList, -1)

scipy.io.savemat('OFDMSymb.mat', dict(ifftList=np.array((ifftdummy)), do_compression=True, oned_as='row'))


################Cyclic Prefix################

cyclicList = []

for m in range(len(ifftdummy)):
    x = ifftdummy[m*1024:m*1024+1024]
    y = ifftdummy[m*1024+1024-70:m*1024+1024]
    d = np.concatenate((y, x), axis = None)
    if len(d) == 0:
        break
    cyclicList.append(d)
    

cyclicDummy = np.reshape(cyclicList, -1)
#print(len(cyclicDummy))  
scipy.io.savemat('TransSym.mat', dict(cyclicList=np.array((cyclicDummy)), do_compression=True, oned_as='row'))

################Up-Convert#################
f = 100000000
symTime = 1/(1024*10000)
for n in range(len(cyclicList)):
    for o in range(len(cyclicList[n])):
        x = cyclicList[n][o].real
        y = cyclicList[n][o].imag
        x *= math.cos(2*math.pi*f*(n*1094+o+1)*symTime)
        y *= math.sin(2*math.pi*f*(n*1094+o+1)*symTime)
        cyclicList[n][o] = complex(x,y)

cyclicDummy = np.reshape(cyclicList, -1)  
#print(len(cyclicDummy))    
scipy.io.savemat('UpConvertedSym.mat', dict(cyclicList=np.array((cyclicDummy)), do_compression=True, oned_as='row'))

exit()
