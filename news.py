import requests 
from bs4 import BeautifulSoup


def lpage(word,ds,de):
  x= 0 
  while True: 

    k=10*x+1 
    URL=f"https://search.naver.com/search.naver?&where=news&query={word}&reporter_article=&pd=3&ds={ds}&de={de}&start={k}&refresh_start=0" #start 에 10개 간격으로
      #x 가 한계치를 넘어가면 계속 x 한계치 페이지나옴
    naver_search  =requests.get(URL) 

    naver_soup=BeautifulSoup(naver_search.text,"html.parser")

      #max_page=[]
    ten_page=[]

    #to_max_page=naver_soup.find("div",{"class":"title_desc all_my"})
    #print(to_max_page.find('span').string)

    pagination= naver_soup.find("div", {"class":"paging"})
    #print(pagination.get_text())
    if pagination is None:
      return None
      #print(str(pagination.find('a')["class"][0]))
    

    elif x%10 == 1:
        strong=int(pagination.find('strong').string)
        for page in pagination.find_all('a'):#[:-1]:    
            
            if len(page.get_text()) > 4:
              pass
            else:    
              ten_page.append(int(page.string))
        ten_page.insert(0,strong)
        ten_page.sort()
        
    else:
        strong=int(pagination.find('strong').string)
        for page in pagination.find_all('a'):#[1:-1]:#이전,다음페이지 제외
            
            if len(page.get_text()) > 4:
              pass
            else:    
              ten_page.append(int(page.string))
        ten_page.insert(x%10, strong)
        
        ten_page.sort()
    
    if len(ten_page) < 3:
      last_page = ten_page[-1]
      return last_page
    elif ten_page[-2] <= x:
      break
    else:
      #print(x,ten_page[-1])
      
      x+=1
    #ten_page[x]= x
  last_page=ten_page[-1]
  return last_page
  #last page 까지구하고 title에서 막힘(저 오류 해결))


def get_news(title):
  titles=title.find('dl').find('dt').find('a')["title"] 
  links=title.find('dl').find('dt').find('a')["href"]
  company=title.find('dl').find('dd').find("span",{"class":"_sp_each_source"}).string

  summary=title.find('dl').find_all('dd')
  summary=summary[1].get_text()
  img=title.find("div", {"class":"thumb"})
  if img is None:
    img="No image"
  else:
   img=img.find('a').find('img')["src"]
  

  return {'title':titles, 'company': company, 'summary':summary, 'links': links,'imgsrc': img}

 
        



def search_news(last_page,word,ds,de):

   news=[]
   for page in range(last_page):
    print(page)
    k=10*page+1 
    URL=f"https://search.naver.com/search.naver?&where=news&query={word}&reporter_article=&pd=3&ds={ds}&de={de}&start={k}&refresh_start=0" #start 에 10개 간격으로
      #x 가 한계치를 넘어가면 계속 x 한계치 페이지나옴
    naver_search =requests.get(URL) 

    naver_soup=BeautifulSoup(naver_search.text,"html.parser")

    find_title=naver_soup.find("ul",{"class":"type01"}).find_all('li')
    for title in find_title:
      if title.find('dl') == None:
        pass
      else:
        news.append(get_news(title))
   return news


def search_results(word,ds,de):
  if lpage(word,ds,de) is None:
    return None
  else:
    return search_news(lpage(word,ds,de),word,ds,de)