#!/bin/bash
export THENEMIN_ROOT="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )" 
export SC_SYNTHDEF_PATH=$THENEMIN_ROOT/synthdefs
jackd -R -P99 -dalsa -dhw:0 -r44100 -p512 -n4 &
sleep 2
scsynth -u 57110 &
sleep 2
jack_connect SuperCollider:out_1 system:playback_1 &
jack_connect SuperCollider:out_2 system:playback_2 &
sleep 0.5
python $THENEMIN_ROOT/thenemin.py 

