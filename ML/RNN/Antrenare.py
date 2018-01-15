import numpy
import time
from keras.models import Sequential
from keras.layers import Dense
from parseruts import return_data

inputs, targets = return_data('set1.txt',300)
# print(inputs[0])
# print(targets[0])
# exit()
first_layer = len(inputs[0])
last_layer = len(targets[0])
inputs = numpy.asarray(inputs)
targets = numpy.asarray(targets)


# reshaped_inputs = []
# reshaped_targets = []

# for inp in inputs:
#     reshaped_inputs.append(numpy.reshape(inp, [1, first_layer]))

model = Sequential()
model.add(Dense(100, input_dim=first_layer, activation='sigmoid'))
model.add(Dense(100, activation='sigmoid'))
model.add(Dense(last_layer, activation='softmax'))

model.compile(loss='categorical_crossentropy', optimizer='rmsprop')

start_time = time.time()
while True:
    model.fit(inputs, targets, batch_size=1, epochs=20, verbose=0)
    if time.time() - start_time > 3600*2:
        model.save_weights("weights_sigmoid_with_softmax.h5", overwrite=True)
        break

inputs, targets = return_data('proba.txt',300)
print(model.predict(numpy.reshape(inputs[0], [1, first_layer]))) 
