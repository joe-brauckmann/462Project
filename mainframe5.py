#Team Hac
#Project 5
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

###################################### Define code constants #####################################
Pn_seq_length = 2**21-1
PiOver4 = math.pi/4
Pi74 = math.pi*7/4
Pi34 = math.pi*3/4
Pi54 = math.pi*5/4

########################################### Open File #############################################
bitstream = []
bitstream = scipy.io.loadmat("Proj5InputData.mat")['InputData'][0].tolist()

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

########################################### QPSK Symbols ###########################################
complexSym = []

for j in range(int(len(Encrypt)/2)):
    if Encrypt[j*2] == 0:
        if Encrypt[j*2 + 1] == 0:
            x = np.cos(PiOver4)
            y = np.sin(PiOver4)
        else:
            x = np.cos(Pi74)
            y = np.sin(Pi74)
    else:
        if Encrypt[j*2 + 1] == 0:
            x = np.cos(Pi34)
            y = np.sin(Pi34)
        else:
            x = np.cos(Pi54)
            y = np.sin(Pi54)
    complexSym.append(complex(x,y))

scipy.io.savemat('ComplexSymbol.mat', dict(complexSym=np.array(complexSym)), do_compression=True, oned_as='row')

############################################ IFFT Stage ##############################################
ifftList = []
i = [0]
for k in range(math.ceil(len(complexSym)/1024)):
    l = complexSym[1024*k:1024*k+1024]
    ifftList.append(np.fft.ifft(l))

scipy.io.savemat('IFFToutput.mat', dict(ifftList=np.array((ifftList)), do_compression=True, oned_as='row'))


########################################## Cyclic Prefix ###############################################
cyclicList = []
for m in range(len(ifftList)):
    y = ifftList[m][-70:]
    x = ifftList[m][0:1023]
    np.append(y,x)
    cyclicList.append(y)

scipy.io.savemat('CyclicPrefixoutput.mat', dict(cyclicList=np.array((cyclicList)), do_compression=True, oned_as='row'))

####################################### Add Noise to Signal #############################################\
Amean = 0
ASD = 0.25
Pmean = 0
### Changing 22 degress to radians 
phaseSD = 22 * math.pi / 180  

NoiseAmp = np.random.normal(Amean, ASD, len(cyclicList))
NoisePhase =  np.random.normal(Pmean, phaseSD, len(cyclicList))

NoiseX = np.cos(NoisePhase)
NoiseY = np.sin(NoisePhase)

complexNoise = np.vectorize(complex)(NoiseX, NoiseY)
complexNoise = np.multiply(complexNoise, NoiseAmp)

NoiseIFFT = []
for k in range(math.ceil(len(complexNoise)/1094)):
    l = complexNoise[1094*k:1094*k+1094]
    NoiseIFFT += np.fft.ifft(l).tolist()

NoiseIFFT = np.array(NoiseIFFT)
FinalNoise = np.add(NoiseIFFT, cyclicList)

scipy.io.savemat('SignalWithNoise.mat', dict(NoiseSignal=np.array((NoiseSignal)), do_compression=True, oned_as='row'))


exit()
