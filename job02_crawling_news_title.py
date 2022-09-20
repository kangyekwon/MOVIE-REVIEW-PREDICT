from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
import pandas as pd
import re
import time
import datetime


category = ['Politics', 'Economic', 'Social', 'Culture', 'World', 'IT']
pages = [110, 110, 110, 78, 110, 66]
#카테고리별 페이지수 110p까지로 맞춤


url = 'https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=100#&date=%2000:00:00&page=1'

options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('lang=ko_KR')  #브라우저 언어설정 - 한국어로
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')  #리눅스에서 쓸때 필요
options.add_argument('disable-gpu')
driver = webdriver.Chrome('./chromedriver', options=options)


df_titles = pd.DataFrame()

for i in range(0, 6):
    titles = []

    for j in range(1, pages[i]+1):
        url = 'https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=10{}#&date=%2000:00:00&page={}'.format(i, j)
        driver.get(url)
        time.sleep(0.2)  #로딩시간 >> delay시킴

        #이중for문 >> 기사제목 20개씩 긁어오기 위해 사용
        for k in range(1, 5):
            for l in range(1, 6):
                x_path = '//*[@id ="section_body"]/ul[{}]/li[{}]/dl/dt[2]/a'.format(k, l)
                try:
                    title = driver.find_element_by_xpath(x_path).text
                    title = re.compile('[^가-힣]').sub('', title)   #한글 타이틀만 저장
                    titles.append(title)

                # error case1
                except NoSuchElementException as e:
                    time.sleep(0.5)
                    try:
                        title = driver.find_element_by_xpath(x_path).text
                        title = re.compile('[^가-힣]').sub('', title)
                        titles.append(title)
                    except:
                        try:
                            x_path = '//*[@id ="section_body"]/ul[{}]/li[{}]/dl/dt/a'.format(k, l)  #이미지가 없는 기사제목 긁어오기
                            title = re.compile('[^가-힣]').sub('', title)
                            titles.append(title)
                        except:
                            print('no such element')
                # error case2
                except StaleElementReferenceException as e:
                    print(e)
                    print(category[i], j, 'page', k*l)
                # error case3
                except:
                    print('error')

        #20개의 기사제목 30페이지마다 저장 >> 기사제목 600개
        if j % 30 == 0 :   #30페이지마다 저장+페이지표시(처음부터 몇p까지인지)
            df_section_titles = pd.DataFrame(titles, columns=['titles'])
            df_section_titles['category'] = category[i]
            df_titles = pd.concat([df_titles, df_section_titles], ignore_index=True)
            df_section_titles.to_csv('./crawling_data/crawling_data_{}_{}_{}.csv'.format(category[i], j-29, j), index=False)
            titles = []

    df_section_titles = pd.DataFrame(titles, columns=['titles'])
    df_section_titles['category'] = category[i]
    df_titles = pd.concat([df_titles, df_section_titles], ignore_index=True)
    df_titles.to_csv('./crawling_data/crawling_data_{}_last.csv'.format(category[i]), index=False)
    titles = []

df_section_titles = pd.DataFrame(titles, columns=['titles'])
df_section_titles['category'] = category[i]
df_titles = pd.concat([df_titles, df_section_titles], ignore_index=True)
df_titles.to_csv('./crawling_data/naver_titles_{}.csv'.format(datetime.datetime.now().strftime('%Y%m%d')), index=False)

driver.close()