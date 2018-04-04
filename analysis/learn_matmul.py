#Function: a regression model to predict #dynamic instruction count based on input data 
#Input: APP_name 
#03/03/18 

import time
import numpy as np 
from sklearn import linear_model 
from sklearn import svm
from sklearn.ensemble.forest import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPRegressor
from sklearn.neighbors import KNeighborsRegressor

APP_name = 'matmul'

def feature(datum):
   feat = []
   #datum is a string, like "122 123\n" 
   feat = feat + [int(i) for i in datum.split()]
   return feat 

def yFeature(datum):
   #datum is "123"
   y = int(datum.split()[0])
   return y 

def pred_accuracy(clf, test_X, test_Y):
   #match = np.array(clf.predict(test_X)).astype(int)/50 == np.array(test_Y)/50
   #diff = abs(clf.predict(test_X) - test_Y)
   pred_Y = clf.predict(test_X)
   sum_diff = 0 
   #sum_rela_diff = 0 
   for i in range(len(test_X)):
       diff = abs((pred_Y[i] - test_Y[i]))
       #rela_diff = abs((pred_Y[i] - test_Y[i]))/float(pred_Y[i])
       sum_diff += (diff > 100000) 
       #sum_rela_diff += rela_diff 
   pred_error = sum_diff / float(len(test_X))
   #ave_diff = sum_rela_diff / float(len(test_X))
   return pred_error 
   #return ave_diff
   #print clf.predict(test_X)[:10], test_Y[:10]
   #print sum(match[:50])
   #return float(sum(match))/len(match)

input_file = open("../data/" + APP_name + '/input_value.txt')
#input_file = open("../data/" + APP_name + '/dyna_inst_mix.txt')
input_list = input_file.readlines()

output_file = open("../data/" + APP_name + '/output_workload.txt')
output_list = output_file.readlines()

X = [feature(x) for x in input_list] 
Y = [yFeature(y) for y in output_list]
train_X, test_X, train_Y, test_Y = train_test_split(X, Y, test_size = 0.10, random_state = 40)

#clf = linear_model.LinearRegression()
#clf = MLPRegressor()
#clf = RandomForestRegressor()
clf = svm.SVC()
#clf = KNeighborsRegressor()
start_time = time.time()
clf.fit(train_X, train_Y)
print("Training Time: -- %s seconds ---" % (time.time() - start_time))

start_time = time.time()
print pred_accuracy(clf, test_X, test_Y) 
print("Testing Time: --- %s seconds ---" % (time.time() - start_time)) 

