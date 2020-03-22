#Team Hac
#Brandon Bastian
#Gavin Fisher
#Joe Brauckman
#Chris Magtibay
#Max Zhang
#Sean Sacchetti
#Polynomial were using, f(x) = 1 + x + x^2 + x^ 5 + x^19
############  SSRG  ####################
    print("SSRG OUTPUT\n")
    reg1 = 1
    reg2 = 0
    reg3 = 0
    reg4 = 0
    reg5 = 0
    for i in range(31):
        print("ITERATION #%d - reg1: %d   reg2: %d   reg3: %d   reg4: %d   reg5: %d"% (i, reg1, reg2, reg3, reg4, reg5)) 
        reg1, reg2, reg3, reg4, reg5 = (reg2+reg5)%2, reg1, reg2, reg3, reg4
############  MSRG  ####################
    print("\nMSRG OUTPUT\n")
    reg1 = 1
    reg2 = 0
    reg3 = 0
    reg4 = 0
    reg5 = 0
    for i in range(31):
        print("ITERATION #%d - reg1: %d   reg2: %d   reg3: %d   reg4: %d   reg5: %d"% (i, reg1, reg2, reg3, reg4, reg5)) 
        reg1, reg2, reg3, reg4, reg5 = reg5, reg1, (reg5+reg2)%2, reg3, reg4   
