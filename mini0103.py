import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from konlpy.tag import Okt
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.utils import to_categorical
import pickle

pd.set_option('display.unicode.east_asian_width', True)
df = pd.read_csv('./crawling_data/samples.csv')
# print(df.head())
# df.info()

X = df['sentence']  #입력
Y = df['movie']  #출력

#라벨엔코딩
encoder = LabelEncoder()
labeled_Y = encoder.fit_transform(Y)
#print(labeled_Y[:3])
label = encoder.classes_
#print(label)

#엔코더저장
with open('./models/samples_encoder.pickle', 'wb') as f:
    pickle.dump(encoder, f)

#원핫엔코딩
onehot_Y = to_categorical(labeled_Y)
print(onehot_Y)

#자연어처리(X처리)
okt = Okt()  #토큰을 만들어줌 / 형태소 단위로 잘라줌 >> 피팅 후 딕셔너리를 가짐
# okt_morph_X = okt.morphs(X[7], stem=True)
# print(okt_morph_X)

#전체 데이터 자연어처리
for i in range(len(X)):
    X[i] = okt.morphs(X[i], stem=True)
#print(X[:10])

#형태소로 나눠진것들 중 조사&한글자 제거(의미이해에 불피요한것)
#불용어(stopwords) >> 조사, 감탄사, 대명사 등 어떠한 카테고리에도 다 나오는것
stopwords = pd.read_csv('./crawling_data/stopwords.csv', index_col=0)

for j in range(len(X)):
    words = []
    for i in range(len(X[j])):
        if len(X[j][i]) >1 :  #한글자단어 버리기
            if X[j][i] not in list(stopwords['stopword']):  #조사 버리기
                words.append(X[j][i])
    X[j] = ' '.join(words)  #다시 문장으로 합치기

#print(X)
#print(words)

#토큰으로 바꾸기 >> 문자를 숫자로 >> 특정 형태소를 int값으로 라벨링(딕셔너리)
#라벨이라 스케일링 작업은 하지 않음
#토크나이저는 0을 사용하지 않음
token = Tokenizer()
token.fit_on_texts(X)
tokend_X = token.texts_to_sequences(X)
wordsize = len(token.word_index)+1  #단어 길이 알고 싶을때 >> 모델한테 전체 단어 개수를 줘야해서 필요함
print(tokend_X)
print(token.word_index)  #토큰의 단어사전 >> 딕셔너리형태

#토크나이저 저장
with open('./models/samples_token.pickle', 'wb') as f:
    pickle.dump(token, f)

#모델 입력 사이즈 맞춰주기 >> 가장 긴 문장을 기준으로 모자란 곳에는 0으로 채우기
#가장 먼저 가장 긴 문장의 len max 찾기
max = 0
for i in range(len(tokend_X)):
    if max < len(tokend_X[i]):
        max = len(tokend_X[i])
#print(max)
#max값에 맞춰서 부족한 곳 앞부터 0으로 채우기
X_pad = pad_sequences(tokend_X, max)
print(X_pad)

#train_test_split
X_train, X_test, Y_train, Y_test = train_test_split(X_pad, onehot_Y, test_size=0.1)
print(X_train.shape, Y_train.shape)
print(X_test.shape, Y_test.shape)

#저장
xy = X_train, X_test, Y_train, Y_test
np.save('./crawling_data/samples_max_{}_wordsize_{}'.format(max, wordsize), xy)