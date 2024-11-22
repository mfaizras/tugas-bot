from typing import Optional
import requests as r
from bs4 import BeautifulSoup
from models.Course import Course
from datetime import datetime
import re
import time
import datetime
import json
from pathlib import Path

class MoodleScraper:
    def __init__(self,url : str,email :str,password:str):

        if url == None or email == None or password == None:
            raise ValueError("Setup Failed")
        
        url = url.strip()
        self.url = url if url[-1] == "/" else url+"/"

        self.calendar_url = url + "calendar/view.php"
        self.login_url = url + "login/index.php"
        self.dashboard_url = url + "my"

        self.cookies_path = "cookiedata" #Change This
        self.cookies_path =  self.cookies_path+".json"

        self.email = email
        self.password = password
        self.session = r.Session()

        cookie = self.readCookie()
        if cookie != "" and self.url in cookie:
            cookie = cookie[self.url] 
            cookieData = cookie
            self.session.cookies.update(cookieData)

        if self.__authenticate() == False:
            print(f"\033[85m{datetime.datetime.now()} \033[0m  \033[96m[LOG]\033[0m \033[32m Login Moodle Failed\033[0m")
            raise ValueError("Login Error! Make Sure email and Password are valid")
        else:
            print(f"\033[85m{datetime.datetime.now()} \033[0m  \033[96m[LOG]\033[0m \033[32m Login Moodle Success\033[0m")

    
    def __doLogin(self):
        print(f"\033[85m{datetime.datetime.now()} \033[0m  \033[96m[LOG]\033[0m \033[32m Attempt To Login on {self.login_url}\033[0m")
        res = self.session.get(self.login_url)
        cookie = res.cookies.get_dict()
        pattern = '<input type="hidden" name="logintoken" value="\w{32}">'
        token = re.findall(pattern, res.text)[0]
        token = re.findall('\w{32}', token)[0]
        payload = {'username': self.email, 'password': self.password, 'anchor': '', 'logintoken': token}
        response = self.session.post(self.login_url, cookies=cookie, data=payload)

        self.cookie = response.cookies.get_dict()
        if 'You are logged in as' in response.text:
            self.dumpCookie()
            return True
        else :
            return False
    
    def __checkAuth(self):
        checkReq = self.session.get(self.login_url)
        if 'You are logged in as' in checkReq.text:
            return True
        else :
            return False
        
    def __authenticate(self):
        checkAuth = self.__checkAuth()
        if checkAuth != True:
            return self.__doLogin()
        else :
            return checkAuth
        
    def getAssignmentByUrl(self, url: str)-> list['Course']:
        response = self.session.get(url)
        print(f"\033[85m{datetime.datetime.now()} \033[0m  \033[96m[LOG]\033[0m \033[32m Scraping {url}\033[0m")
        data: list['Course'] = []
        sp = BeautifulSoup(response.content, 'html.parser')
        allEvent = sp.find('div',class_='eventlist').find_all('div',class_="event")
        if allEvent == None:
            return data
        for event in allEvent:
            descriptionList = event.find('div',class_="description card-body").find_all('div',class_='row')
            dataTemp = {}
            dataTemp['title'] = event['data-event-title']
            dataTemp['course-id'] = event['data-course-id']
            dataTemp['event-id'] = event['data-event-id']
            dataTemp['data'] = []
            x = 0
            for description in descriptionList:
                desc = {}
                getDesc = description.find_all('div')
                desc['title'] = getDesc[0].contents[0]['title']
                if getDesc[1].find('a',href=True) != None:
                    desc['text'] = getDesc[1].text
                    desc['link'] = getDesc[1].find('a',href=True)['href']
                else :
                    desc['text'] = getDesc[1].text
                    desc['link'] = ""
                x+=1
                dataTemp['data'].append(desc)
            data.append(Course(dataTemp))
        return data
        
    
    def getAssignmentToday(self)-> list['Course']:
        url = f"{self.calendar_url}?view=day"
        return self.getAssignmentByUrl(url)
    
    def getAssignmentByTimeStamp(self,timestamp:str)-> list['Course']:
        url = f"{self.calendar_url}?view=day&time={timestamp}"
        return self.getAssignmentByUrl(url)
    
    def getAssignmentByDate(self,date:str=None):
        """Return an Assignemnt by Selected Date with Format : d/m/Y
        """
        if date == None:
            return self.getAssignmentToday()
        else:
            timestamp = time.mktime(datetime.datetime.strptime(date, "%d/%m/%Y").timetuple())
            return self.getAssignmentByTimeStamp(timestamp)
    
    def getAssigmentAreNotYetDue(self)-> list['Course']:
        url = f"{self.calendar_url}?view=upcoming"
        return self.getAssignmentByUrl(url)
    
    def doLogout(self):
        logout = self.session.get(self.dashboard_url)
        sp = BeautifulSoup(logout.content,'html.parser')
        logoutLink = sp.find("a",string='Log out',href=True)['href']

        response = self.session.get(logoutLink)

        # print(response.text)
        if "You are not logged in." in response.text:
            return "Successfully logged out"
        else :
            return "Failed To Logout"
    
    def readCookie(self):
        file_path = Path(self.cookies_path)

        if file_path.exists() and file_path.stat().st_size > 0:
            data = json.loads(file_path.read_text())
        else:
            data = {} 

        return data
    
    def dumpCookie(self):
        cookies = self.session.cookies.get_dict()
        cookiesData = self.readCookie()
        cookiesData[self.url] = cookies

        Path(self.cookies_path).write_text(json.dumps(cookiesData))