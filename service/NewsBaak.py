from datetime import datetime
from typing import Optional
from bs4 import BeautifulSoup
import requests as r
from helpers.Text import Text
from models.NewsModel import NewsModel

class NewsBaak(NewsModel):

    def get_data_all(self) -> list['NewsModel'] | None:
        response = r.get("https://baak.gunadarma.ac.id/berita")
        print(f"\033[85m{datetime.now()} \033[0m  \033[96m[LOG]\033[0m \033[32m Scraping https://baak.gunadarma.ac.id/berita\033[0m")
        if response.status_code == 200:
            article_lists = []
            sp = BeautifulSoup(response.content, 'html.parser')
            article_lists_scrap = sp.find_all('div', class_='post-news-body')
            for article_data in article_lists_scrap:
                h6 = article_data.find('h6')
                article = {}
                article['url'] = h6.find('a')['href']
                article['id'] = article['url'].split("/")[-1]
                article['title'] = h6.find('a').text
                article['body'] = article_data.find(class_='offset-top-5').find('p').text
                article['date'] = article_data.find('span', class_="text-middle inset-left-10 text-italic text-black").text
                article['source'] = "BAAK"
                article_lists.append(NewsModel(article))
            return article_lists
        else:
            return None
         
    def get_data_by_day(self) -> list['NewsModel'] | None:
        results = self.get_data_all()
        news = []
        for result in results:
            if result.date == datetime.now().strftime("%d/%m/%Y"):
                news.append(result)
            else:
                return
        return news
    
    def get_news_by_id(self, id:int) -> Optional['NewsModel'] | ValueError:
        url = f"https://baak.gunadarma.ac.id/berita/{id}"
        response = r.get(url)
        if response.status_code == 200:
            sp = BeautifulSoup(response.content, 'html.parser')
            news = sp.find('div', class_="cell-sm-8 cell-md-8 text-left")
            self.title = news.find('h3', class_='text-bold').text
            body = news.find_all_next(class_='offset-md-top-20')
            self.url = url
            self.date = body[0].find_all_next('ul')[0].find_all_next('li')[0].text
            self.body = Text().trim_text(body[1].text)
            self.source = "BAAK"
            return self
        else:
            return ValueError("News ID not found")
        