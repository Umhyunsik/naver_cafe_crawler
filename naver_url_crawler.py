from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
from selenium.common.exceptions import NoSuchElementException
import pymysql
import sys
import re
import time
def findnotindb(p):
    first_check=20
    while True:
        url=driver.find_element_by_xpath("/html/body/div[3]/div/div/div[4]/div/ul/li[%s]/a[1]"%(first_check)).get_attribute("href")
        # already in db check
        article_id=int(p.findall(url)[0])
        sql4= "select id from post_tab where article_id={0}".format(article_id)
        curs.execute(sql4)
        returnvalue=curs.fetchone()

        if (returnvalue)!=None:
            #print("already in db")
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(5)
            driver.find_element_by_xpath("/html/body/div[3]/div/div/div[4]/div/div/a").click()
            first_check+=20
            time.sleep(10)

        else:
                
            return first_check-20

#driveropen

driver = webdriver.Chrome('./chromedriver')

driver.get('https://m.cafe.naver.com/ca-fe/web/cafes/19943558/menus/64')
time.sleep(10)
print("until page open waiting")
conn = pymysql.connect(host='localhost', port=3306, user='root', password='',\
                      db='', charset='utf8mb4')
curs = conn.cursor()
max_picture=20


p=re.compile(r'articleid=([0-9]+)')
p1=re.compile(r'menuid=([0-9]+)')

gofind=0
posts=0
flag=False


if start==0:
    start=1


max_picture=start+20
while True:
    print(posts,"crawling 된 post 개수 ")
    if gofind==7:
        # 위에 새로운 post들이 들어와 7번이상 db에 있는것들이 발견되면 다시 crawling된 곳까지 페이지 내리면서 20개씩 확인 
        start=findnotindb(p)
        gofind=0
    try:

        temp=driver.find_element_by_xpath("/html/body/div[3]/div/div/div[4]/div/ul/li[%s]/a[1]/strong"%(start+1)).text
 
    except:

        driver.find_element_by_xpath("/html/body/div[3]/div/div/div[4]/div/div/a").click()
        time.sleep(5)
        continue

    for i in range (start,max_picture):
        
        title=driver.find_element_by_xpath("/html/body/div[3]/div/div/div[4]/div/ul/li[%s]/a[1]/strong"%(i)).text
        url=driver.find_element_by_xpath("/html/body/div[3]/div/div/div[4]/div/ul/li[%s]/a[1]"%(i)).get_attribute("href")
        article_id=int(p.findall(url)[0])
        menu_id=int(p1.findall(url)[0])
        q=driver.find_element_by_xpath("/html/body/div[3]/div/div/div[4]/div/ul/li[%s]/a[1]"%(i)).text
        title=title.replace("'","\\'").replace('"','\\"')
        if q in '20.08': # 몇월 까지 crawling 했다면 나가기 
            flag=True
            break

        time.sleep(3)
        
        # already in db check
        sql4= "select id from post_tab where article_id={0}".format(article_id)
        curs.execute(sql4)
        returnvalue=curs.fetchone()
        
        if (returnvalue)!=None:
            gofind+=1
            print("already in db")
            continue
            
        else:
            
            sql = "insert into post_tab(menu_id,article_id,post_url,title) \
            values ({0}, {1}, {2},{3})".format(menu_id,article_id,"'"+ url+"'","'"+title+"'")
            curs.execute(sql)
            conn.commit()
            time.sleep(5)
            posts+=1
            
    if flag==True:
        break
        
    start+=20
    max_picture+=20
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(5)
    driver.find_element_by_xpath("/html/body/div[3]/div/div/div[4]/div/div/a").click()
    time.sleep(10)
    
conn.close()