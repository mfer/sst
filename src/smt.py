from utils import *
import time

def steiner_minimal_tree(g,k,FILE,PLOT):
    layout = Layout(zip(g.vs["x"], g.vs["y"]))
    weights = [distance(layout[edge.source], layout[edge.target]) for edge in g.es]
    if (g.clusters(mode="weak").size(0)==g.clusters(mode="weak").n):
        #print "Clustering with "+str(float(len(g.clusters(mode="weak").giant().vs))/g.clusters(mode="weak").n)\
        #    +"% of vertices in the giant cluster. There are "+str(len(g.clusters(mode="weak").sizes()))\
        #    +" clusters with sizes "+str(g.clusters(mode="weak").sizes())+"."
    #else:
        #print str(g.clusters(mode="weak").summary())+". Length: "+str(sum(weights))+". Bottleneck: "+str(max(weights))
        print "SMT\t"+str(sum(weights))+"\t"+str(max(weights)),

    for vertex in range(0,len(g.vs)):
        if(vertex >= len(g.vs)-steiner):
            g.vs[vertex]["color"]="blue"
        else:
            g.vs[vertex]["color"]="red"

    if PLOT:
        plot(g,FILE,edge_color="blue",vertex_size=5)


def read_graph(TERMS_FILE, STEINS_FILE):
    with open(TERMS_FILE) as f:
        terms = f.readlines()

    with open(STEINS_FILE) as f:
        steins = f.readlines()

    steiner=0
    for c in steins:
        l = c.split("\t")
        if len(l) == 2:
            steiner=steiner+1
        elif len(l) == 1:
            seconds_SMT = l[0].split("\n")[0]

    smt=Graph(len(terms)+steiner)
    #print str(len(terms)+steiner)+" "+str(len(terms))+" "+str(steiner)

    NODES=0
    for c in terms:
        l = c.split(" ")
        x = l[0]
        y = l[1].split("\n")[0]
        smt.vs[NODES]["id"]=NODES
        smt.vs[NODES]["x"]=float(x)
        smt.vs[NODES]["y"]=float(y)
        NODES=NODES+1

    for c in steins:
        l = c.split("\t")
        if len(l) == 2:
            l = c.split("\t")
            x = l[0]
            y = l[1].split("\n")[0]
            smt.vs[NODES]["id"]=NODES
            smt.vs[NODES]["x"]=float(x)
            smt.vs[NODES]["y"]=float(y)
            NODES=NODES+1


    #print NODES
    #for v in smt.vs:
    #    print str(v["id"])+" "+str(v["x"])+" "+str(v["y"])

    #for v in range(0,len(smt.vs)):
    #    print str(smt.vs[v]["id"])+" "+str(smt.vs[v]["x"])+" "+str(smt.vs[v]["y"])

    edges=0
    for c in steins:
        l = c.split("\t")
        if len(l) == 4:
            edges=edges+1
            l = c.split("\t")
            x1 = float(l[0])
            y1 = float(l[1])
            x2 = float(l[2])
            y2 = float(l[3].split("\n")[0])
            a=-1
            b=-1
            for v in range(0,len(smt.vs)):
                if smt.vs[v]["x"] == x1 and smt.vs[v]["y"] == y1:
                    a=v
                if smt.vs[v]["x"] == x2 and smt.vs[v]["y"] == y2:
                    b=v
            if (a>=0 and b>=0):
                smt.add_edges([(a,b)])
            else:
                v=0
                while v<len(smt.vs):
                    if smt.vs[v]["x"] == x1 and smt.vs[v]["y"] == y1:
                        a=v
                    v=v+1
                v=0
                while v<len(smt.vs):
                    if smt.vs[v]["x"] == x2 and smt.vs[v]["y"] == y2:
                        b=v
                    v=v+1
                if (a>=0 and b>=0):
                    smt.add_edges([(a,b)])
                else:
                    print >> sys.stderr, "error: problem to add edges."
                    print >> sys.stderr, "not finding "+str(x1)+" "+str(y1)+" or "+str(x2)+" "+str(y2)+" in "
                    for v in range(0,len(smt.vs)):
                        print >> sys.stderr, str(v)+" "+str(smt.vs[v]["x"])+" "+str(smt.vs[v]["y"])
                    sys.exit(1)


    #print edges
    return [smt, steiner, seconds_SMT]

###############################################################################
PWD=os.path.dirname(os.path.realpath(__file__))+"/"

DEPLOY_FILE=PWD+"input/deploy"
TERMS_FILE=PWD+"input/workfile"
STEINS_FILE=PWD+"input/steiner"

SMT_FILE=PWD+"output/smt"+str(time.time())+".png"
SMT_SST_FILE=PWD+"output/smt_sst"+str(time.time())+".png"

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

#READ_GRAPH#########################################################################################
rg=read_graph(TERMS_FILE,STEINS_FILE)
smt=rg[0]
steiner=rg[1]
seconds_SMT=float(rg[2])

#SMT################################################################################################
#b=time.time()
steiner_minimal_tree(smt,steiner,SMT_FILE,PLOT)
#e=time.time()
#print("\tsmt: b: "+str(b)+" e: "+str(e)+" e-b: "+str(e-b)+ " (e-b)/3600: "+str((e-b)/3600))

#SMT_SST############################################################################################
b=time.time()
print "\t"+steinerized_spanning_tree(smt, steiner,SMT_SST_FILE,PLOT),
print "\t"+str(len(smt.vs)-steiner)+"\t",
print str(steiner)+"\t",
e=time.time()
#print("\tsmt_sst: b: "+str(b)+" e: "+str(e)+" e-b: "+str(e-b)+ " (e-b)/3600: "+str((e-b)/3600))
print str(e-b+seconds_SMT)+"\t"+str((e-b+seconds_SMT)/3600)
