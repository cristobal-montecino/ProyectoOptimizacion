from pinkind import pinkind
from Fabrik import fabrik
from direk import direk

from random import random
from time import sleep, time
import numpy as np
def dist(a, b):
    return ((a[0]-b[0])**2+(a[1]-b[1])**2+(a[2]-b[2])**2)**0.5

def error(points, lengths):
    sum=0
    for i in range(1, len(points)):
        sum=sum+(dist(points[i], points[i-1])-lengths[i-1])**2
    return sum
    
TOLERANCE=10**-1
RADIUS=1
NUMBER=10000
TARGETMODIFIER=1


lengths=np.array([(RADIUS*random()+0.5) for i in range(NUMBER)])

points=[[0, 0, 0]]*(len(lengths))
for i in range(1, len(points)):
    points[i][0]=points[i-1][0]+lengths[i-1]

target=[(random()-0.5)*2*RADIUS*NUMBER*TARGETMODIFIER, (random()-0.5)*2*RADIUS*NUMBER*TARGETMODIFIER, (random()-0.5)*2*RADIUS*NUMBER*TARGETMODIFIER]

t0=time()
sleep(1)
dirPoints=np.array(direk(points, target, lengths, scalar_epsilon=10**(-1), vector3_epsilon=10**(-1)))
sleep(1)
t1=time()
sleep(1)
fabrikPoints=np.array(fabrik(points, target, lengths, 10**(-12)))
sleep(1)
t2=time()
sleep(1)
pinkPoints=np.array(pinkind(lengths, [0, 0, 0], target))
sleep(1)
t3=time()

timeDirek=(t1-t0-2)*1000
timeFabrik=(t2-t1-2)*1000
timePinkind=(t3-t2-2)*1000

print(timeFabrik)
print(timePinkind)
print(timeDirek)
distFabrik=error(fabrikPoints, lengths)
distPink=error(pinkPoints, lengths)
distDir=error(dirPoints, lengths)
print(distFabrik)
print(distPink)
print(distDir)
print(pinkPoints[-1], " vs ", target)