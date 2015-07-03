#!/bin/bash
REP=10
MUS="16 8 4 2"

mkdir -p src/input
mkdir -p src/output

for MU in `echo $MUS`
do
  mkdir -p run/$MU
  cp -R src/* run/$MU
  cd run/$MU
  ./run.sh $REP $MU > /dev/null 2>&1 &
  cd ../../
  sleep 10
done

clear
echo "simulation is running. wait."
