#Team Hac
#Brandon Bastian
#Gavin Fisher
#Joe Brauckman
#Christopher Magtibay
#Max Zhang
#Sean Sacchetti

import numpy as np
import math
#import scipy.io
# gonna need to install it too


# read matlab file directly use 
# data = scipy.io.loadmat(Filename)[Matlab variable name][0].tolist()
# "so much better than fucking around with text files 

#Read input file
f = open("Proj1TestDataASCII.txt", "r")
bitstream = []

#while(True):
for i in range(100):
    try:
		output = (f.read(16))
		bitstream.append(int(output[3]))
	except:
		break
	
print(bitstream)



#Polynomial were using, f(x) = 1 + x + x^2 + x^ 5 + x^19
############  MSRG  ####################
    print("\nMSRG OUTPUT\n")
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

#Instead of for loop, this shifting should happen every time you "call it" 
# sequence is 2^19 - 1 long, after this many iterations the shifting will start to repeat
# the nice way to do this is
# for i in range(2**19-1) is the correct way 
# have a list thats 2^19 -1 and have to loop fill the list
# for grading we have to submit the Pn sequence so its easy to store in a list then submit that
# adding red 19 to the list 
# whatever is in 19 at the start is the first thing of the Pn sequence, then shift take... forever 
# xor each bit of data with Pn sequence
# data is reallllllly big like 2 million and Pn sequence is roughly 500k so we need to xor first 500k of data with Pn then shift and repeat
# need to submut array of encrypted data which we should store in another array.
PnSeq = []
Encrypt =[]
    for i in range(2**19-1):
	PnSeq.append(reg19)
        ##print("ITERATION #%d - reg1: %d   reg2: %d   reg3: %d   reg4: %d   reg5: %d  reg6: %d reg7: %d reg8: %d reg9: %d reg10: %d reg11: %d reg12: %d reg13: %d reg14: %d reg15: %d reg16: %d reg17: %d reg18: %d reg19: %d "% (i, reg1, reg2, reg3, reg4, reg5, reg6, reg7, reg8, reg9, reg10, reg11, reg12, reg13, reg14, reg15, reg16, reg17, reg18, reg19)) 
        reg1,reg2,reg3,reg4,reg5,reg6,reg7,reg8,reg9,reg10,reg11,reg12,reg13, reg14,reg15,reg16,reg17,reg18,reg19  = reg19, (reg1+reg19)%2, (reg2+reg19)%2, reg3, reg4, (reg5+reg19)%2, reg6, reg7, reg8, reg9, reg10, reg11, reg12, reg13, reg14, reg15, reg16, reg17, reg18   
    for i in range(len(bitstream)):
	Encrypt.append(bitstream[i]^PnSeq[i%(2**19-1)])
	
print(PnSeq[:50]) #print first 50
exit()
#################################
#Convert to Complex Symbols
# NICK SAID
# Have to do it in radians so 45 = pi/4 etc (need math.pi)
#Theres a complex data type in python 
complexSym = []
realVals = []
imagVals = []
for j in range(int(len(MSRG)/2)):
	if bitstream[j*2] == 0:
        	if bitstream[j*2 + 1] == 0:
           		x = np.cos(math.pi/4)
            		y = np.sin(math.pi/4)
        	else:
            		x = np.cos(math.pi*7/4)
            		y = np.sin(math.pi*7/4)
    	else:
        	if bitstream[j*2 + 1] == 0:
            		x = np.cos(math.pi*3/4)
            		y = np.sin(math.pi*3/4)
        	else:
           		x = np.cos(math.pi*5/4)
            		y = np.sin(math.pi*5/4)
			#example. 
			#complex(1,2)
			#this is actually 1+2i 
			
	complexSym.append(complex(x,y))
	#realVals.append(float(x))
	#imagVals.append(float(y) * 1j)

ifftList = []

for k in range(math.ceil(len(complexSym)/1024)):
	l = complexSym[1024*k:1024*k+1023]
	while (len(l) < 1024):
		l.append(0)
	ifftList.append(l)

###########IFFT##################
#NICK VERIFIED THIS IS CORRECT
# Nick used ifftn function not sure if theres a difference
#Uses IFFT to encode QPSK output array (Not entirely sure if correct, yet..)
ifftOut = np.fft.ifft(ifftList)
