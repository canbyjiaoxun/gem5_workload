#Function: predict bit-level timing errors of FUs using RFC(n_estimators=100) 
# Xun Jiao 01/19/2017
#Warning: bit_width 

import time
import os
from random import * 
from collections import defaultdict
import numpy as np
import sklearn
import scipy
from sklearn import svm
from sklearn import tree
from sklearn.ensemble.forest import RandomForestRegressor
from sklearn.ensemble import RandomForestClassifier
#from sklearn.neural_network import MLPClassifier
from sklearn import linear_model
from sklearn import neighbors
from sklearn.metrics import (accuracy_score, precision_score, recall_score, f1_score)


#create the binary vector as input feature
def bin_feature(data_list,i):
    feat = []
    x1 = map(int, data_list[i-1].split()[0])
    x2 = map(int, data_list[i-1].split()[1])
    x3 = map(int, data_list[i].split()[0])
    x4 = map(int, data_list[i].split()[1])
    feat = feat + x1 + x2 + x3 + x4
    #feat = feat + x3 + x4
    return feat

def bin_sum_feature(data_list,sum_list,i,bit_width,bit_position):
    feat = []
    x1 = map(int, data_list[i-1].split()[0])
    x2 = map(int, data_list[i-1].split()[1])
    x3 = map(int, data_list[i].split()[0])
    x4 = map(int, data_list[i].split()[1])
    sum1 = map(int, sum_list[i-1+2][2:].strip())
    sum2 = map(int, sum_list[i+2][2:].strip())
    feat = feat + x1 + x2 + x3 + x4 + sum1 + sum2 
    #feat = feat + x3 + x4 + sum2 
    return feat

def bit_label(TC_list, line_number, bit_position):
    bit = int(TC_list[line_number][31-bit_position])
    return bit 

def read_input_output_list(operator, condition, data, clk):
    input_data_file = open('../stimuli_data/' + data,'r')
    output_data_file = open("../REP/TC_" + operator + condition + clk + data + '.txt','r')
    input_data_list = input_data_file.readlines()
    output_data_list = output_data_file.readlines()
    input_data_file.close()
    output_data_file.close()
    return input_data_list, output_data_list 

#def write_result(bit_position, clk, test_data, exe_time, ML_accuracy, naive_accuracy, random_accuracy):
def write_result(bit_position, clk, test_data, ML_accuracy,ML_precision,ML_recall, ML_F1, ML_exe_time, naive_accuracy,naive_precision, naive_recall,  naive_F1, random_accuracy, random_precision, random_recall, random_F1):
    prediction_file = open('RFC_bit_error_prediction_result','a')
    prediction_file.write('################ For CLK at ' + clk + ' at bit ' + str(bit_position) + ' for ' + test_data + '%#################\n')
    prediction_file.write("--- " + str(ML_exe_time) + " seconds ---\n")
    prediction_file.write("Prediction accuracy for clf1 is " +  str(ML_accuracy) + ',' +str(ML_precision)+ ',' + str(ML_recall) + ',' + str(ML_F1) + '\n')
    prediction_file.write(str(clf1)+'\n')
    prediction_file.write("Prediction accuracy for naive is " + str(naive_accuracy) + ','  +str(naive_precision)+ ',' + str(naive_recall) + ',' + str(naive_F1) + '\n')
    prediction_file.write("Prediction accuracy for random is " + str(random_accuracy) + ',' +str(random_precision)+ ',' + str(random_recall) + ',' + str(random_F1) + '\n')
    prediction_file.close()

def clim_predictor(X, y_test, clf):
    start_time = time.time()
    y_pred = clf.predict(X)
    exe_time = time.time() - start_time
    accuracy = accuracy_score(y_test, y_pred)
    #print y_test, list(y_pred)
    #print y_pred[0]
    precision = precision_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)
    F1 = f1_score(y_test, y_pred) 
    return accuracy, precision, recall, F1, exe_time  

def rand_predictor(y_test):
    y_pred = [randint(0,1) for i in range(len(y_test))] 
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)
    F1 = f1_score(y_test, y_pred) 
    #error = sum(abs(randint(0,1)-int(test_y[i])) for i in range(len(test_y)))
    #accuracy = 1-float(error)/len(test_y)
    return accuracy, precision, recall, F1   
    #return accuracy

def naive_predictor(y_test):
    y_pred = [0 for i in range(len(y_test))]
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)
    F1 = f1_score(y_test, y_pred) 
    #error = sum(abs(int(test_y[i])-0) for i in range(len(test_y)))
    #accuracy = 1-float(error)/len(test_y)
    return accuracy, precision, recall, F1   
    #return accuracy

