from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
import pandas as pd
import re
import time
import datetime


category = ['Vege', 'Fruit', 'Fish', 'Meat', 'Drinks', 'Snack', 'Bakery']


url = 'https://www.kurly.com/shop/goods/goods_list.php?category=907'

options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('lang=ko_KR')  #브라우저 언어설정 - 한국어로
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')  #리눅스에서 쓸때 필요
options.add_argument('disable-gpu')
driver = webdriver.Chrome('./chromedriver', options=options)


df_titles = pd.DataFrame()

for i in range(7, 16):
    titles = []

    url = 'https://www.kurly.com/shop/goods/goods_list.php?category=90{}'.format(i)
    driver.get(url)
    time.sleep(0.2)  #로딩시간 >> delay시킴

        #이중for문 >> 기사제목 20개씩 긁어오기 위해 사용
    for k in range(1, 30):
        x_path = '//*[@id="goodsList"]/div[2]/div/ul/li[k]/div/a/span[1]'.format(k)


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
            # except:
            #     try:
            #         x_path = '//*[@id="goodsList"]/div[2]/div/ul/li[k]/div/a/span[1]'.format(k)  #이미지가 없는 기사제목 긁어오기
            #         title = re.compile('[^가-힣]').sub('', title)
            #         titles.append(title)
            #     except:
            #         print('no such element')
        # error case2
            except StaleElementReferenceException as e:
                print(e)
                print(category[i], 'page', k)
        # error case3
        except:
            print('error')

    #20개의 기사제목 30페이지마다 저장 >> 기사제목 600개
    if i % 30 == 0 :   #30페이지마다 저장+페이지표시(처음부터 몇p까지인지)
        df_section_titles = pd.DataFrame(titles, columns=['titles'])
        df_section_titles['category'] = category[i]
        df_titles = pd.concat([df_titles, df_section_titles], ignore_index=True)
        df_section_titles.to_csv('./crawling_data/crawling_data_{}.csv'.format(category[i]), index=False)
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