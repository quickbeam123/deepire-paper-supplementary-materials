# deepire-paper-supplementary-materials
Supplementary files accompanying the paper New Techniques that Improve ENIGMA-style Clause Selection Guidance (M. Suda) submitted to CADE2021

1) The list of SMT-LIB files used in our experiments can be found in
selectedSMTLIBproblems.txt

2) The used version of vampire can be found at
vampire branch: https://github.com/vprover/vampire/tree/deepire3
commit: https://github.com/vprover/vampire/commit/110f414207d632819dea4cf01a1ddaca86d0cca3

3) To compile vampire, libtorch from
https://download.pytorch.org/libtorch/cu102/libtorch-shared-with-deps-1.6.0.zip
should be unzipped under vampire/
If needed, please update the respective paths in vampire/Makefile accordingly.
Then run
make vampire_rel
to produce
vampire_rel_deepire3_4869

4) The baseline vampire strategy was "-sa discount -awr 10:1"

5) We used a set of shell scripts for parallel execution on the benchmark problems, namely, the these are the files
filenamify_path.sh
run_deepire3_def_10s.sh
run_deepire3_def_500s.sh
run_in_parallel_plus.sh
to be found under parallel_execution

6) The first run, to evaluate S, was executed using
./run_in_parallel_plus.sh 30 selectedSMTLIBproblems.txt ./run_deepire3_def_10s.sh ./vampire_rel_deepire3_4869 "-sa discount -awr 10:1" existing_dir_to_save_results_to/smtlib_deepire3_d4869_10s_base

7) To make vampire_deepire output logs to train from, an option "-s4k on" was added and a larger time limit was imposed, since printing out the logs take extra time. Nevertheless, only logs for the problems solved at 6) were generated.
./run_in_parallel_plus.sh 30 base.solved.txt ./run_deepire3_def_500s.sh ./vampire_rel_deepire3_4869 "-sa discount -awr 10:1 -s4k on" existing_dir_to_save_results_to/smtlib_deepire3_d4869_10s_base_s4k-on

8) The training was done with a set of python scripts made publicly available via
https://github.com/quickbeam123/deepire3.1
commit: https://github.com/quickbeam123/deepire3.1/commit/e843221ac18214bad282e89f45a7d43908c6c929

9) The vampire run logs were first read by a log_loader script:
./log_loader.py loop0dis10s_10 loop0dis10s_10/logs.txt
where logs.txt contained a line-by-line listing to access the files obtained in 7)

this left loop0dis10s_10 with files
raw_log_data_avF_thaxAxiomNames.pt
data_sign.pt

storing all the necessary info to continue the pipeline.

10) Next, a compressor script was used to compress the problem logs along the abstraction and group some runs to approximately match the 1000 nodes per minibatch size.

./compressor.py loop0dis10s_10/compressed/ loop0dis10s_10/raw_log_data_avF_thaxAxiomNames.pt loop0dis10s_10/data_sign.pt

11) The training was performed by calling

mkdir training
./multi_inf_parallel_files_continuous.py loop0dis10s_10/compressed/ training

12) the model M to be used later in vampire was extracted as in:

./exporter.py loop0dis10s_10/compressed/data_sign.pt training/check-epoch45.pt loop1_i45.pt

The obtained model M can be found under in this repo as the file:
models/loop1_run40_i45_newExport.pt
(the file models/loop1_run40_i45_l720_p863_n816.pt is a version of the model which does not do caching of embeddings dusing evaluation)

13) To run and evaluate vampire under the guidance of a specific model, we executed commands like:

./run_in_parallel_plus.sh 30 selectedSMTLIBproblems.txt ./run_deepire3_def_10s.sh ./vampire_rel_deepire3_4869 "-sa discount -awr 10:1 -e4k ../models/loop1_run40_i45_newExport.pt -nesq on -nesqr 2,1 -nesqc 0.25" existing_dir_to_save_results_to/smt4vamp_deepire3_d4869_10s_dis10.1_model_loop1_run40_i45_newExport_nesqr-2.1_nesqc-0.25

here: "-e4k" tells vampire where to look for a model to use; "-nesqr 2,1" triggeres layered selection using the model for guidance and with a second level ratio 2:1 (this is actually 1:2 in the paper), and "-nesqc" specifies the cutoff value to use, "0.25" is actually "-0.25" in the paper

14) Finally, to fetch and collect the results from the directories filled up with vampire's run logs, such as "existing_dir_to_save_results_to/smt4vamp_deepire3_d4869_10s_dis10.1_model_loop1_run40_i45_newExport_nesqr-2.1_nesqc-0.25", we used the following two scripts

scripts/scan_and_store_neurspeed.py
scripts/analyze_results_loops.py

./scan_and_store_neurspeed.py selectedSMTLIBproblems.txt existing_dir_to_save_results_to/smt4vamp_deepire3_d4869_10s_dis10.1_model_loop1_run40_i45_newExport_nesqr-2.1_nesqc-0.25
...
...
saving to smt4vamp_deepire3_d4869_10s_dis10.1_model_loop1_run40_i45_newExport_nesqr-2.1_nesqc-0.25.pkl
Eval time on average 31.344747765 percent

and finally:

./analyze_results_loops.py *.pkl

obtaining an output such as:

