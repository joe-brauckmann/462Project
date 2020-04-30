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
    
#scipy.io.savemat('PnSeq.mat', dict(PnSeq=np.array([float(x) for x in PnSeq])), do_compression=True, oned_as='row')
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

scipy.io.savemat('ComplexSymbol.mat', dict(complexSym=np.array((complexSym)), do_compression=True, oned_as='row'))

############################################ IFFT Stage ##############################################
ifftList = []
for k in range(math.ceil(len(complexSym)/1024)):
    l = complexSym[1024*k:1024*k+1024]
    ifftList.append(np.fft.ifft(l))

ifftdummy = np.reshape(ifftList, -1)

scipy.io.savemat('IFFToutput.mat', dict(ifftList=np.array((ifftdummy)), do_compression=True, oned_as='row'))

########################################## Cyclic Prefix ###############################################
cyclicList = []

for m in range(len(ifftList)):
    x = ifftdummy[m*1024:m*1024+1024]
    y = ifftdummy[m*1024+1024-70:m*1024+1024]
    d = np.concatenate((y, x), axis = None)
    if len(d) == 0:
        break
    cyclicList+=d.tolist()
    
scipy.io.savemat('CyclicPrefixoutput.mat', dict(cyclicList=np.array((cyclicList)), do_compression=True, oned_as='row'))

####################################### Add Noise to Signal #############################################\
Amean = 0
ASD = 0.25
Pmean = 0
### Changing 22 degress to radians 
phaseSD = 22 * math.pi / 180  

### Generate the random noise based off of parameters
NoiseAmp = np.random.normal(Amean, ASD, len(cyclicList))
NoisePhase =  np.random.normal(Pmean, phaseSD, len(cyclicList))

### Get x,y coordinates of the random noise on the QPSK constillation 
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

scipy.io.savemat('SignalWithNoise.mat', dict(FinalNoise=np.array((FinalNoise)), do_compression=True, oned_as='row'))

############################################################### END OF TRANSMITTER STAGE #################################################################



############################################################## BEGIN RECIEVER STAGE ######################################################################

############################### Reshape signal withj noise ##########################
FinalNoise = np.transpose(FinalNoise).tolist()

############################### Remove Cyclic Prefix ################################
# Remove first 70 bits and store remaining 1024 into an array of lists
# Each list is 1024 bytes 
noPrefix = []
for i in range(len(FinalNoise)):
    noPrefix += FinalNoise[1094*i+70:1094*i+1094]

noPrefix = np.reshape(noPrefix, -1)

################ Save output to matlab file ################
scipy.io.savemat('RxCpRemove.mat', dict(RxCpRemove=np.array((noPrefix))), do_compression=True, oned_as='row')

#################### Use FFT function ######################
fftList = []
for i in range(math.ceil(len(noPrefix)/1024)):
    temp = noPrefix[1024*i:1024*i+1024]
    temp = np.fft.fftn(temp)
    fftList.append(temp)

################### Create 2-D array for output ########################
fftList = np.transpose(fftList)
scipy.io.savemat('RxFFT.mat', dict(RxFFT=np.array((fftList))), do_compression=True, oned_as='row')

################## OFDM Modulation to Encrypted Data ##########################
INarray = []
INarray = fftList

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

scipy.io.savemat('RxEncyrpted.mat', dict(FFTSymb=np.array((output))), do_compression=True, oned_as='row')
#####################################  SSRG Encryption ############################################
#Polynomial were using, f(x) = 1 + x^3 + x^31 
Registers = [1] + [0 for i in range(20)]
PnSeq = []
Decrypt =[]
for i in range(Pn_seq_length):
    PnSeq.append(Registers[0] ^ Registers[7])
    tmpReg = Registers[1]^Registers[20]
    Registers = [tmpReg] + Registers[:20]

for i in range(len(output)):
    Decrypt.append(output[i]^PnSeq[i%(Pn_seq_length)])
    
scipy.io.savemat('Decryptedata.mat', dict(Decrypt=np.array([float(x) for x in Decrypt])), do_compression=True, oned_as='row')

##################################### Test for error rate ##############################################
n = 0
tester = scipy.io.loadmat("Proj5InputData.mat")['InputData'][0].tolist()
for i in range(len(tester)):
    if tester[i] != Decrypt[i]:
        n+=1 
print(n/len(tester))

exit()
