# En desarrollo

def dist(p1, p2):
    return sum([(p1[i]-p2[i])**2 for i in range(3)])**0.5

def unrestricted(inpt, tar):
    if len(inpt)<3:
        raise ValueError("Error: Son necesarios mas de dos nodos!")
    lengthList=list()
    for i in range(len(inpt)-1):
        lengthList.append(dist(inpt[i], inpt[i+1]))
    totalLength=sum(lengthList)
    for i in range(len(lengthList)):
        if sum(lengthList[:i])>totalLength/2:
            if sum(lengthList[:i])-sum(lengthList[i:])>sum(lengthList[i-1:])-sum(lengthList[:i-1]):
                k=i
            else:
                k=i-1
            break
    l1=sum(lengthList[:k])
    l2=sum(lengthList[k:])
    D=dist(tar, [0, 0, 0])
    z=(l1**2-l2**2+D**2)/2
    r=(l1**2-z**2)**0.5
    if tar[2]==0:
        P=[0, 0, r]
    else:
        R=[1, 1, (-tar[0]-tar[1])/tar[2]]
        P=[R[q]*r/dist(R, 0) for q in range(3)]
    Q=[tar[i]*z for i in range(3)]
    N=[Q[i]+P[i] for i in range(3)]
    inpt[k+1]=N
    print(N)
    for i in range(len(inpt)-1):
        if i+1<k:
            inpt[i+1]=[N[j]*sum(lengthList[:i])/dist(N, 0)]
        elif i+1>k:
            inpt[i+1]=[N[j]+(sum(lengthList[k+1:i+1])*(tar[j]-N[j])) for j in range(3)]
    return inpt
    
print(unrestricted([[0, 0, 0], [1, 0, 0], [3, 0, 0], [4, 0, 0]], [0, 2,0]))