Absolute ranking:
l0and1/smt4vamp_deepire3_d4869_10s_dis10.1_model_loop1_run40_i45_newExport_nesqr-2.1_nesqc-0.25.pkl 1066 0
l0and1/smt4vamp_deepire3_d4869_10s_dis10.1_model_loop1_run40_i95ne_nesqr-2.1.pkl 988 -78
l0and1/smt4vamp_deepire3_d4869_10s_dis10.1_model_loop1_run40_i45_newExport_nesqr-2.1_nesqc--0.25.pkl 945 -121
l0and1/smt4vamp_deepire3_d4869_10s_dis10.1_model_loop1_run40_i45_newExport_nesqr-20.1.pkl 919 -147
l0and1/smt4vamp_deepire3_d4869_10s_dis10.1_model_loop1_run40_i65ne_nesqr-2.1.pkl 895 -171
l0and1/smt4vamp_deepire3_d4869_10s_dis10.1_model_loop1_run40_i45_newExport_nesqr-10.1_nesqc-2.0.pkl 886 -180
l0and1/smt4vamp_deepire3_d4869_10s_dis10.1_model_loop1_run40_i35ne_nesqr-10.1.pkl 875 -191
l0and1/air03_smt4vamp_deepire3_d4869lrsSave_10s_loop0_dis10.1.pkl 734 -332
l0and1/smt4vamp_deepire3_d4869_10s_dis10.1_model_loop1_run40_i15ne_nesqr-2.1.pkl 720 -346

By loops:
l0and1/air03_smt4vamp_deepire3_d4869lrsSave_10s_loop0_dis10.1.pkl 734 100.0 734 0
Loop 0 734 100.0 added 734 still missing 0 accum 734
l0and1/smt4vamp_deepire3_d4869_10s_dis10.1_model_loop1_run40_i45_newExport_nesqr-2.1_nesqc-0.25.pkl 1066 145.231607629 439 107
l0and1/smt4vamp_deepire3_d4869_10s_dis10.1_model_loop1_run40_i45_newExport_nesqr-20.1.pkl 919 125.204359673 387 202
l0and1/smt4vamp_deepire3_d4869_10s_dis10.1_model_loop1_run40_i45_newExport_nesqr-2.1_nesqc--0.25.pkl 945 128.746594005 375 164
l0and1/smt4vamp_deepire3_d4869_10s_dis10.1_model_loop1_run40_i95ne_nesqr-2.1.pkl 988 134.604904632 372 118
l0and1/smt4vamp_deepire3_d4869_10s_dis10.1_model_loop1_run40_i35ne_nesqr-10.1.pkl 875 119.209809264 328 187
l0and1/smt4vamp_deepire3_d4869_10s_dis10.1_model_loop1_run40_i65ne_nesqr-2.1.pkl 895 121.934604905 313 152
l0and1/smt4vamp_deepire3_d4869_10s_dis10.1_model_loop1_run40_i45_newExport_nesqr-10.1_nesqc-2.0.pkl 886 120.708446866 244 92
l0and1/smt4vamp_deepire3_d4869_10s_dis10.1_model_loop1_run40_i15ne_nesqr-2.1.pkl 720 98.0926430518 223 237
Loop 1 1506 205.177111717 added 794 still missing 22 accum 1528

Greedy cover:
l0and1/smt4vamp_deepire3_d4869_10s_dis10.1_model_loop1_run40_i45_newExport_nesqr-2.1_nesqc-0.25.pkl contributes 1066 total 1066 not known 1066 uniques 28
l0and1/smt4vamp_deepire3_d4869_10s_dis10.1_model_loop1_run40_i95ne_nesqr-2.1.pkl contributes 190 total 988 not known 988 uniques 38
l0and1/smt4vamp_deepire3_d4869_10s_dis10.1_model_loop1_run40_i35ne_nesqr-10.1.pkl contributes 85 total 875 not known 875 uniques 18
l0and1/smt4vamp_deepire3_d4869_10s_dis10.1_model_loop1_run40_i45_newExport_nesqr-10.1_nesqc-2.0.pkl contributes 48 total 886 not known 886 uniques 30
l0and1/smt4vamp_deepire3_d4869_10s_dis10.1_model_loop1_run40_i45_newExport_nesqr-20.1.pkl contributes 38 total 919 not known 919 uniques 28
l0and1/smt4vamp_deepire3_d4869_10s_dis10.1_model_loop1_run40_i45_newExport_nesqr-2.1_nesqc--0.25.pkl contributes 32 total 945 not known 945 uniques 28
l0and1/smt4vamp_deepire3_d4869_10s_dis10.1_model_loop1_run40_i15ne_nesqr-2.1.pkl contributes 27 total 720 not known 720 uniques 25
l0and1/air03_smt4vamp_deepire3_d4869lrsSave_10s_loop0_dis10.1.pkl contributes 24 total 734 not known 734 uniques 22
l0and1/smt4vamp_deepire3_d4869_10s_dis10.1_model_loop1_run40_i65ne_nesqr-2.1.pkl contributes 18 total 895 not known 895 uniques 18
Total 1528 not known 1528

...

DISCLAIMER:

The provided scripts are only research prototypes and may require some debugging to be used on a new computer.
In particular, some paths might have been hard-coded and need to be appropriately updated for the scripts to work properly.
