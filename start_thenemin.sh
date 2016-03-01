#!/bin/sh
export THENEMIN_ROOT="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )" && 
jackd -R -P99 -dalsa -dhw:0 -r44100 -p512 -n4 &
sleep 4
scsynth -u 57110 &
sleep 4
jack_connect SuperCollider:out_1 system:playback_1 &
jack_connect SuperCollider:out_2 system:playback_2 &
sleep 1
./thenemin.py 

