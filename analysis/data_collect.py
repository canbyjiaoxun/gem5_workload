#Function: read the sim_insts and dynamic instruction mix 
#Input: m5out/stats.txt and m5out/benchmark.trace.file 
#Output: train_input containing different instruction type mix 
#Output: train_output which is sim_insts 
import os 
import sys 
from collections import defaultdict 

#runpath = "/home/canbyjioxun/gem5/run.py"
#sys.path.append(os.path.abspath(runpath))
#import run 

#APP_name = raw_input("what application do you want to collect")
APP_name = 'sha'
#APP_name = run.APP_name 

############# Constant Initialization ################
read_lines_start = 10000
read_lines_end = 20000

############# Variable initialization ################
inst_dict = defaultdict(int)

################# read input data file ########################
#input_data_value_file = open('input_data_value.txt')
#input_data_value_list = input_data_value_file.readlines()

#################  read instruction trace file ####################
trace_file = open('../m5out/' + APP_name + '.arm.trace.out')
trace_list = trace_file.readlines() 
for line in trace_list[:10000]:
   inst = line.split()[6] 
   if inst.startswith('add'):
      inst_dict['add'] += 1 
   elif inst.startswith('mul'):
      inst_dict['mul'] += 1 
   elif inst.startswith('cmp'):
      inst_dict['cmp'] += 1 
   elif inst.startswith('ldr'):
      inst_dict['ldr'] += 1 
   elif inst.startswith('sub'):
      inst_dict['sub'] += 1 
   elif inst.startswith('str'):
      inst_dict['str'] += 1 
   elif inst.startswith('b'):
      inst_dict['branch'] += 1 
   elif inst.startswith('mov'):
      inst_dict['mov'] += 1 
   else:
      inst_dict['other'] += 1 

print inst_dict.values() 


dyna_inst_mix_file = open('../data/' + APP_name + '/dyna_inst_mix.txt', 'a')
for inst in ['add', 'mul', 'cmp', 'ldr', 'sub', 'str', 'branch', 'mov', 'other']:
    dyna_inst_mix_file.write(str(inst_dict[inst]) + '\t')
dyna_inst_mix_file.write('\n')
#dyna_inst_mix_file.write(str(inst_dict.values()) + '\n')


################ read output file #######################
stats_file = open('../m5out/stats.txt')
stats_list = stats_file.readlines()
train_output_file = open('../data/' + APP_name + '/output_workload.txt', 'a')
train_output_file.write(stats_list[11].split()[1] + '\n')
