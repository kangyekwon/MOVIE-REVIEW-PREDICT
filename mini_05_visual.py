import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import math
from matplotlib import font_manager, rc
import matplotlib

df = pd.read_csv('./crawling_data/movies.csv')
# df.info()
# RangeIndex: 9214 entries, 0 to 9213
# Data columns (total 3 columns):
#  #   Column    Non-Null Count  Dtype
# ---  ------    --------------  -----
#  0   movie     9214 non-null   object
#  1   sentence  9214 non-null   object
#  2   score     9214 non-null   int64

# 코멘트가 없는 리뷰 데이터(NaN) 제거
df_reviews = df.dropna()
# 중복 리뷰 제거
df_reviews = df_reviews.drop_duplicates(['sentence'])
# df_reviews.info()
# df_reviews.head(10)
# Int64Index: 9097 entries, 0 to 9213
# Data columns (total 3 columns):
#  #   Column    Non-Null Count  Dtype
# ---  ------    --------------  -----
#  0   movie     9097 non-null   object
#  1   sentence  9097 non-null   object
#  2   score     9097 non-null   int

# 영화 리스트 확인
movie_lst = df.movie.unique()
#print('전체 영화 편수 =', len(movie_lst))
#print(list(movie_lst))
# print(movie_lst[:10])
# 전체 영화 편수 = 1122
# ['그대가 조국' '괴테스쿨의 사고뭉치들' '삼진그룹 영어토익반' '박수건달' '범죄도시2' '닥터 스트레인지: 대혼돈의 멀티버스'
#  '녹색 광선' '버닝' '엽기적인 그녀' '조제, 호랑이 그리고 물고기들']

# 각 영화 리뷰 수 계산
cnt_movie = df_reviews.movie.value_counts()
# print(cnt_movie[:20])
# 범죄도시2                  3029
# 그대가 조국                 2953
# 닥터 스트레인지: 대혼돈의 멀티버스     451
# 유체이탈자                    80
# 안녕하세요                    70
# 피는 물보다 진하다               55
# 어부바                      51
# 자산어보                     47
# 야차                       46
# 리턴 투 파라다이스               43
# 사이버 지옥: N번방을 무너뜨려라       40
# 신비한 동물들과 덤블도어의 비밀        38
# 오마주                      38
# 모비우스                     36
# 연애 빠진 로맨스                30
# 배드 가이즈                   26
# 몬스터 싱어: 매직 인 파리          26
# 플레이그라운드                  26
# 공기살인                     23
# 히든                       23

# 각 영화 평점 분석
info_movie = df_reviews.groupby('movie')['score'].describe()
# print(info_movie.sort_values(by=['count'], axis=0, ascending=False))
#                       count       mean       std   min   25%   50%   75%   max
# movie
# 범죄도시2                3029.0   9.407395  1.575204   1.0  10.0  10.0  10.0  10.0
# 그대가 조국               2953.0   7.187944  4.062715   1.0   2.0  10.0  10.0  10.0
# 닥터 스트레인지: 대혼돈의 멀티버스   451.0   7.529933  2.662641   1.0   6.0   8.0  10.0  10.0
# 유체이탈자                  80.0   7.012500  2.848467   1.0   5.0   8.0  10.0  10.0
# 안녕하세요                  70.0   8.671429  2.110851   1.0   8.0  10.0  10.0  10.0
# ...                     ...        ...       ...   ...   ...   ...   ...   ...
# 불한당: 나쁜 놈들의 세상          1.0  10.000000       NaN  10.0  10.0  10.0  10.0  10.0
# 붉은 10월                  1.0   2.000000       NaN   2.0   2.0   2.0   2.0   2.0
# 뷰티 인사이드                 1.0   7.000000       NaN   7.0   7.0   7.0   7.0   7.0
# 뷰티풀 마인드                 1.0  10.000000       NaN  10.0  10.0  10.0  10.0  10.0
# 힘을 내요, 미스터 리            1.0   8.000000       NaN   8.0   8.0   8.0   8.0   8.0

# print(info_movie.sort_values(by=['count'], axis=0, ascending=False)[:15])
# exit()

Y = df['score']
# score 0~3(2) / 4~6(1) / 7~10(0)
for i in range(len(Y)):
    if 7 <= Y[i] <= 10:
        Y[i] = 0
    elif 4 <= Y[i] <= 6:
        Y[i] = 1
    else:
        Y[i] = 2
