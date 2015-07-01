import numpy as np
import sys
import time
import random
import igraph
from igraph import *
from utils import *

def minimum_spanning_tree(g, PLOT):
    layout = Layout(zip(g.vs["x"], g.vs["y"]))
    weights = [distance(layout[edge.source], layout[edge.target]) for edge in g.es]
    mst = g.spanning_tree(weights)
    layout = Layout(zip(mst.vs["x"], mst.vs["y"]))
    mst_weights = [distance(layout[edge.source], layout[edge.target]) for edge in mst.es]
    #checking if it is a unique or forest spanning
    if (mst.clusters(mode="weak").size(0)==mst.clusters(mode="weak").n):
    #    print "Clustering with "+str(float(len(mst.clusters(mode="weak").giant().vs))/mst.clusters(mode="weak").n)\
    #        +"% of vertices in the giant cluster. There are "+str(len(mst.clusters(mode="weak").sizes()))\
    #        +" clusters with sizes "+str(mst.clusters(mode="weak").sizes())+"."
    #else:
        #print str(mst.clusters(mode="weak").summary())+". Length: "+str(sum(mst_weights))+". Bottleneck: "+str(max(mst_weights))
        print "MST\t"+str(sum(mst_weights))+"\t"+str(max(mst_weights)),

    if PLOT:
        plot(mst,MST_FILE,edge_color="blue",vertex_size=5)

def read_graph(TERMS_FILE):
    with open(TERMS_FILE) as f:
        content = f.readlines()

    g=Graph(len(content))

    NODES=0
    for c in content:
        l = c.split(" ")
        x = l[0]
        y = l[1].split("\n")[0]
        g.vs[NODES]["id"]=NODES
        g.vs[NODES]["x"]=float(x)
        g.vs[NODES]["y"]=float(y)
        def addEdgesL(v,r,g):
            for u in range(v-1,0-1,-1):
                if( dist(g,v,u) < r ):
                    g.add_edges([(u,v)])
        deployFree=True
        if(deployFree):
            addEdgesL(NODES,R,g)
        else:
            addEdges(NODES,R,g, EPSILON)
        NODES=NODES+1

    with open(STEINS_FILE) as f:
        steins = f.readlines()

    steiner=0
    for c in steins:
        l = c.split("\t")
        if len(l) == 2:
            steiner=steiner+1


    return [g, steiner]

###############################################################################
PWD=os.path.dirname(os.path.realpath(__file__))+"/"

DEPLOY_FILE=PWD+"input/deploy"
TERMS_FILE=PWD+"input/workfile"
STEINS_FILE=PWD+"input/steiner"

MST_FILE=PWD+"output/mst.png"
MST_SST_FILE=PWD+"output/mst_sst.png"

#READ_PARAMETERS###########################################################################################
with open(DEPLOY_FILE) as f:
    content = f.readlines()

GRANULARITY=int(content[0])
SEGMENTS=GRANULARITY*(GRANULARITY-1)*2
INTERSECTS=GRANULARITY*GRANULARITY

MU=int(content[3]) #greater than one, should be
NODES=SEGMENTS*MU

EPSILON=float(content[1])#ciw(MU)/1.0 #smaler than half, should be

#minR=2*math.sqrt(2)*EPSILON
#R=3*(ciw(MU)/EPSILON)*minR
#R=ctr(GRANULARITY,MU)/1.0
R=float(content[2])

PLOT=False

#READ_TERMS###########################################################################################
rg=read_graph(TERMS_FILE)
g=rg[0]
steiner=rg[1]

#MST################################################################################################
b=time.time()
minimum_spanning_tree(g, PLOT)
#e=time.time()
#print("\tmst: b: "+str(b)+" e: "+str(e)+" e-b: "+str(e-b)+ " (e-b)/3600: "+str((e-b)/3600))

#MST_SST############################################################################################
#b=time.time()
print "\t"+steinerized_spanning_tree(g, steiner, MST_SST_FILE, PLOT),
print "\t"+str(len(g.vs))+"\t",
print str(steiner)+"\t",
e=time.time()
#print("\tmst_sst: b: "+str(b)+" e: "+str(e)+" e-b: "+str(e-b)+ " (e-b)/3600: "+str((e-b)/3600))
print str(e-b)+"\t"+str((e-b)/3600)
