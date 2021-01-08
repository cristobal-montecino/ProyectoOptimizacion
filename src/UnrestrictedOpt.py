import numpy as np
DEBUG=0


def dist(p1, p2):
    return sum((p1-p2)**2)**0.5

def orthogonal(p):
    if (p==np.zeros(3)).all():
        raise ValueError("Error: No hay vector ortogonal a 0")
    if (p[0:2]==np.zeros(2)).all():
        return np.array([0, 0, 1])
    return np.array([p[1], -p[0], 0])/(p[0]**2+p[1]**2)**0.5

def gripper(inpt, tar):
    if DEBUG==1:
        print("GRIPPER\n")
        print("INPT: ", inpt, "\n")
        print("TAR: ", tar, "\n")
    if len(inpt)!=3:
        raise ValueError("Error: Gripper solo admite 3 nodos.")
    
    l1=dist(inpt[0], inpt[1])
    l2=dist(inpt[1], inpt[2])
    r=dist(inpt[0], tar)
    
    K=(l1**2+r**2-l2**2)/(2*l1*r)
    
    if DEBUG==1:
        print("L1: ", l1, "\n")
        print("L2: ", l2, "\n")
        print("r: ", r, "\n")
        print("K: ", K, "\n")
    
    direction=(tar-inpt[0])/dist(tar-inpt[0], np.zeros(3))
    
    inpt[2]=tar
    inpt[1]=inpt[0]+direction*K*l1+orthogonal(direction)*(1-K**2)**0.5*l1
    
    if DEBUG==1:
        print("DIRECTION: ", direction, "\n")
        print("ORTHOGONAL DIRECTION: ", orthogonal(direction), "\n")
        print("FINAL INPT: ", inpt, "\n")
        print("END GRIPPER\n")
    return inpt
    
def unrestricted(inpt, tar):
    if len(inpt)<3:
        raise ValueError("Error: Son necesarios mas de dos nodos!")
    
    for i in range(len(inpt)):
        if type(inpt[i])==type(list()):
            inpt[i]=np.array(inpt[i])
    
    if DEBUG:
        print("UNRESTRICTED\n")
        print("INITIAL INPT: ", inpt, "\n")
    
    if len(inpt)==3:
        if DEBUG==1:
            print("GRIPPED INPT: ", gripper(inpt, tar), "\n")
            print("FINAL GRIPPER\n")
        return gripper(inpt, tar)
    
    lengthList=list()
    for i in range(len(inpt)-1):
        lengthList.append(dist(inpt[i], inpt[i+1]))
    
    totalLength=sum(lengthList)
    
    if DEBUG==1:
        print("LENGTHLIST: ", lengthList, "\n")
        print("TOTALLENGTHLIST: ", totalLength, "\n")

    for i in range(1, len(lengthList)):
        if sum(lengthList[:i])>totalLength/2:
            if sum(lengthList[:i])-sum(lengthList[i:])>sum(lengthList[i-1:])-sum(lengthList[:i-1]):
                k=i
            else:
                k=i-1
            break
    
    inpt=[inpt[0]]+[inpt[0]+np.array([sum(lengthList[:i]), 0, 0]) for i in range(1, len(lengthList)+1)]
    
    if DEBUG==1:
        print("NORMALIZED INPT: ", inpt, "\n")
    
    grip=gripper([inpt[0], inpt[k], inpt[-1]], tar)
    
    if DEBUG==1:
        print("GRIPPED INPT: ", grip, "\n")
    
    for i in range(1, k):
        inpt[i]=inpt[0]+sum(lengthList[:i])/sum(lengthList[:k])*(grip[1]-grip[0])
    
    inpt[k]=grip[1]
    
    for i in range(k+1, len(inpt)):
        inpt[i]=grip[1]+sum(lengthList[k:i])/sum(lengthList[k:])*(grip[2]-grip[1])
    
    if DEBUG==1:
        print("FINAL INPT: ", inpt, "\n")
        print("FINAL UNRESTRICTED\n")
    
    return inpt