# print(df.groupby('score').size().reset_index(name = 'count'))
#    score  count
# 0      0   7160
# 1      1    562
# 2      2   1492

#top10 movies
top15 = df_reviews.movie.value_counts().sort_values(ascending=False)[:15]
top15_title = top15.index.tolist()
top15_reviews = df_reviews[df_reviews['movie'].isin(top15_title)]
# print(top10_title)
# ['범죄도시2', '그대가 조국', '닥터 스트레인지: 대혼돈의 멀티버스', '유체이탈자', '안녕하세요', '피는 물보다 진하다', '어부바', '자산어보', '야차', '리턴 투 파라다이스']
# print(top10_reviews.info())
# Int64Index: 6825 entries, 0 to 9213
# Data columns (total 3 columns):
#  #   Column    Non-Null Count  Dtype
# ---  ------    --------------  -----
#  0   movie     6825 non-null   object
#  1   sentence  6825 non-null   object
#  2   score     6825 non-null   int64

#-- 한글 폰트 사용 설정
font_path = "C:/Windows/Fonts/HYNAMM.ttf"
font = font_manager.FontProperties(fname=font_path).get_name()
rc('font', family=font)

#-- 그래프 마이너스 기호 표시 설정
matplotlib.rcParams['axes.unicode_minus'] = False

#상위 10개 영화에 대한 평균 평점을 시각화
movie_title = top15_reviews.movie.unique().tolist()    #-- 영화 제목 추출
avg_score = {}  #-- {제목 : 평균} 저장
for t in movie_title:
    avg = top15_reviews[top15_reviews['movie'] == t]['score'].mean()
    avg_score[t] = avg
plt.figure(figsize=(15, 10))
plt.title('영화 평균 평점 (top 15: 리뷰 수)\n', fontsize=25)
plt.xlabel('영화 제목')
plt.ylabel('평균 평점')
plt.xticks(rotation=20, fontsize=6)
for x, y in avg_score.items():
    color = np.array_str(np.where(y == max(avg_score.values()), 'forestgreen', 'lightgrey'))
    plt.bar(x, y, color=color)
    plt.text(x, y, '%.2f' % y,
             horizontalalignment='center',
             verticalalignment='bottom')
plt.show()
#exit()

#평점 분포도
#붉은 색 점선=평균
fig, axs = plt.subplots(5, 3, figsize=(10, 15))
fig.subplots_adjust(hspace=0.5)
axs = axs.flatten()
for title, avg, ax in zip(avg_score.keys(), avg_score.values(), axs):
    num_reviews = len(top15_reviews[top15_reviews['movie'] == title])
    x = np.arange(num_reviews)
    y = top15_reviews[top15_reviews['movie'] == title]['score']
    ax.set_title('\n%s (%d명)' % (title, num_reviews), fontsize=8)
    ax.set_ylim(0, 10.5, 2)
    ax.plot(x, y, 'o', markersize=3, color='seagreen')
    ax.axhline(avg, color='blue', linestyle='--')  # -- 평균 점선 나타내기
plt.show()
#exit()

#원형 차트
fig, axs = plt.subplots(3, 5, figsize=(15, 10))
fig.subplots_adjust(hspace=0.5)
axs = axs.flatten()
colors = ['#92d050', '#c5e0b4', '#e2f0d9']
# score 0~3(2) / 4~6(1) / 7~10(0)
labels=['0(7~10점)','1 (4~6점)','2 (0~3점)']
top15_reviews['score_bin'] = pd.cut(top15_reviews['score'], [0, 4, 7, 10], labels=[2, 1, 0])

for title,ax in zip(avg_score.keys(), axs):
    num_reviews = len(top15_reviews[top15_reviews['movie'] == title])
    values = top15_reviews[top15_reviews['movie'] == title]['score_bin'].value_counts()
    #print(values)
    ax.set_title('\n%s (%d명)' % (title, num_reviews) , fontsize=10)
    ax.pie(values,
           autopct='%1.1f%%',
           colors=colors,
           shadow=False,
           startangle=180,
           textprops={'size':8})
    ax.axis('equal')
plt.legend(labels)
plt.show()