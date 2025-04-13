import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.callbacks import EarlyStopping

from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix

import nltk
nltk.download('stopwords')
nltk.download('punkt')
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

import functools, re
import random

df = pd.read_csv(r"C:\Users\afzal\PycharmProjects\cyberbullyingdetection\myapp\static\toxi.csv")
df.cyberbullying_type.value_counts().plot.barh(xlim=(7800,8000))

stopwords = [i.lower() for i in nltk.corpus.stopwords.words('english') + [chr(i) for i in range(97, 123)]]
x = df.tweet_text.apply(lambda text: re.sub("\s+", " ", ' '.join([i for i in re.sub("[^9A-Za-z ]", "" , re.sub("\\n", "", re.sub("\s+", " ", re.sub(r'http\S+', '', text.lower())))).split(" ") if i not in stopwords]))).values.astype(str)

y = df.cyberbullying_type != "not_cyberbullying"

x_train, x_val, y_train, y_val = train_test_split(x, y, test_size=0.4)
x_val, x_test, y_val, y_test = train_test_split(x_val, y_val, test_size=0.25)

tokenizer = tf.keras.preprocessing.text.Tokenizer(num_words=2000, oov_token="<OOV>")
tokenizer.fit_on_texts(x)
word_index = tokenizer.word_index

x_train = pad_sequences(tokenizer.texts_to_sequences(x_train), maxlen=100, padding='post', truncating='post')
x_test = pad_sequences(tokenizer.texts_to_sequences(x_test), maxlen=100, padding='post', truncating='post')
x_val = pad_sequences(tokenizer.texts_to_sequences(x_val), maxlen=100, padding='post', truncating='post')

model = tf.keras.Sequential([
    tf.keras.layers.Embedding(2000, 64), # embedding layer
    tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(64, dropout=0.2, recurrent_dropout=0.2)), # LSTM layer
    tf.keras.layers.Dropout(rate=0.2), # dropout layer
    tf.keras.layers.Dense(64, activation='swish'), # fully connected layer
    tf.keras.layers.Dense(1, activation='sigmoid') # final layer
])

model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy', 'AUC'])

model.summary()

early_stopping_monitor = EarlyStopping(patience=2)
history = model.fit(x_train, y_train, epochs=10, validation_data=(x_val, y_val), callbacks = [early_stopping_monitor])


y_pred = model.predict(x_test).round().T[0]

(y_pred == y_test).mean()

print(classification_report(y_test.astype(int), y_pred, digits=3))

y_rand = np.random.random(*y_test.shape).round().astype(int)
(y_rand == y_test).mean()

print(classification_report(y_test.astype(int), y_rand, digits=3))

model.save('cyberbullying-bdlstm.h5')
import json
with open("tokenizer.json", "w+") as file:
    file.write(tokenizer.to_json())
