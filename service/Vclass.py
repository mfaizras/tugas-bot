from scraper.MoodleScraper import MoodleScraper
import os
from dotenv import load_dotenv
class VclassService:
    def __init__(self):
        load_dotenv()
        self.url = "https://v-class.gunadarma.ac.id/"
        self.email = os.getenv("VCLASS_MAIL")
        self.password = os.getenv("VCLASS_PASS")
        self.vclass = MoodleScraper(url=self.url, email=self.email, password=self.password)

    def getAssignmentToday(self):
        return self.vclass.getAssignmentToday()
    
    def getAssignmentByTimeStamp(self, timestamp:str):
        return self.vclass.getAssignmentByTimeStamp(timestamp)
    
    def getAssignmentByDate(self, date:str):
        return self.vclass.getAssignmentByDate(date)
    
    def getAssigmentAreNotYetDue(self):
        return self.vclass.getAssigmentAreNotYetDue()
    