#!/usr/bin/env python2

import sys, os

import subprocess, time, signal

import cPickle as pickle
import gzip
import math, random
from collections import defaultdict

def normalize_names(dict):
  res = {}
  for name,val in dict.items():
    if name.startswith("./"):
      name = name[2:]
    elif name.startswith("/"):
      name = name[1:]
    res[name] = val
  return res

def get_loop_idx(name):
  for piece in name.split("_"):
    if piece.startswith("loop"):
      while piece[-1] not in "0123456789":
        piece = piece[:-1]
      return int(piece[4:])    
  return -1

def get_model_index(name): # ...x1000_d02_256_i90_nesqr...  --> 90
  for piece in name.split("_"):
    if piece.startswith("i"):
      piece = piece[1:]+"x" # drop it leading i and add a fake char so that we can start the loop by removing something
      while len(piece)>1:
        piece = piece[:-1]
        try:
          # print "Trying", piece
          return int(piece)
        except ValueError:
          pass

  return -1

if __name__ == "__main__":

  solved_by_someone = set()
  with open("/nfs/sudamar2/mizar/pepa-solved","r") as f:
    for line in f:
      prob = "small_np/"+line[:-1]
      # print prob
      solved_by_someone.add(prob)

  by_model = {} # model_index -> (num_solved_in_total,num_solved_over_prev_loop)

  '''
  solved_by_someone = {}
  with open("/nfs/sudamar2/mizar/mizar_strat1_train.txt","r") as f:
    for line in f:
      prob = line[:-1]
      # print prob
      solved_by_someone[prob] = 1.0

  with open("mizar_strat1_train.pkl",'wb') as f:
    pickle.dump(solved_by_someone,f)
  '''

  # print len(all_probs)

  hist = defaultdict(int) # how many times has this benchmark been solved?
  
  confs = [] # to have solvers in order
  
  results = {} # conf -> (bechmarm -> time)
  solveds = {} # conf -> set_of_solved
  
  loop_solveds = defaultdict(set) # loop_idx -> set_of_solved (in the union across all in the loop group)
  
  for filename in sys.argv[1:]:
    with open(filename,'rb') as f:
      confs.append(filename)
      
      result = normalize_names(pickle.load(f))
      results[filename] = result
      solved = set(result)
      solveds[filename] = solved
      loop_solveds[get_loop_idx(filename)] |= solved
      
      for benchmark in result:
        hist[benchmark] += 1

  '''
  stras_with_scores = []
  for strat, solved in solveds.iteritems():
    score = sum([1.0/hist[benchmark] for benchmark in solved])
    stras_with_scores.append((strat,len(solved),score))

  for strat, total, score in sorted(stras_with_scores,key = lambda x : x[2]):
    print strat, total, score
  '''

  '''
  base = results[confs[0]]
  other = results[confs[1]]

  base_total = 0.0
  other_total = 0.0
  common_cnt = 0

  base_under_3 = 0

  for benchmark in hist:
    if benchmark in base and base[benchmark] <= 3.0:
      base_under_3 += 1
    
  
    # print benchmark
    if benchmark in base and benchmark in other:
      common_cnt += 1
      base_total += base[benchmark]
      other_total += other[benchmark]

  print "common_cnt", common_cnt
  print "base_total", base_total
  print "other_total", other_total

  print
  print "base_under_3", base_under_3

  exit(0)
  '''
  
  print "Absolute ranking:"
  ranked_solveds = sorted(solveds.items(),key = lambda x : -len(x[1]))
  best_conf,best_solved = ranked_solveds[0]
  for conf, set_of_solved in ranked_solveds:
    print conf, len(set_of_solved), len(set_of_solved) - len(best_solved)

    idx = get_model_index(conf)
    if idx >= 0:
      by_model[idx] = len(set_of_solved)

  # print by_model

  print
  print "By loops:"
  union = set()
  loop0 = None
  for loop_idx in sorted(loop_solveds):
    for conf, set_of_solved in sorted(solveds.items(),key = lambda x : -len(x[1]-union)):
      if get_loop_idx(conf) == loop_idx:
        gain = len(set_of_solved-union)
        loss = len(union-set_of_solved)
        print conf, len(set_of_solved), 100.0*len(set_of_solved)/len(union) if union else 100.0, gain, loss
        
        idx = get_model_index(conf)
        if idx >= 0:
          total = by_model[idx]
          by_model[idx] = (total,gain)

    cur_loop_solved = loop_solveds[loop_idx]
    if loop_idx == 0:
      loop0 = cur_loop_solved
    print "Loop {}".format(loop_idx), len(cur_loop_solved), 100.0*len(cur_loop_solved)/len(union) if union else 100.0,
    print "added", len(cur_loop_solved-union), "still missing", len(union-cur_loop_solved),
    union |= cur_loop_solved
    print "accum", len(union)

  '''
  for loop_idx,solves in loop_solveds.items():
    if loop_idx < 2:
      solveds["loop{}".format(loop_idx)] = solves
  '''

  '''
  base_val = None
  last_dashcount = 0
  for conf, set_of_solved in sorted(solveds.items(),key = lambda x : x[0].count("-")*10000 + len(x[1])):
    if base_val is None:
      base_val = len(set_of_solved)
    dashcount = conf.count("-")
    if dashcount > last_dashcount:
      last_dashcount = dashcount
      print
    print conf, len(set_of_solved), len(set_of_solved) - base_val, 100.0*(len(set_of_solved) - base_val) / base_val
  '''

  list_for_josef = []

  print 
  print "Greedy cover:"
  if False: # a hack version starting greedy cover from the loop0 result
    covered = loop0
  else:
    covered = set()
  intersection = best_solved
  while True:
    best_val = 0
    for strat, solved in solveds.iteritems():
      intersection = intersection & solved
      val = len(solved - covered)
      # print "test:", strat, val
      if val > best_val:
        best_val = val
        best_strat = strat
    if best_val > 0:
      best_solved = solveds[best_strat].copy()
      print best_strat, "contributes", best_val, "total", len(best_solved), # "known", len(best_solved & solved_by_someone)
      print "not known", len(best_solved-solved_by_someone),
      list_for_josef.append((best_strat,best_solved))
      for strat, solved in solveds.iteritems():
        if strat != best_strat:
          best_solved = best_solved - solved
      print "uniques", len(best_solved)
      '''
      for prob in best_solved:
        print prob
      '''
      covered = covered | solveds[best_strat]
    else:
      break
  print "Total", len(covered), "not known", len(covered - solved_by_someone)

  print
  for idx,(total,gain) in sorted(by_model.items()):
    print idx, total, gain

  with open("histogram.txt","w") as f:
    for prob,val in hist.items():
      print >>f, prob,val

  '''
  print "Intersection", len(intersection)
  for prob in list(intersection)[:10]:
    print prob
  '''

  '''
  print
  for (best_strat,best_solved) in list_for_josef:
    prefix = best_strat.split(".")[0]+"/"
    for solved in best_solved:
      print prefix+solved.replace("/","_")+".log"
  '''
  '''
  print
  print len(all_probs), len(all_probs-covered)
  for prob in all_probs-covered:
    print prob
  '''
