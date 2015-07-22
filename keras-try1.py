from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation
from keras.layers.recurrent import LSTM
from keras.optimizers import SGD
import numpy as np

text = open('big.txt').read().lower()[100000:200000]
print('corpus length:', len(text))

chars = set(text)
print('total chars:', len(chars))
char_indices = dict((c, i) for i, c in enumerate(chars))
indices_char = dict((i, c) for i, c in enumerate(chars))

# cut the text in semi-redundant sequences of maxlen characters
maxlen = 20
step = 3
sentences = []
next_chars = []
for i in range(0, len(text) - maxlen, step):
    sentences.append(text[i : i + maxlen])
    next_chars.append(text[i + maxlen])
print('nb sequences:', len(sentences))

print('Vectorization...')
X = np.zeros((len(sentences), maxlen, len(chars)), dtype=np.bool)
y = np.zeros((len(sentences), len(chars)), dtype=np.bool)
for i, sentence in enumerate(sentences):
    for t, char in enumerate(sentence):
        X[i, t, char_indices[char]] = 1
    y[i, char_indices[next_chars[i]]] = 1

# build the model: 2 stacked LSTM
print('Build model...')
model = Sequential()
model.add(LSTM(len(chars), 20, return_sequences=True))
model.add(Dropout(0.2))
model.add(LSTM(20, 20, return_sequences=False))
#model.add(LSTM(len(chars), 20, return_sequences=False))
model.add(Dropout(0.2))
model.add(Dense(20, len(chars)))
model.add(Activation('softmax'))

print 'Compiling model...'
model.compile(loss='categorical_crossentropy', optimizer='adadelta')

print 'Begining to train...'
for iteration in range(1, 10):
    print '-' * 50
    model.fit(X, y, batch_size=128, nb_epoch=1)
    # generate a test sentence
    start_index = np.random.randint(0, len(text) - maxlen - 1)
    generated = ''
    sentence = text[start_index : start_index + maxlen]
    generated += sentence
    print 'Seed sentence:', sentence
    for _ in range(40):
        x = np.zeros((1, maxlen, len(chars)))
        for t, char in enumerate(sentence):
            x[0, t, char_indices[char]] = 1.0
        preds = model.predict(x, verbose=0)[0]
        next_index = np.argmax(preds)
        next_char = indices_char[next_index]
        generated += next_char
        sentence = sentence[1:] + next_char
    print 'Generated sentence:', generated
