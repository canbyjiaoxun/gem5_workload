#1) delete the collected data 
#2) build the latest source code 
#3) run the built object with the input data generated from ./rand 
#4) collect the latest input and output data 
import os 
from random import randint 

APP_name = 'sha'
run_time = 200

os.system("cd data/" + APP_name + " && rm *")
if APP_name == 'sha':
   os.system("cd benchmark/" + APP_name + " && rm " + APP_name + "_driver" + " && arm-linux-gnueabihf-gcc -o " + APP_name + "_driver" + " " + APP_name + "_driver.c -static")
else: 
   os.system("cd benchmark/" + APP_name + " && rm " + APP_name +  " && arm-linux-gnueabihf-gcc -o " + APP_name + " " + APP_name + ".c -static")

for i in range(run_time):
    # Generate random seed file 
    os.system("./rand")
    if APP_name == 'sha': 
       os.system('./build/ARM/gem5.opt --debug-flags=Exec,ExecTicks --debug-file=' + APP_name + '.arm.trace.out configs/example/se.py -c benchmark/' + APP_name + '/' + APP_name + '_driver')
    else: 
       os.system('./build/ARM/gem5.opt --debug-flags=Exec,ExecTicks --debug-file=' + APP_name + '.arm.trace.out configs/example/se.py -c benchmark/' + APP_name + '/' + APP_name)
    os.system('cd analysis && python data_collect.py')

