import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from konlpy.tag import Okt
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.utils import to_categorical
import pickle
from tensorflow.keras.models import load_model

pd.set_option('display.unicode.east_asian_width', True)
pd.set_option('display.max_columns', 20)
df = pd.read_csv('./crawling_data/naver_headline_news_20220527.csv')

X = df['titles']
Y = df['category']

with open('./models/encoder.pickle', 'rb') as f:
    encoder = pickle.load(f)

labeled_Y = encoder.transform(Y)
label = encoder.classes_

onehot_Y = to_categorical(labeled_Y)
print(onehot_Y)

okt = Okt()

for i in range(len(X)):
    X[i] = okt.morphs(X[i], stem=True)

stopwords = pd.read_csv('./crawling_data/stopwords.csv', index_col=0)

for j in range(len(X)):
    words = []
    for i in range(len(X[j])):
        if len(X[j][i]) >1 :
            if X[j][i] not in list(stopwords['stopword']):
                words.append(X[j][i])
    X[j] = ' '.join(words)

with open('./models/news_token.pickle', 'rb') as f:
    token = pickle.load(f)

tokend_X = token.texts_to_sequences(X)

for i in range(len(tokend_X)):
    if len(tokend_X[i]) > 17:
        tokend_X[i] = tokend_X[i][:17]

X_pad = pad_sequences(tokend_X, 17)
print(X_pad[:5])

model = load_model('./models/news_category_classification_model_0.7045454382896423.h5')
preds = model.predict(X_pad)
predicts = []
for pred in preds:
    most = label[np.argmax(pred)]
    pred[np.argmax(pred)] = 0
    second = label[np.argmax(pred)]
    predicts.append([most, second])
df['predict'] = predicts

print(df.head(30))

df['OX'] = 0
for i in range(len(df)):
    if df.loc[i, 'category'] in df.loc[i, 'predict']:
        df.loc[i, 'OX'] = 'O'
    else:
        df.loc[i, 'OX'] = 'X'
print(df.head(30))

print(df['OX'].value_counts())
print(df['OX'].value_counts()/len(df))

for i in range(len(df)):
    if df['category'][i] != df['predict'][i]:
        print(df.iloc[i])