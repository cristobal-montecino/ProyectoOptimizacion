#FABRIK Implementation
#Well work with lists of coordinates.
import matplotlib.pyplot as plt
CONSTRAINT=100000
DEBUG=0

#2 Norm
def dist(p1, p2):
    return sum([(p1[i]-p2[i])**2 for i in range(3)])**0.5

#Linear adjust of Fabrik
def linearAdjust(p1, p2, l):
    if DEBUG:
        print("linAdj p1: ", p1)
        print("linAdj p2: ", p2)
        print("linAdj l: ", l)
    
    if DEBUG:
        print("linAdj rtrn: ", [p2[i]+(p1[i]-p2[i])*(dist(p1, p2)-l)/dist(p1, p2) for i in range(3)])
        
    return [p2[i]+(p1[i]-p2[i])*(dist(p1, p2)-l)/dist(p1, p2) for i in range(3)]

#Fabrik loop
def fabrik_iterate(inpt, tar, lengthList):
    if DEBUG:
        print("iterPre: ", inpt)
        print("tar: ", tar)
    inpt[-1]=tar
    for i in range(len(inpt)-1):
        if DEBUG:
            print("p1 to linAdj: ", inpt[-i-1],"\np2 to linAdj: ",  inpt[-i-2])
        inpt[-i-2]=linearAdjust(inpt[-i-1], inpt[-i-2], lengthList[-i-1])
    inpt[0]=[0, 0, 0]
    if DEBUG:
        print("iterBTW: ", inpt)
    for i in range(len(inpt)-1):
        inpt[i+1]=linearAdjust(inpt[i], inpt[i+1], lengthList[i])
    if DEBUG:
        print("iterPost: ", inpt)
    return inpt

#Fabrik proper
def fabrik(inpt, tar, lengths, tol):
    if len(inpt)<2:
        raise ValueError("Error: El actuador no tiene suficientes nodos!")
    
    elif tol<=0:
        raise ValueError("Error: La tolerancia debe ser un valor positivo!")
    
    lengthList = lengths
    if sum(lengthList)<dist(tar, inpt[0]):
        return [inpt[0]]+[linearAdjust(tar, inpt[0], sum(lengths[:i])) for i in range(1, len(lengths))]
    j=0
    while dist(inpt[-1], tar)>tol:
        if DEBUG:
            print("iter: ", inpt)
        inpt=fabrik_iterate(inpt, tar, lengthList)
        j=j+1
        if j>CONSTRAINT:
            raise RuntimeError("Error: demasiadas iteraciones sin alcanzar la tolerancia!")
    return inpt
