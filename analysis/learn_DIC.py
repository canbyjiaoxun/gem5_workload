#Function: a regression model to predict #dynamic instruction count based on input data 

import numpy as np 
from sklearn import linear_model 
from sklearn import svm
from sklearn.ensemble.forest import RandomForestRegressor

def feature(datum):
   feat = []
   #datum is a string, like "122 123\n" 
   feat = feat + [int(i) for i in datum.split()]
   return feat 

def yFeature(datum):
   #datum is a string 
   y = int(datum.split()[1])
   return y 

def pred_accuracy(clf, test_X, test_Y):
   #match = np.array(clf.predict(test_X)).astype(int)/50 == np.array(test_Y)/50
   diff = abs(clf.predict(test_X) - test_Y)
   return np.mean(diff)
   #print clf.predict(test_X)[:10], test_Y[:10]
   #print sum(match[:50])
   #return float(sum(match))/len(match)

train_input_file = open("../data/train_input")
train_input_list = train_input_file.readlines()

train_output_file = open("../data/train_output")
train_output_list = train_output_file.readlines()

test_input_file = open("../data/test_input")
test_input_list = test_input_file.readlines()

test_output_file = open("../data/test_output")
test_output_list = test_output_file.readlines() 

train_X = [feature(x) for x in train_input_list] 
train_Y = [yFeature(y) for y in train_output_list]

test_X = [feature(x) for x in test_input_list]
test_Y = [yFeature(y) for y in test_output_list]

#clf = linear_model.LinearRegression()
clf = RandomForestRegressor()
#clf = svm.SVC()
clf.fit(train_X, train_Y)

print pred_accuracy(clf, test_X, test_Y) 
 

