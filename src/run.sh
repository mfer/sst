#!/bin/bash
REP=$1
MU=$2
DATE="$(date +%s)"
cd baseline && ./configure && make && cd ../
touch /tmp/$DATE
for ((c=1; c <= REP ; c++)); do python deploy.py $MU >> /tmp/$DATE;	cd baseline && (cat ../input/workfile | ./efst | ./bb) >> /tmp/$DATE && cd ../; python smt.py >> /tmp/$DATE; python mst.py >> /tmp/$DATE; sleep 0; done
mkdir -p output/data
#printf "alg\ttotalLength\tbottleLength\tbottleLengthSST\tterm\tsteiner\ttimeSec\ttimeHour\n" > output/data/$DATE
grep -v '%' /tmp/$DATE >> output/data/$DATE
rm /tmp/$DATE
