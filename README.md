
# 네이버 카페 게시판 크롤링

사용기술
+ selenium
+ beautifulsoup4
+ mysql

설치필요
+ pymysql
+ chromedriver

크롤러는 총 두개로 이루어져있다

### naver_url_crawler.py

+ 한 게시판 당 url을 긁어오는 크롤러 driver.get('https://m.cafe.naver.com/ca-fe/web/cafes/19943558/menus/64') 
+ 새롭게 post된 url들도있으니 위에서부터 내려오다가 일정 개수가 db안에 저장되어있다면 페이지를 내려서 20개씩 건너 뛰면서 db에 체크 

### naver_post_crawler.py

+ 위에서 모은 url들을 방문해서 게시글내용,작성자,조회수 등을 가져오는 크롤러 Db에 저장 

