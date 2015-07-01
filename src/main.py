import numpy as np
import sys
import time
import random
import igraph
from igraph import *

def q(eps, mu):
    e=eps
    e1=1-eps
    e2=1-2*eps
    ee=2*eps
    m=mu
    mm=2*mu
    mmm=3*mu
    mmmm=4*mu
    a=e2**mmmm
    b=4*e2**mmm
    c=e1**m+ee**m
    d=2*e2**mm
    e=2*ee**mm + 2*e1**m*ee**mu - e1**mm
    f=2*e2**m
    g=e1**m*(2*ee**m - 3*ee**mm - e**m) + e1**mm*e**m - ee**mm
    h=e1**mm
    i=ee**mm+2*e**m -4*ee**m
    j=2*e1**m
    k=ee**mm - e**m
    return (a-b*c+d*e+f*g+h*i+j*k+1)

def ciw(mu):
    epsilon=0.001
    while q(epsilon,mu)<0.99 and epsilon<0.499:
        epsilon=epsilon+0.001
    return epsilon

def ctr(granularity,mu):
    if mu == 1:
        print >> sys.stderr, "error: MU should be greater than one."
        sys.exit(1)
    A=1
    term1=math.log(float(granularity**(A+0.5)))
    term2=math.log(float(mu-1))
    return (term1+term2)/mu

def save_points_in_file(g,FILE):
    f = open(FILE, 'w')
    for i in range(0,len(g.vs)):
        f.write(str(g.vs[i]["x"])+" "+str(g.vs[i]["y"])+"\n")

def distance(p1, p2):
    return ((p1[0]-p2[0]) ** 2 + (p1[1]-p2[1]) ** 2) ** 0.5

def on_vertical_line(g,v):
    if(g.vs[v]["x"]==round(g.vs[v]["x"])):
        return True
    else:
        return False

def triangular_visibility(g,v,u):
    if on_vertical_line(g,v):
        if on_vertical_line(g,u):
            return round(g.vs[v]["x"])==round(g.vs[u]["x"])
        else:
            if round(g.vs[v]["y"])==round(g.vs[u]["y"]):
                dv=abs(g.vs[v]["y"]-round(g.vs[v]["y"]))
            else:
                dv=abs(g.vs[v]["y"]-g.vs[u]["y"])
            du=abs(g.vs[u]["x"]-g.vs[v]["x"])
    else:
        if on_vertical_line(g,u):
            if round(g.vs[v]["x"])==round(g.vs[u]["x"]):
                dv=abs(g.vs[v]["x"]-round(g.vs[v]["x"]))
            else:
                dv=abs(g.vs[v]["x"]-g.vs[u]["x"])
            du=abs(g.vs[u]["y"]-g.vs[v]["y"])
        else:
            return round(g.vs[v]["y"])==round(g.vs[u]["y"])

    A = dv < EPSILON
    B = du < EPSILON
    C = dv < 2*EPSILON and du < 2*EPSILON
    return A or B or C

def lineofsight_visibility(g,v,u):
    return False

def visible(g,v,u):
    return triangular_visibility(g,v,u)

def dist(g,v,u):
    return ((g.vs[u]["x"]-g.vs[v]["x"]) ** 2 + (g.vs[u]["y"]-g.vs[v]["y"]) ** 2) ** 0.5

def addEdges(v,r,g):
    for u in range(v-1,0-1,-1):
        if( dist(g,v,u) < r ):
            if(visible(g,v,u)):
                g.add_edges([(u,v)])

def numpy_random(n):
    """Return a list of n random floats in the range [0, 1)."""
    return np.random.random((n)).tolist()

def numpy_randint(a, b, n):
    """Return a list of n random ints in the range [a, b]."""
    return np.random.randint(a, b, n).tolist()

def deploy_efficiently(g):
    #https://www.robertnitsch.de/notes/python/efficiently_generate_large_amounts_of_random_data
    continuous = numpy_random(NODES)
    discrete = numpy_randint(0, GRANULARITY, NODES)
    for n in range(0,NODES):
        if(random.uniform(0,1)>0.5):#point on horizontal line
            x=(GRANULARITY-1)*continuous[n]
            y=float(discrete[n])
            g.vs[n]["id"]=n
            g.vs[n]["x"]=x
            g.vs[n]["y"]=y
            addEdges(n,R,g)
        else:#point on vertical line
            x=float(discrete[n])
            y=(GRANULARITY-1)*continuous[n]
            g.vs[n]["id"]=n
            g.vs[n]["x"]=x
            g.vs[n]["y"]=y
            addEdges(n,R,g)


def deploy_criptographically(g):
    for n in range(0,NODES):
        if(random.uniform(0, 1)>0.5):#point on horizontal line
            x=random.uniform(0, GRANULARITY-1)
            y=float(round(random.uniform(0, GRANULARITY-1)))
            g.vs[n]["id"]=n
            g.vs[n]["x"]=x
            g.vs[n]["y"]=y
            addEdges(n,R,g)
        else:#point on vertical line
            x=float(round(random.uniform(0, GRANULARITY-1)))
            y=random.uniform(0, GRANULARITY-1)
            g.vs[n]["id"]=n
            g.vs[n]["x"]=x
            g.vs[n]["y"]=y
            addEdges(n,R,g)

def deploy(g):
    deploy_criptographically(g)
    #deploy_efficiently(g)
    plot(g,G_FILE,vertex_size=5)


###############################################################################


PWD="/home/manassesferreira/sst/"
TERMS_FILE=PWD+"input/workfile"
STEINS_FILE=PWD+"input/steiner"
SST_FILE=PWD+"output/sst.png"
G_FILE=PWD+"output/g.png"
MST_FILE=PWD+"output/mst.png"

GRANULARITY=2
SEGMENTS=GRANULARITY*(GRANULARITY-1)*2
INTERSECTS=GRANULARITY*GRANULARITY

MU=10 #greater than one, should be
NODES=SEGMENTS*MU

EPSILON=ciw(MU)/1.0 #smaler than half, should be

minR=2*math.sqrt(2)*EPSILON
R=3*(ciw(MU)/EPSILON)*minR
#R=ctr(GRANULARITY,MU)/1.0

g=Graph(NODES)

#DEPLOY#############################################################################################
b=time.time()
deploy(g)
e=time.time()
print("dep: b: "+str(b)+" e: "+str(e)+" e-b: "+str(e-b)+ " (e-b)/3600: "+str((e-b)/3600))
save_points_in_file(g, TERMS_FILE)
