#!/bin/bash
# run as in: ./run_deepire(blabla).sh exectuable(starting ./) problem "extra options" folder(preferably on /local/...)
# the folder must exists (that's the job of run_in_parallel "above" us)
export LD_LIBRARY_PATH=/home/sudamar2/projects/vampire/libtorch/lib/
# for deepire, we currently pick discount(awr 5), as LRS is in general broken
timelimit -t 510 -T 10 $1 -m 90000 -p off --input_syntax smtlib2 -stat full -tstat on -t 500 $2 $3 > "$4"/`(./filenamify_path.sh $2)`.log 2>&1
