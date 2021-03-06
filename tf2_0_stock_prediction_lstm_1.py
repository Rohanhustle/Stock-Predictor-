# -*- coding: utf-8 -*-
"""TF2.0 Stock Prediction LSTM 1.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/19dJ3Hz8AGLGST2U7NPP6pOypBm-VfMns
"""

!pip install tensorflow-gpu==2.0.0-beta1
import tensorflow as tf
print(tf.__version__)

from tensorflow.keras.layers import Input,Dense,Flatten,SimpleRNN,LSTM,GRU,GlobalMaxPool1D
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import SGD,Adam

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler

df=pd.read_csv('../stock predictor')

#Start by doing the wrong thing-tryingt o predict the stock itself
series=df['close'].values.reshape(-1,1)

#Normalize the data
scaler =StandardScaler()
scaler.fit(:len(series) //2])
series=scaler.transform(series).flatten()

#build the dataset
T=10
D=1
X=[]
Y=[]
for t inrange(len(series) - T):
  x=series[t:t+T]
  X.append(x)
  y=series[t+T]
  Y.append(y)

X=np.array(X).reshape(-1,T,1) 
Y=np.array(Y)
N=len(X)
print('X.shape',X.shape,'Y.shape',Y.shape)

i=Input(shape=(T,1))
x=LSTM(5)(i) # relu and tanh do not work for this
x=Dense(1)(x)
model=Model(i,x)
model.compile(
    loss='mse',
    optimizer=Adam(lr=0.1),
)
#train the RNN
r=model.fit(
    X[:-N//2],Y[:-N//2], # here we train the first half 
    epochs=80,
    validation_data = (X[-N//2:],Y[-N//2:]), # here we test the rest data from N/2 to N
)

df['PrevClose']=df['close'].shift() # move everything by one

#then the return is
#(x[t] - x[t-1]) /x[t-1]
df['Return']=(df['close']-df['PrevClose'])/df['PrevClose']

df['Return'].hist()

series=df['Return'].values[1:].reshape(-1,1)
#Normalize the data
scaler = StandardScaler()
scaler.fit(:len(series) // 2)
series = scaler.transform(series).flatten()

#build the dataset
T=10
D=1
X=[]
Y=[]
for t inrange(len(series) - T):
  x=series[t:t+T]
  X.append(x)
  y=series[t+T]
  Y.append(y)

X=np.array(X).reshape(-1,T,1) 
Y=np.array(Y)
N=len(X)
print('X.shape',X.shape,'Y.shape',Y.shape)

i=Input(shape=(T,1))
x=LSTM(5)(i) # relu and tanh do not work for this
x=Dense(1)(x)
model=Model(i,x)
model.compile(
    loss='mse',
    optimizer=Adam(lr=0.1),
)
#train the RNN
r=model.fit(
    X[:-N//2],Y[:-N//2], # here we train the first half 
    epochs=80,
    validation_data = (X[-N//2:],Y[-N//2:]), # here we test the rest data from N/2 to N
)

#OneStep Validation
outputs = model.predict(X)
print(outputs.shape)
predictions= outputs[:,0]

plt.plot(Y,label='targets')
plt.plot(predictions,label='predictions')
plt.title("Linear Regression Predictions")
plt.legend()
plt.show()

# Multi Step Correct way of forecasting
validation_target = Y[-N//2:]
validation_predictions=[]
#index of first validation input

#last train input
last_x=X[-N//2] # i-D array of length T

while len(validation_predictions)<len(validation_target):
  p=model.predict(X[i].reshape(1,-1,1))[0,0] # predict gives a 2x2 array ->scalar

  #update the prediction list
  validation_predictions.append(p)

  #make the new input
  last_x = np.roll(last_x,-1) # -1 means all are shifted to the left by 1 unit
  last_x[-1] =p # add the pediction as the last new value to the list

#Now turn the data into numpy array

#Not yet in the final "X" format
input_data= df[['open','high','low','close','volume']].values
targets=df['Return'].values

#Now make the actual data that will go into the neural network
T=10
D=input_data.shape[1]
N=len(input_data) - T

Ntrain = len(input_data)*2 //3
scaler = StandardScaler()
scaler.fit(input_data[:Ntrain + T])
input_data=scaler.transform(input_data)

X_train = np.zeros((Ntrain,T,D))
y_train = np.zeros(Ntrain)

for t in range(len(Ntrain)):
  X_train[t,:,:] = input_data[t:t+T]
  y_train[t] = (targets[t+T] > 0 )

X_test = np.zeros((N-NTrain,T,D))
Y_test = np.zeros(N-Ntrain)

for u in range(N-Ntrain):
  # u counts from 0 .... (N-NTrain)
  #t counts from NTrain ....N
  t=u+NTrainX
  X_test[u,:,:]=input_data[t:t+T]
  Y_test[u] = (targets[t+T] > 0)

i=Input(shape=(T,D))
x=LSTM(50)(i)
x=Dense(1,activation='sigmoid')(x)
model = Model(i,x)
model.compile(
    loss='binary_crossentropy',
    optimizer=Adam(lr=0.01),
    metrics=['accuracy'],
)

r=model.fit(
    X_train,Y_train,
    batch_size=32,
    epochs=300,
    validation_data = (X_test,Y_test),
)

