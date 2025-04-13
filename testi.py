# import warnings
# def warn(*args, **kwargs):
#     pass
# warnings.warn = warn

import os
import time
import numpy as np
import pandas as pd
import re

import keras
from keras import *
from keras import layers, optimizers
from keras.layers import Embedding, Conv1D, GlobalMaxPooling1D, Dense, Dropout
from keras.models import Model
from keras.preprocessing import *
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences

from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

import pickle
keras.backend.clear_session()
sms_df = pd.read_csv(r'C:\Users\afzal\PycharmProjects\cyberbullyingdetection\spamham.csv')

# sms_df['Category'] = sms_df['Category'].replace("ham", 1)
# sms_df['Category'] = sms_df['Category'].replace("spam", 0)

labels = sms_df.values[:, 1]
msgs = sms_df.values[:, 0]

print(labels)

print(msgs)

train_texts, test_texts, train_labels, test_labels = train_test_split(msgs, labels, test_size=0.1, random_state=500)


test_texts=["@praisexoscar you're nigger youself you dumb fuck"]
VOCABULARY_SIZE = 5000
tokenizer = Tokenizer(num_words=VOCABULARY_SIZE)
tokenizer.fit_on_texts(train_texts)

print("Vocabulary created")

meanLength = np.mean([len(item.split(" ")) for item in train_texts])
#MAX_SENTENCE_LENGTH = int(meanLength + 5)
MAX_SENTENCE_LENGTH=100
print("MAX_SENTENCE LENGTH=",MAX_SENTENCE_LENGTH)
trainFeatures = tokenizer.texts_to_sequences(train_texts)
trainFeatures = pad_sequences(trainFeatures, MAX_SENTENCE_LENGTH, padding='post')
# trainLabels = train_labels.values

testFeatures = tokenizer.texts_to_sequences(test_texts)
testFeatures = pad_sequences(testFeatures, MAX_SENTENCE_LENGTH, padding='post')
# testLabels = test_labels.values

print("Tokenizing completed")

FILTERS_SIZE = 16
KERNEL_SIZE = 5

EMBEDDINGS_DIM = 10
LEARNING_RATE = 0.001
BATCH_SIZE = 32
EPOCHS = 20

print("embed=",EMBEDDINGS_DIM)
print(len(trainFeatures[0]))

maxlen=0

for i in trainFeatures:
    if len(i)>maxlen:
        maxlen=len(i)
print("maxlen=",maxlen)




model = Sequential()
model.add(Embedding(input_dim=VOCABULARY_SIZE + 1, output_dim=EMBEDDINGS_DIM, input_length=maxlen))
model.add(Conv1D(FILTERS_SIZE, KERNEL_SIZE, activation='relu'))
model.add(Dropout(0.5))
model.add(GlobalMaxPooling1D())
model.add(Dropout(0.5))
model.add(Dense(8, activation='relu'))
model.add(Dense(1, activation='sigmoid'))

optimizer = optimizers.Adam(lr=LEARNING_RATE)
model.compile(optimizer=optimizer, loss='binary_crossentropy', metrics=['accuracy'])

print(model.summary())

history = model.fit(trainFeatures, train_labels, batch_size=BATCH_SIZE, epochs=EPOCHS)

with open('tokenizer.pickle', 'wb') as handle:
    pickle.dump(tokenizer, handle, protocol=pickle.HIGHEST_PROTOCOL)
model_json = model.to_json()
with open("model.json", "w") as json_file:
    json_file.write(model_json)
model.save_weights("model.h5")


x = model.predict(testFeatures)

predicted = []

for i in x:
    print(i)

    if i[0] > 0.6:
        print("bull")
    else:
        print("not bull")

print('labels')

