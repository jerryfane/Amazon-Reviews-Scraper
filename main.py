from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
#from fake_useragent import UserAgent
import time
from random import randrange
import functions
import random
import os
import sqlite3



def open_Chrome():
    optionsChrome = Options()
    # ua = UserAgent()
    # userAgent = ua.random
    # print(userAgent)
    # optionsChrome.add_argument(f'user-agent={userAgent}')
    optionsChrome.add_argument("--window-size=1920,1080");
    optionsChrome.add_argument("--start-maximized");
    optionsChrome.add_argument('--headless')
    optionsChrome.add_argument('--disable-gpu')  # Last I checked this was necessary.
    #socks4_list = functions.get_proxy_list('socks4_list.txt')
    #random_num = randrange(len(socks4_list)-1)
    #proxy = socks4_list[random_num]
    #optionsChrome = functions.get_Chrome_proxy(optionsChrome, proxy)
    browser = webdriver.Chrome(options=optionsChrome)
    print('browser opened')
    #browser = webdriver.Firefox(firefox_profile=fp)
    return browser

def get_data_path(review_num):

    review_num = str(review_num)
    author_name_path = '/html/body/div[1]/div[3]/div[1]/div[1]/div/div[1]/div[5]/div[3]/div['+review_num+']/div/div/div[1]/a/div[2]/span'
    review_title_path = '/html/body/div[1]/div[3]/div[1]/div[1]/div/div[1]/div[5]/div[3]/div['+review_num+']/div/div/div[2]/a[2]/span'
    review_score_path = '/html/body/div[1]/div[3]/div[1]/div[1]/div/div[1]/div[5]/div[3]/div['+review_num+']/div/div/div[2]/a[1]/i'
    review_text_path = '/html/body/div[1]/div[3]/div[1]/div[1]/div/div[1]/div[5]/div[3]/div['+review_num+']/div/div/div[4]/span/span'
    review_date_path = '/html/body/div[1]/div[3]/div[1]/div[1]/div/div[1]/div[5]/div[3]/div['+review_num+']/div/div/span'

    data = {}
    data['author_name_path'] = author_name_path
    data['review_title_path'] = review_title_path
    data['review_score_path'] = review_score_path
    data['review_text_path'] = review_text_path
    data['review_date_path'] = review_date_path

    return data

def get_pages_data(browser, current_url):
    pages_data = []
    for num in range(2,12):
        temp_list = []
        review_data = get_data_path(num)
        for data_path in review_data:
            path = review_data[data_path]
            if data_path == 'review_score_path':
                #print(data_path)
                try:
                    x = browser.find_element_by_xpath(path).get_attribute("class")
                except:
                    #functions.PrintException()
                    x = 'Error ' + data_path
            else:
                try:
                    x = browser.find_element_by_xpath(path).text
                except:
                    #functions.PrintException()
                    x = 'Error ' + data_path
            temp_list.append(x)
            #time.sleep(0.1)
        pages_data.append(temp_list)

    pages_data = check_pages_data(pages_data, browser, current_url)
    return pages_data

def check_pages_data(pages_data, browser, current_url):
    score = 0
    for data in pages_data:
        if data == ['Error author_name_path', 'Error review_title_path', 'Error review_score_path', 'Error review_text_path', 'Error review_date_path']:
            score += 1
    print('Score is '+str(score))
    if score > 8:
        time.sleep(0.5)
        browser.close()
        #browser = open_Chrome()
        browser.get(current_url)
        browser.execute_script("window.scrollTo(0, 500);")
        time.sleep(0.5)
        pages_data = get_pages_data(browser, current_url)
    return pages_data

def get_url(url, page_num):
    url_complete = url+'&pageNumber='+str(page_num)
    return url_complete


def save_data(con, cur, pages):
    tuple_row = [tuple(row) for row in pages]
    cur.executemany("INSERT INTO reviews VALUES (?,?,?,?,?)", (tuple_row))
    #Please note that we now executemany outside of the inner loop
    con.commit()


def main(folder_path, database_name, url, start_page, end_page):
    con = sqlite3.connect(database_name)
    cur = con.cursor()

    cur.execute('CREATE TABLE IF NOT EXISTS reviews (author, title, score, text, place_date)')

    browser = open_Chrome()

    for page_num in range(start_page, end_page+1):
        print("Current Page: "+str(page_num))
        current_url = get_url(url, page_num)
        browser.get(current_url)
        browser.execute_script("window.scrollTo(0, 500);")
        time.sleep(1)

        pages = get_pages_data(browser, current_url)
        #for i in pages:
            #print(i)

        save_data(con, cur, pages)
