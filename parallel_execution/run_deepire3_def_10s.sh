#!/bin/bash
# run as in: ./run_deepire(blabla).sh exectuable(starting ./) problem "extra options" folder(preferably on /local/...)
# the folder must exists (that's the job of run_in_parallel "above" us)
export LD_LIBRARY_PATH=/home/sudamar2/projects/vampire/libtorch/lib/
# 10s runs are OK with running avatar and discout. We simply run the default strategy (as in our CADE20 paper)
timelimit -t 11 -T 1 $1 -m 90000 -p off --input_syntax smtlib2 -stat full -tstat on -t 10 "$2" $3 > "$4"/`(./filenamify_path.sh "$2")`.log 2>&1
