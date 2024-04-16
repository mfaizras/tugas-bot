import datetime
from typing import Optional
from bs4 import BeautifulSoup
import requests as r
from helpers.Text import Text
from models.NewsModel import NewsModel
from datetime import datetime

class NewsStudentsite(NewsModel):

    def get_data_all(self, limit=None) -> list['NewsModel'] | None:
        response = r.get("https://studentsite.gunadarma.ac.id/index.php/site/news")
        print(f"\033[85m{datetime.now()} \033[0m  \033[96m[LOG]\033[0m \033[32m Scraping https://studentsite.gunadarma.ac.id/index.php/site/news \033[0m")
        if response.status_code == 200:
            article_lists = []
            sp = BeautifulSoup(response.content, 'html.parser')
            content_boxes = sp.find_all('div', class_='content-box')
            i = 0
            for content_box in content_boxes:
                if limit != None and i > limit:
                    break
                article = {}
                article['title'] = content_box.find('h3', class_='content-box-header').get_text().strip()
                # article['url'] = f"https://studentsite.gunadarma.ac.id{content_box.find('a')['href']}"
                article['url'] = f"https://studentsite.gunadarma.ac.id{content_box.find('a', class_='btn btn-info')['href']}"
                article['id'] =  str(article['url']).split("/")[-1]
                article['body'] = content_box.find('div', class_='content-box-wrapper').text.strip()
                # article['date'] = content_box.find('div', class_='font-gray').text.strip()
                article['date'] = content_box.find('div', class_='font-gray').text.split("  ")[-1]
                article['source'] = "STUDENT SITE"
                article_lists.append(NewsModel(article))
                i+=1
                # print(article['id'])
            return article_lists
        else:
            return None
