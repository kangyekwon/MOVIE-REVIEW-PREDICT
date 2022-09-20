from bs4 import BeautifulSoup
import requests
import re
import pandas as pd
import datetime

category = ['Politics', 'Economic', 'Social', 'Culture', 'World', 'IT']

url = 'https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=100'
#경제url = 'https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=101'

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36'}

df_titles = pd.DataFrame()

#6개 카테고리 헤드라인 긁어오기
for i in range(6):
    url = 'https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=10{}'.format(i)
    response = requests.get(url, headers=headers)
    # print(response)
    # print(list(response))
    # print(type(response))

    # 제목만 뽑아내기
    soup = BeautifulSoup(response.text, 'html.parser')
    # print(soup)
    title_tags = soup.select('.cluster_text_headline')
    #print(title_tags[0].text)

    titles = []
    for title_tag in title_tags:
        title = re.compile('[^가-힣]').sub('', title_tag.text)
        # 헤드라인 문장부호 제거 & 형태소단위로 분류+조사제거
        # 한글만 남기고 제거(숫자,영어,문장부호)
        # ^ >> '제외하고'라는 의미(정규표현식)
        titles.append(title)

    df_section_titles = pd.DataFrame(titles, columns=['titles'])
    df_section_titles['category'] = category[i]
    df_titles = pd.concat([df_titles, df_section_titles], axis='rows', ignore_index=True)


print(df_titles.head())
df_titles.info()
print(df_titles['category'].value_counts())

df_titles.to_csv('./crawling_data/naver_headline_news_{}.csv'.format(datetime.datetime.now().strftime('%Y%m%d')), index=False)