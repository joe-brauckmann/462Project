#Team Hac
#Brandon Bastian
#Gavin Fisher
#Joe Brauckman
#Christopher Magtibay
#Max Zhang
#Sean Sacchetti

import numpy as np

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

############  SSRG  ####################
#    print("SSRG OUTPUT\n")
#    reg1 = 1
#    reg2 = 0
#    reg3 = 0
#    reg4 = 0
#    reg5 = 0
#    for i in range(31):
#        print("ITERATION #%d - reg1: %d   reg2: %d   reg3: %d   reg4: %d   reg5: %d"% (i, reg1, reg2, reg3, reg4, reg5)) 
#        reg1, reg2, reg3, reg4, reg5 = (reg2+reg5)%2, reg1, reg2, reg3, reg4
#^ commented out this code for right now because I don't think we need it, but uncomment it if I am wrong. -Joe	
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
    for i in range(31):
        print("ITERATION #%d - reg1: %d   reg2: %d   reg3: %d   reg4: %d   reg5: %d"% (i, reg1, reg2, reg3, reg4, reg5)) 
        reg1, reg2, reg3, reg4, reg5 = reg5, reg1, (reg5+reg2)%2, reg3, reg4   
	
#################################
#Convert to Complex Symbols
complexSym = []
realVals = []
imagVals = []
for j in range(int(len(MSRG)/2)):
	if bitstream[j*2] == 0:
		if bitstream[j*2 + 1] == 0:
			x = np.cos(45)
			y = np.sin(45)
		else:
			x = np.cos(315)
			y = np.sin(315)
	else:
		if bitstream[j*2 + 1] == 0:
			x = np.cos(135)
			y = np.sin(135)
		else:
			x = np.cos(225)
			y = np.sin(225)
	complexSym.append(float(x) + 1j * float(y))
	realVals.append(float(x))
	imagVals.append(float(y) * 1j)

print(complexSym)

