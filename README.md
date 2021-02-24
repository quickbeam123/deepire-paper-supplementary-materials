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

TODO: under construction

5) Training data (loop 0)

6) To start training:
