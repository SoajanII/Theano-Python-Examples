__author__ = 'SoajanII'
#https://en.wikipedia.org/wiki/Iris_flower_data_set

import numpy as np
import theano.tensor as T
from theano import function
from theano import shared

def E(Y, Y_act):
    numElements = Y.shape[0]
    diff = abs(Y-Y_act)
    numDiff = diff.sum()/2.
    return numDiff/numElements

nf = 4 #number of features
no = 3 #number of outputs
N = 150 #total number of examples
fracTrain = 0.8 #fraction of training examples to all examples
fileName = 'iris.txt'

initM = 0.1
ls1 = 4
ls2 = 4
learningRate = 0.1
numIterations = 500000

#initializing the test and train matrices
nTrain = int(N*fracTrain)
nTest = N - nTrain
"""
Xtrain=np.zeros(shape=(nTrain, nf)) #X declaration
Ytrain=np.zeros(shape=(nTrain, no)) #Y declaration
Xtest=np.zeros(shape=(nTest, nf)) #X declaration
Ytest=np.zeros(shape=(nTest, no)) #Y declaration
"""
#reading the file and writing to the big matrix
X_and_Y=np.zeros(shape=(N, nf+no)) #X declaration
file = open(fileName, 'r')
line = file.readline()
lineCounter = 0

while lineCounter<N:
    data = line.split()
    for i in range(0,nf):
        X_and_Y[lineCounter, i] = data[i]
    if(data[nf]=='I.setosa'):
        X_and_Y[lineCounter, nf:] = [1, 0, 0]
    elif(data[nf]=='I.versicolor'):
        X_and_Y[lineCounter, nf:] = [0, 1, 0]
    elif(data[nf]=='I.virginica'):
        X_and_Y[lineCounter, nf:] = [0, 0, 1]
    lineCounter=lineCounter+1
    line = file.readline()

#shuffling the big matrix in the end to for Xtrain, Ytrain, Xtest, Ytest
np.random.shuffle(X_and_Y)

Xtrain = X_and_Y[0:nTrain, 0:nf]
Ytrain = X_and_Y[0:nTrain, nf:]
Xtest = X_and_Y[nTrain:, 0:nf]
Ytest = X_and_Y[nTrain:, nf:]

#normalize the input data!!!!!
Xtrain_norm = Xtrain/10
Xtest_norm = Xtest/10
"""
print Xtrain_norm
print " "
print Ytrain
"""
#stop, train time!!
#symbolic math
Xtr=T.dmatrix('Xtr')
Ytr=T.dmatrix('Ytr')
w1 = shared(np.random.rand(nf, ls1)*initM, name='w1')
w2 = shared(np.random.rand(ls1, ls2)*initM, name='w2')
w3 = shared(np.random.rand(ls2, no)*initM, name='w3')
print w1.get_value()
h1=T.nnet.sigmoid(T.dot(Xtr, w1)) #http://deeplearning.net/software/theano/library/tensor/nnet/nnet.html#tensor.nnet.sigmoid
h2=T.nnet.sigmoid(T.dot(h1, w2))
pred = T.nnet.softmax(T.dot(h2, w3))
crossEnt = T.nnet.categorical_crossentropy(pred, Ytr)
cost = T.mean(crossEnt)
gw1, gw2, gw3 = T.grad(cost=cost, wrt=[w1, w2, w3])
train = function(inputs=[Xtr, Ytr], outputs = [pred, cost], updates=((w1, w1-learningRate*gw1), (w2, w2-learningRate*gw2), (w3, w3-learningRate*gw3)), allow_input_downcast=True)

Xte = T.dmatrix('Xte')
ht1 = T.nnet.sigmoid(T.dot(Xte, w1))
ht2 = T.nnet.sigmoid(T.dot(ht1, w2))
test_pred = T.nnet.softmax(T.dot(ht2, w3))
test = function(inputs=[Xte], outputs=test_pred)

for i in range(numIterations):
    output, costt = train(Xtrain_norm, Ytrain)
    if i%10000==0:
        print "iteration #" + str(i) + ": , cost: " + str(costt)
        print "Ein: " + str(E(output, Ytrain))
        output_test = test(Xtest_norm)
        print "Eout: " +str(E(output_test, Ytest))
        print " "
