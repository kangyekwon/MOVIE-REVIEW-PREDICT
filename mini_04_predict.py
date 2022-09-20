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
import re

pd.set_option('display.unicode.east_asian_width', True)
pd.set_option('display.max_columns', 20)
df = pd.read_csv('./crawling_data/movies.csv')

X = []  #입력
# 제목 + 리뷰내용 합치기
for i in range(len(df)):
    X.append(df.iloc[i, 0] + df.iloc[i, 1])
# 리뷰내용 한국어&공백 빼고 삭제하기
for i in range(len(X)):
    X[i] = re.compile('[^가-힣 ]').sub(' ', X[i])
#print(X[:5])

Y = df['score']  #출력
# score 7미만은 라벨 부정(0)으로 변경 / else는 긍정(1)로 변경
for i in range(len(Y)):
    if Y[i] < 7:
        Y[i] = 0
    else:
        Y[i] = 1

with open('./models/movies_encoder.pickle', 'rb') as f:
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

with open('./models/movies_token.pickle', 'rb') as f:
    token = pickle.load(f)

tokend_X = token.texts_to_sequences(X)

for i in range(len(tokend_X)):
    if len(tokend_X[i]) > 181:
        tokend_X[i] = tokend_X[i][:181]

X_pad = pad_sequences(tokend_X, 181)

print(X_pad[:5])

model = load_model('./models/movies_classification_model_0.8448182344436646_0602.h5')

score = model.predict(X_pad) # 예측
# print(score)
# exit()

for i in range(len(df)):
    if(np.argmax(score[i])):
        print(df.iloc[i], "{:.2f}% 확률로 긍정 리뷰입니다.\n".format(score[i][1] * 100))
    else:
        print(df.iloc[i], "{:.2f}% 확률로 부정 리뷰입니다.\n".format((score[i][0]) * 100))