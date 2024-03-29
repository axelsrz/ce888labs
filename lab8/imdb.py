
from __future__ import print_function
import numpy as np
np.random.seed(1337)  # for reproducibility

from keras.preprocessing import sequence
from keras.models import Model
from keras.layers import Dense, Activation, Embedding, Flatten, Input, Convolution1D, GlobalMaxPooling1D, LSTM, Dropout, merge
from keras.datasets import imdb

max_features = 20000
maxlen = 80  # cut texts after this number of words (among top max_features most common words)
batch_size = 32

print('Loading data...')
(X_train, y_train), (X_test, y_test) = imdb.load_data(nb_words=max_features)
print(len(X_train), 'train sequences')
print(len(X_test), 'test sequences')

print (X_train[0])

print('Pad sequences (samples x time)')
X_train = sequence.pad_sequences(X_train, maxlen=maxlen)
X_test = sequence.pad_sequences(X_test, maxlen=maxlen)
print('X_train shape:', X_train.shape)
print('X_test shape:', X_test.shape)

print('Build model...')


inputs = Input(shape=(maxlen,))
x = inputs
x = Embedding(max_features, 128, dropout=0.2)(x)
x = Convolution1D(64, 3, border_mode='same')(x)
x = Activation('relu')(x)
x = GlobalMaxPooling1D()(x)
x = Dropout(0.25)(x)
x = Dense(64)(x)
x = Activation("relu")(x)

y = Embedding(max_features, 128, dropout=0.2)(inputs)
y = LSTM(128, dropout_W=0.2, dropout_U=0.2)(y)
y = Dense(64)(y)
y = Activation("relu")(y)

m = merge([x, y], mode='concat', concat_axis=1)
m = Dense(1)(m)
m = Activation('sigmoid')(m)


model = Model(input=inputs, output=m)
model.compile(loss='binary_crossentropy',
              optimizer='adam',
              metrics=['accuracy'])

print('Train...')
model.fit(X_train, y_train, batch_size=batch_size, nb_epoch=15,
          validation_data=(X_test, y_test))
score, acc = model.evaluate(X_test, y_test,
                            batch_size=batch_size)
print('Test score:', score)
print('Test accuracy:', acc)