p = True 
operator = os.path.relpath('..','../..')
#operator = 'IntAdder_32_f400_uid2_Wrapper'
condition = '.0.85.50.'
#clk_list = ["1.369.","1.333.","1.304.","1.284."]
clk_list = ["1.400.","1.369.","1.333.","1.304.","1.284."]
train_data = 'random_data_1M'
#test_data_APP_list  = ["DCT_data", "roberts_data", "scharr_data", "prewitt_data", "sharpen_data", "sobel_data"]
#test_data_APP_list  = ["random_data", "sobel_data", "gauss_data"]
test_data_APP_list  = ["random_data"]
sum_data_file = open('../REP/outport_FPAdder_8_23_uid2_Wrapper.0.85.50.3.0.'+train_data+'.txt','r')
sum_data_list = sum_data_file.readlines()
sum_data_file.close()


#########################FOR EACH CLK ##############################
for clk in clk_list:
	####################### FORM TRAINING FEATURES ########################################
	train_data_list, train_bit_list = read_input_output_list(operator, condition, train_data, clk)
	TRAIN = int(len(train_data_list) * 0.9)
	bit_width = len(train_data_list[0].split()[0])-2  #FP_ADD use 34 bits 
        print bit_width

	#Extracting train features
	#train_X1 = [bin_feature(train_data_list,i) for i in range(1,TRAIN)]  #start from the 2nd element of training data because it has preceding input  
	###################### FOR EACH TEST DATA #########################################
	for test_data in test_data_APP_list: 
		test_data_list,test_bit_list = read_input_output_list(operator, condition, test_data, clk) 
		TEST = int(len(test_data_list) * 0.5)
	        sum_test_file = open('../REP/outport_FPAdder_8_23_uid2_Wrapper.0.85.50.3.0.'+test_data+'.txt','r')
	        sum_test_list = sum_test_file.readlines()
                sum_test_file.close()

		#Extract test features
		#test_X1 = [bin_feature(test_data_list,i) for i in range(1,TEST)]

		######################## FOR EACH BIT POSITION #############################
		#for bit_position in range(bit_width):
		for bit_position in range(18,21):
			####################### FORM TRAINING LABELS #####################################
	                #train_X1 = [bin_feature(train_data_list,i) for i in range(1,TRAIN)]  #start from the 2nd element of training data because it has preceding input  
                	train_X2 = [bin_sum_feature(train_data_list,sum_data_list,i,bit_width,bit_position) for i in range(1,TRAIN)] #start from the 2nd element of training data because it has preceding input 
			train_y = [bit_label(train_bit_list,i,bit_position) for i in range(3,TRAIN+2)] # 1st element map to 2nd element 

			#clf1 = linear_model.LogisticRegression()
			#clf1 = MLPClassifier(alpha=0.5)
			clf1 = RandomForestClassifier(n_estimators=100)  
			clf1.fit(train_X2, train_y)
			#clf1.fit(train_X2, train_y)
			print "model fitting complete"

			#form testing input file 
		        #test_X1 = [bin_feature(test_data_list,i) for i in range(1,TEST)]
        		test_X2 = [bin_sum_feature(test_data_list,sum_test_list,i,bit_width,bit_position) for i in range(1,TEST)]
			test_y = [bit_label(test_bit_list,i,bit_position) for i in range(3,TEST+2)]
			
			#################### WRITE RESULT TO FILE ##########################
			#start_time = time.time()
			ML_accuracy, ML_precision, ML_recall, ML_F1, ML_exe_time = clim_predictor(test_X2, test_y, clf1)
			#ML_accuracy, ML_precision, ML_recall, ML_F1, ML_exe_time = clim_predictor(test_X2, test_y, clf1)
			#exe_time = time.time() - start_time 
			naive_accuracy, naive_precision, naive_recall, naive_F1 = naive_predictor(test_y)
			random_accuracy, random_precision, random_recall, random_F1 = rand_predictor(test_y)
			print "accuracy for clf1 is ", ML_accuracy,ML_precision,ML_recall, ML_F1
			print "accuracy for naive is ", naive_accuracy,naive_precision,naive_recall,naive_F1
			print "accuracy for random is ", random_accuracy,random_precision,random_recall, random_F1
			write_result(bit_position, clk, test_data, ML_accuracy,ML_precision,ML_recall, ML_F1, ML_exe_time, naive_accuracy,naive_precision, naive_recall,  naive_F1, random_accuracy, random_precision, random_recall, random_F1)
 


