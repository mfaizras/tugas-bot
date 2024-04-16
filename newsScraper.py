from service.NewsBaak import NewsBaak
from service.NewsStudentsite import NewsStudentsite
import os
from dotenv import load_dotenv
from models.NewsModel import *
class ScraperNews:
    def __init__(self):
        load_dotenv()
        self.newsBaak = NewsBaak()
        self.newsStudentSite = NewsStudentsite()

    def runScrape(self):
        datas = self.newsBaak.get_data_all() + self.newsStudentSite.get_data_all(100)
        model = NewsHandler()
        model.add_data(datas)
