#!/bin/bash
# run as in: ./run_in_parallel.sh 50 smt4vamp.txt ./run_vampire_generic.sh ./vampire_rel_detached_4195 "-ttq on -ynr 3:1 -aut 0.9" vampire_ari_ttq2.1_aut0.9
mkdir -p $6
cat $2 | parallel -I% --max-args 1 -P $1 $3 $4 % \"$5\" $6
