from utils import *
import sys

PWD=os.path.dirname(os.path.realpath(__file__))+"/"
DEPLOY_FILE=PWD+"input/deploy"
TERMS_FILE=PWD+"input/workfile"
STEINS_FILE=PWD+"input/steiner"
G_FILE=PWD+"output/g.png"

GRANULARITY=2 #greater than one, should be
SEGMENTS=GRANULARITY*(GRANULARITY-1)*2
INTERSECTS=GRANULARITY*GRANULARITY

if len(sys.argv)==1:
    MU=10 #greater than one, should be
else:
    MU=int(sys.argv[1])

NODES=SEGMENTS*MU

EPSILON=ciw(MU)/5.0 #smaler than half, should be

###################
#minR=2*math.sqrt(2)*EPSILON
#R=3*(ciw(MU)/EPSILON)*minR
###################
#R=ctr(GRANULARITY,MU)*1.0/1.0
###################
R=2**(1/2)

PLOT=False

#DEPLOY#############################################################################################
b=time.time()
g=deploy(GRANULARITY,EPSILON,NODES,R,G_FILE,PLOT)
e=time.time()
#print("\tdep: b: "+str(b)+" e: "+str(e)+" e-b: "+str(e-b)+ " (e-b)/3600: "+str((e-b)/3600))
save_points_in_file(g, TERMS_FILE)
f = open(DEPLOY_FILE, 'w')
f.write(str(GRANULARITY)+"\n")
f.write(str(EPSILON)+"\n")
f.write(str(R)+"\n")
f.write(str(MU)+"\n")
