import pandas as pd
import numpy as np
import requests
import re
from sklearn.model_selection import train_test_split
from konlpy.tag import Okt
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.utils import to_categorical
import pickle

pd.set_option('display.unicode.east_asian_width', True)
df = pd.read_csv('./crawling_data/movies.csv')
# print(df.head())
# df.info()

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
# print(df.head())
# print(df.groupby('score').size().reset_index(name = 'count'))
# exit()

# #인코딩 >> 사이킷런의 머신러닝 알고리즘은 문자열 값을 입력 값으로 허락하지 않으므로, 모든 문자열 값들을 숫자 형으로 인코딩하는 전처리 작업 후에 머신러닝 모델에 학습을 시켜야함
# # 라벨인코딩 >> 범주형 변수의 문자열을 수치형으로 변환
# encoder = LabelEncoder()
# labeled_Y = encoder.fit_transform(Y)
# print(labeled_Y)
# print(len(labeled_Y))
# #exit()
# label = encoder.classes_
# print(label)
#
# # 엔코더저장
# with open('./models/movies_encoder.pickle', 'wb') as f:
#     pickle.dump(encoder, f)

# 원핫인코딩 >> 피처값의 유형에 따라 새로운 피처를 추가해 고유값에 해당하는 칼럼에만 1표시/ 그외는 0표시
onehot_Y = to_categorical(Y)
print(onehot_Y)
#exit()

# 자연어처리 >> 조사, 감탄사 등 삭제하기
# 토큰을 만들어줌 / 형태소 단위로 잘라줌 >> 피팅 후 딕셔너리를 가짐
okt = Okt()
# okt_morph_X = okt.morphs(X[7], stem=True)
# print(okt_morph_X)

# 전체 데이터 자연어처리
for i in range(len(X)):
    X[i] = okt.morphs(X[i], stem=True)
# print(X[:10])

# 형태소로 나눠진것들 중 조사&한글자 제거(의미이해에 불피요한것)
# 불용어(stopwords) >> 조사, 감탄사, 대명사 등 어떠한 카테고리에도 다 나오는것
stopwords = pd.read_csv('./crawling_data/stopwords.csv', index_col=0)

for j in range(len(X)):
    words = []
    for i in range(len(X[j])):
        if len(X[j][i]) > 1:  # 한글자 단어 버리기
            if X[j][i] not in list(stopwords['stopword']):  # 조사 버리기
                words.append(X[j][i])
    X[j] = ' '.join(words)  # 다시 문장으로 합치기

# print(X)
# print(words)
# exit()

# 토큰화 >> 형태소 단위로 끊기
# 라벨이라 스케일링 작업은 하지 않음
# 토크나이저는 0을 사용하지 않음
token = Tokenizer()
token.fit_on_texts(X)
tokend_X = token.texts_to_sequences(X)
wordsize = len(token.word_index) + 1  # 단어 길이 알고 싶을때 >> 모델한테 전체 단어 개수를 줘야해서 필요함
print(tokend_X)
print(token.word_index)  #토큰의 단어사전 >> 딕셔너리형태

#토크나이저 저장
with open('./models/movies_token_0602.pickle', 'wb') as f:
    pickle.dump(token, f)

# #모델 입력 사이즈 맞춰주기 >> 가장 긴 문장을 기준으로 모자란 곳에는 0으로 채우기
# #가장 먼저 가장 긴 문장의 len max 찾기
max = 0
for i in range(len(tokend_X)):
    if max < len(tokend_X[i]):
        max = len(tokend_X[i])
print(max)
# #max값에 맞춰서 부족한 곳 앞부터 0으로 채우기
X_pad = pad_sequences(tokend_X, max)
print(X_pad)

# train_test_split
X_train, X_test, Y_train, Y_test = train_test_split(X_pad, onehot_Y, test_size=0.2)
print(X_train.shape, Y_train.shape)
print(X_test.shape, Y_test.shape)
exit()

# 저장
xy = X_train, X_test, Y_train, Y_test
np.save('./crawling_data/movies_max_{}_wordsize_{}_0602'.format(max, wordsize), xy)
