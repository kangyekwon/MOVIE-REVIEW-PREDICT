import pandas as pd
import glob
import datetime


#경로받아오기
data_path = glob.glob('./crawling_data/*')
#print(data_path)


#파일합치기
df = pd.DataFrame()
for path in data_path:
    df_temp = pd.read_csv(path)
    df = pd.concat([df, df_temp])

df.dropna(inplace=True)   #혹시모를 NaN값 제거
df.reset_index(inplace=True, drop=True)  #drop=True>>인덱스있는 값일때주면됨
print(df.head())
print(df.tail())
print(df['category'].value_counts())
df.info()
df.to_csv('./crawling_data/naver_news_titles_{}.csv'.format(datetime.datetime.now().strftime('%Y%m%d')), index=False)


# 에러 없었을 때
# df = pd.read_csv('./crawling_data/crawling_data.csv')
# df_headline = pd.read_csv('./crawling_data/naver_headline_news_20220525.csv')
# df_all = pd.concat([df, df_headline])
#
# print(df_all.head())
# print(df_all.tail())
# print(df_all['category'].value_counts())
# df_all.info()
# df_all.to_csv('./crawling_data/naver_news_titles_{}.csv'.format(
#     datetime.datetime.now().strftime('%Y%m%d')), index=False)
