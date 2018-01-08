import numpy
import time
from keras.models import Sequential
from keras.layers import Dense
from parseruts import return_data


model = Sequential()
model.add(Dense(100, input_dim=52, activation='relu'))
model.add(Dense(100, activation='relu'))
model.add(Dense(52, activation='relu'))

model.compile(loss='mse', optimizer='adam')
model.load_weights("weights.h5")

inputs, targets = return_data('proba.txt',300)
print(inputs[0])
print(targets[0])
print(model.predict(numpy.reshape(inputs[0], [1, 52]))) 
