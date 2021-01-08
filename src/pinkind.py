import numpy as np

def rotation_matrix(axis, theta):
    axis = axis / np.linalg.norm(axis)
    a = np.cos(theta / 2.0)
    b, c, d = -axis * np.sin(theta / 2.0)
    return np.array([[a*a + b*b - c*c - d*d, 2 * (b*c + a*d), 2 * (b*d - a*c)],
                     [2 * (b*c - a*d), a*a + c*c - b*b - d*d, 2 * (c*d + a*b)],
                     [2 * (b*d + a*c), 2 * (c*d - a*b), a*a + d*d - b*b - c*c]])

def pinkind(lengths, orig, end):
    endpoint=np.array(end)-np.array(orig)
    endpointValue=np.linalg.norm(endpoint)
    solution=core(lengths, endpointValue)
    solution=np.concatenate([solution, np.zeros((len(solution), 1))], axis=1)
    
    if endpoint[0]!=0 or endpoint[2]!=0:
        rotation=rotation_matrix(np.cross(np.array([0.0, 1.0, 0.0]), endpoint), np.arccos(np.dot(np.array([0.0, 1.0, 0.0]), endpoint/endpointValue)))
        solution=solution.dot(rotation.transpose())+orig
    elif endpoint[1]<0:
        solution=-solution+orig
    return solution
    

def core(lengths, endpoint):
    totalLength=sum(lengths)
    partialSum=0
    i=-1
    if len(lengths)>2:
        while partialSum<totalLength/2:
            i=i+1
            partialSum=partialSum+lengths[i]
        converseSum=totalLength-partialSum
    else:
        l1=lengths[0]
        l2=lengths[1]
        return solve(np.array([[0, 0], [0, l1]]), np.array([[0, l2]]), endpoint)
    
    
    leftLeg=np.zeros((len(lengths)-i-1, 2))
    leftLeg[0][1]=lengths[i+1]
    for j in range(1, len(lengths)-i-1):
        leftLeg[j][1]=leftLeg[j-1][1]+lengths[i+1+j]
    
    if partialSum-converseSum>endpoint:
        print("ping")
        rightLeg=core(lengths[:i+1], leftLeg[-1][1])
    else:
        rightLeg=np.zeros((i+2, 2))
        rightLeg[0][1]=0
        for j in range(i+1):
            rightLeg[j+1][1]=rightLeg[j][1]+lengths[j]
    
    return solve(rightLeg, leftLeg, endpoint)

def solve(rightLeg, leftLeg, endpoint):
    l1=rightLeg[-1][1]
    l2=leftLeg[-1][1]
    
    if endpoint<=l1-l2:
        return np.concatenate([rightLeg, -leftLeg+np.array([0.0, l1])])
    
    elif endpoint<=l2-l1:
        return np.concatenate([-rightLeg, leftLeg-np.array([0.0, l1])])
    
    elif l1+l2<endpoint:
        return np.concatenate([rightLeg, leftLeg+np.array([0.0, l1])])
    
    y=(endpoint**2+l1**2-l2**2)/(2*endpoint)
    x=(l1**2-y**2)**0.5
    
    c=y/l1
    s=-x/l1
    rotationMatrix1=np.array([[c, -s], [s, c]])
    
    c=(endpoint-y)/l2
    s=x/l2
    rotationMatrix2=np.array([[c, -s], [s, c]])
    
    return np.concatenate([rightLeg.dot(rotationMatrix1.transpose()), leftLeg.dot(rotationMatrix2.transpose())+np.array([x, y])])