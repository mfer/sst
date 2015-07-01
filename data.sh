#!/bin/bash
printf "alg\ttotalLength\tbottleLength\tbottleLengthSST\tterm\tsteiner\ttimeSec\ttimeHour\n" > data.data
cd run
MUS="$(ls -1)"
PWD="$(pwd)"

for MU in `echo $MUS`
do
  DIR=$PWD$MU"/output/data/"
  if [ -d "DIR" ]; then
    echo $DIR
  else
    RUNS="$(ls -1 $MU/output/data/)"
    for RUN in `echo $RUNS`
    do
      cat $MU/output/data/$RUN >> ../data.data
    done
  fi
done
cd ..
