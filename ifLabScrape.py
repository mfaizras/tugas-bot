from scraper.MoodleScraper1 import MoodleScraper
import os
from dotenv import load_dotenv
from models.TugasModel import TugasModel,TugasDataHandler
class ScraperTugas:
    def __init__(self):
        load_dotenv()
        self.url = os.getenv("IFLAB_URL")
        self.email = os.getenv("IFLAB_MAIL")
        self.password = os.getenv("IFLAB_PASS")
        self.vclass = MoodleScraper(url=self.url, email=self.email, password=self.password)

    def runScrape(self):
        datas = self.vclass.getAssigmentAreNotYetDue()
        tempData = []
        model = TugasModel()
        for i,data in enumerate(datas):
            tempData.append(data.tugas_data_handler("IFLAB"))
        model.add_data(tempData)
