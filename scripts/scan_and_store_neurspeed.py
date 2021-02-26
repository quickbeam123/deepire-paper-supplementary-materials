#!/usr/bin/env python2

import sys, os

import cPickle as pickle
import gzip
import math
from collections import defaultdict

if __name__ == "__main__":
  prob_text_file_name = sys.argv[1]
  solver_folder = sys.argv[2]

  # to be run as in: ./scan_and_store_one.py prob_text_file.txt folder_name_with_output_logs(no trailing slash)
  
  # either there are some unresolved ones we report on, or we create a pickle with results and save it

  unresolved = set()
  true_names = {}
  with open(prob_text_file_name,"r") as f:
    for line in f:
      true_name = line[:-1]
      if true_name[0] == ".":
        true_name = true_name[1:]
      bench_name = true_name.replace("/","_")
      unresolved.add(bench_name)
      true_names[bench_name] = true_name

  results = {} # (benchmark -> time)

  eval_times_sum = 0.0
  last_time_sum = 0.0
  
  eval_times_sum_on_failed = 0.0
  last_time_sum_on_failed = 0.0
  
  eval_times_sum_on_solved = 0.0
  last_time_sum_on_solved = 0.0

  for (dirpath, dirnames, filenames) in os.walk(solver_folder):
    if filenames:
      for log in filenames:
        benchmark = log[:-4]
      
        '''
        if tptp_name not in bench_ratings:
          unresolved.discard(tptp_name)
          continue
        '''
      
        with open(dirpath+"/"+log,"r") as f:
          result = None
          last_time = None
          eval_time = None
          report = True
          error = False
          hasThax = False
          lines = []
          for line in f:
            lines.append(line)
        
            # vampiric part:
            if (line.startswith("% SZS status Timeout for") or line.startswith("% SZS status GaveUp") or
               line.startswith("% Time limit reached!") or line.startswith("% Refutation not found, incomplete strategy") or
               line.startswith("% Refutation not found, non-redundant clauses discarded") or
               line.startswith("Unsupported amount of allocated memory:")):
              result = "---"
              report = False
        
            if line.startswith("% SZS status Unsatisfiable") or line.startswith("% SZS status Theorem") or line.startswith("% SZS status ContradictoryAxioms"):
              result = "uns"
              report = False

            if line.startswith("% SZS status Satisfiable") or line.startswith("% SZS status CounterSatisfiable"):
              result = "sat"
              report = False
      
            if "[theory axiom]" in line:
              hasThax = True
      
            if line.startswith("Parsing Error on line"):
              result = "err"
              report = False
            
            if "violated" in line:
              error = True
            if "Aborted by signal" in line:
              error = True
      
            if line.startswith("% Time elapsed:"):
              last_time = float(line.split()[-2])
        
            # % neural model evaluation: 6.475 s
            if line.startswith("% neural model evaluation:"):
              eval_time = float(line.split()[-2])
        
              assert last_time
              eval_times_sum += eval_time
              last_time_sum += last_time
              # print benchmark, "eval time percent:", eval_time/last_time, result
              
              if result == "uns":
                eval_times_sum_on_solved += eval_time
                last_time_sum_on_solved += last_time
              if result == "---":
                eval_times_sum_on_failed += eval_time
                last_time_sum_on_failed += last_time
        
          if error:
            print "Error for", benchmark

            printing = None # either None, or acculates an error
            time_elapsed_dist = 666
            last_percent_line = ""
            for line in lines:
              if line.startswith("%"):
                last_percent_line = line[:-1]
            
              if line.startswith("% Time elapsed:"):
                time_elapsed_dist = 0
              else:
                time_elapsed_dist += 1
            
              if "Condition in file" in line:
                printing = [last_percent_line,"time_elapsed_dist "+str(time_elapsed_dist)]
              
              if "Control points passed: " in line and printing is None:
                printing = [last_percent_line,"PURE CONTROL POINT?"+str(time_elapsed_dist)]
            
              if "Aborted by signal" in line and printing is None:
                printing = [last_percent_line,"PURE ABORT"]
              
              if "corrupted double-linked list" in line and printing is None:
                printing = ["corrupted double-linked list"]
              
              if "corrupted size vs. prev_size in fastbins" in line and printing is None:
                printing = ["corrupted size vs. prev_size in fastbins"]
              
              if "timelimit: sending warning signal 15" in line and printing is None:
                printing = ["timelimit: sending warning signal 15"]
              
              if printing is not None:
                printing.append(line[:-1])
              
              if line.startswith("%") and printing is not None:
                '''
                if [line for line in printing if "Z3Interfacing::solve" in line]:
                  pass
                elif [line for line in printing if "Skolem::preskolemise (Formula*)" in line]:
                  pass
                elif [line for line in printing if "Kernel/Substitution.cpp, line 61 violated:" in line]:
                  pass
                elif [line for line in printing if "Condition in file Lib/Allocator.cpp, line 779 violated:" in line]:
                  pass
                elif [line for line in printing if "Condition in file SAT/Z3Interfacing.cpp, line 225 violated:" in line]:
                  pass
                else:
                '''
                if [line for line in printing if "Z3Interfacing::getAssignment" in line]:
                  print "NextArrayError:", true_names[benchmark],
                else:
                  print "Next error:"
                for line in printing:
                  print line

                printing = None

          if report:
            # print "Problems/"+benchmark
            # print "Problems/"+benchmark[:3]+"/"+benchmark
            # continue
            
            print "Weirdness for", benchmark
            # continue
            if lines:
              print "Has", len(lines), "lines"
            
              print "Printing last 5 lines:"
              for line in lines[-5:]:
                print line[:-1]
        
              print
              print
            else:
              print "EMPTY" # this happens when E does not finish and is killed from outside
          else:
            # print (result, last_time)
            if not error:
              unresolved.remove(benchmark)
            
            ''' -- only makes sense if the logs contain proofs!
            if not hasThax:
              print "noThax", benchmark, result
            '''
            
            # print "{}, {}, {}".format(true_names[benchmark], result, last_time if result != "---" else None)
            
            '''
            if result == "uns":
              print true_names[benchmark]
            '''
            
            if result == "sat" or result == "uns":
              results[true_names[benchmark]] = last_time

  if len(unresolved):
    print "unresolved", len(unresolved)
    for benchmark in unresolved:
      print true_names[benchmark]
  else:
    pass
  
  if True:
    print "results", len(results)

    for benchmark,time in results.items():
      print "."+benchmark

    save_to_name = solver_folder+".pkl"
    print "saving to", save_to_name
    with open(save_to_name,'wb') as f:
      pickle.dump(results,f)

  print "Eval time on average", 100.0*eval_times_sum/last_time_sum,"percent"

  # print "Eval time on solved", 100.0*eval_times_sum_on_solved/last_time_sum_on_solved,"percent"
  # print "Eval time on failed", 100.0*eval_times_sum_on_failed/last_time_sum_on_failed,"percent"
