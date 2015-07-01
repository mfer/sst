import numpy as np
from igraph import *
import sys
import time
import random

def steinerized_spanning_tree(g, k, FILE, PLOT):
    layout = Layout(zip(g.vs["x"], g.vs["y"]))
    weights = [distance(layout[edge.source], layout[edge.target]) for edge in g.es]
    sst = g.spanning_tree(weights)

    layout = Layout(zip(sst.vs["x"], sst.vs["y"]))
    weights = [distance(layout[edge.source], layout[edge.target]) for edge in sst.es]

    Points = [[] for i in range(len(sst.es))]
    points_in = [0 for i in range(len(sst.es))]
    lengths = [weights[i] for i in range(len(sst.es))]
    v_left = [0 for i in range(len(sst.es))]
    v_right = [0 for i in range(len(sst.es))]

    for s in range(len(sst.vs), len(sst.vs)+k):
        e = [i for i, j in enumerate(lengths) if j == max(lengths)][0]
        v_left[e]=sst.get_edgelist()[e][0]
        v_right[e]=sst.get_edgelist()[e][1]
        Points[e].append(s)
        points_in[e]=points_in[e]+1
        lengths[e]=weights[e]/(points_in[e]+1)
        #print str(s)+" "+str(e)+" "+str(lengths[e])

    #print Points
    #print points_in

    #print sst

    sst.add_vertices(k)
    for e in range(len(sst.es)):
        if points_in[e]>0:
            u=v_left[e]
            v=v_right[e]
            sinal=1
            if g.vs[u]["x"] > g.vs[v]["x"]:
                v=v_left[e]
                u=v_right[e]
            if g.vs[u]["y"] > g.vs[v]["y"]:
                sinal=-1

            dx=abs(g.vs[u]["x"]-g.vs[v]["x"])/(points_in[e]+1)
            dy=abs(g.vs[u]["y"]-g.vs[v]["y"])/(points_in[e]+1)
            #minx=min(g.vs[u]["x"],g.vs[v]["x"])
            #miny=min(g.vs[u]["y"],g.vs[v]["y"])
            #i=1
            last=u
            for s in Points[e]:
                sst.add_edges([(last,s)])
                sst.vs[s]['x']=sst.vs[last]['x']+dx
                sst.vs[s]['y']=sst.vs[last]['y']+sinal*dy
                last=s

            #print str(e)+": "+str([(last,v)])
            sst.add_edges([(last,v)])
            sst.delete_edges([(u,v)])

    #print sst
    layout = Layout(zip(sst.vs["x"], sst.vs["y"]))
    sst_weights = [distance(layout[edge.source], layout[edge.target]) for edge in sst.es]
    #if (sst.clusters(mode="weak").size(0)!=sst.clusters(mode="weak").n):
    #    print "Clustering with "+str(float(len(sst.clusters(mode="weak").giant().vs))/sst.clusters(mode="weak").n)\
    #        +"% of vertices in the giant cluster. There are "+str(len(sst.clusters(mode="weak").sizes()))\
    #        +" clusters with sizes "+str(sst.clusters(mode="weak").sizes())+"."
    #else:
    #    print str(sst.clusters(mode="weak").summary())+". Length: "+str(sum(sst_weights))+". Bottleneck: "+str(max(sst_weights))


    if PLOT:
        for vertex in range(0,len(sst.vs)):
            if(vertex >= len(g.vs)):
                sst.vs[vertex]["color"]="blue"
            else:
                sst.vs[vertex]["color"]="red"

        plot(sst,FILE,vertex_size=5)

    return str(max(sst_weights))

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

def triangular_visibility(g,v,u,EPSILON):
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

def visible(g,v,u,EPSILON):
    return triangular_visibility(g,v,u,EPSILON)

def dist(g,v,u):
    return ((g.vs[u]["x"]-g.vs[v]["x"]) ** 2 + (g.vs[u]["y"]-g.vs[v]["y"]) ** 2) ** 0.5

def addEdges(v,r,g,EPSILON):
    for u in range(v-1,0-1,-1):
        if( dist(g,v,u) < r ):
            if(visible(g,v,u,EPSILON)):
                g.add_edges([(u,v)])

def numpy_random(n):
    """Return a list of n random floats in the range [0, 1)."""
    return np.random.random((n)).tolist()

def numpy_randint(a, b, n):
    """Return a list of n random ints in the range [a, b]."""
    return np.random.randint(a, b, n).tolist()

def deploy_efficiently(GRANULARITY,NODES,R):
    #https://www.robertnitsch.de/notes/python/efficiently_generate_large_amounts_of_random_data
    g=Graph(NODES)
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
    return g

def deploy_criptographically(GRANULARITY,EPSILON,NODES,R):
    g=Graph(NODES)
    for n in range(0,NODES):
        if(random.uniform(0, 1)>0.5):#point on horizontal line
            x=random.uniform(0, GRANULARITY-1)
            y=float(round(random.uniform(0, GRANULARITY-1)))
            g.vs[n]["id"]=n
            g.vs[n]["x"]=x
            g.vs[n]["y"]=y
            addEdges(n,R,g,EPSILON)
        else:#point on vertical line
            x=float(round(random.uniform(0, GRANULARITY-1)))
            y=random.uniform(0, GRANULARITY-1)
            g.vs[n]["id"]=n
            g.vs[n]["x"]=x
            g.vs[n]["y"]=y
            addEdges(n,R,g,EPSILON)
    return g

def deploy_freely(NODES,R):
    g = Graph.GRG(NODES, R)
    return g

def deploy(GRANULARITY,EPSILON,NODES,R,G_FILE,PLOT):
    #g=deploy_criptographically(GRANULARITY,EPSILON,NODES,R)
    #g=deploy_efficiently(GRANULARITY,NODES,R)
    g=deploy_freely(NODES,R)
    if PLOT:
        plot(g,G_FILE,vertex_size=5)
    return g
