from selenium import webdriver
import pymysql
import sys
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
from selenium.common.exceptions import NoSuchElementException
import re

#driveropen
driver = webdriver.Chrome('./chromedriver')

conn = pymysql.connect(host='localhost', port=3306, user='root', password='',\
                      db='', charset='utf8mb4')
curs = conn.cursor()

time.sleep(10)
while True:
    sql4= "select post_url from post_tab where crawl_flag=0 limit 1"
    curs.execute(sql4)
    returnvalue=curs.fetchone()
    url=returnvalue[0]
    p=re.compile(r'articleid=([0-9]+)')
    article_id=int(p.findall(url)[0])
    try:
        driver.get(url)
        time.sleep(15)
        post_reg_date=driver.find_element_by_xpath("/html/body/div[3]/div/div/div[2]/div[1]/div[1]/div/div[2]/div[2]/span[1]").text
    except:
        #게시글 사라짐
        sql = "update post_tab set crawl_flag=-1 where article_id={0}".format(article_id)
        curs.execute(sql)
        conn.commit()
        
        time.sleep(5)
        continue
    
    post_reg_date=post_reg_date.replace("작성일\n","")
    views=driver.find_element_by_xpath("/html/body/div[3]/div/div/div[2]/div[1]/div[1]/div/div[2]/div[2]/span[2]").text
    views=views.replace("조회 ","")

    if ',' in views:
        views=views.replace(",",'')
    elif '만' in views and '.' in views:
        left,right=views.split(".")
        right=right.replace("만","000")
        views=left+right
    elif '만' in views:
        views=views.replace("만","0000")

    try:
        views=int(views)
    except:
        driver.find_element_by_xpath("/html/body/div[3]/div/div[1]/div[2]/div/div[2]/div/a[1]").click()
        continue
    html = driver.page_source 
    soup = BeautifulSoup(html, "lxml")
    try:
                
        text=driver.find_element_by_xpath("/html/body/div[3]/div/div/div[2]/div[1]/div[3]").text
        #text=text.replace("● 모든 게시물은 사진 + 글 첨부 필수 https://cafe.naver.com/casuallydressed/44062 매뉴얼 확인 부탁드립니다.","")
        post_content=text.replace("'","\\'").replace('"','\\"')
       
    except:
        mydivs = soup.findAll("div", {"class": "se-main-container"})
        #text=mydivs[0].text.replace("\n\n\n\n\n● 모든 게시물은 사진 + 글 첨부 필수 https://cafe.naver.com/casuallydressed/44062 매뉴얼 확인 부탁드립니다.","")
        text=text.replace("\n\n\n\n ","\n")
        text=text.replace("\n\n\n\n\n\n\n\n\n\n\n\n","\n")
        post_content=text.replace("\n\n\n\n\n","").replace("'","\\'").replace('"','\\"')

    try:
        user_nick = soup.findAll("span", {"class": "end_user_nick"})
        user_nick=user_nick[0].text
    except:
        user_nick=driver.find_element_by_xpath("/html/body/div[3]/div/div/div[2]/div[1]/div[1]/div/div[2]/div[1]/a[1]/span/span").text
    user_nick=user_nick.replace("'","\\'").replace('"','\\"')

    sql = "update post_tab set user_id={0}, post_content={1},views={2},post_reg_date={3},crawl_flag=1 where article_id={4}".format("'"+user_nick+"'","'"+post_content+"'",views,"'"+post_reg_date+"'",article_id)
    curs.execute(sql)
    conn.commit()
    time.sleep(5)

conn.close()
