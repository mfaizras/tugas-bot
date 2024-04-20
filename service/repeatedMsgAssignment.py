from models.TugasModel import TugasModel
from datetime import datetime
from dateutil.parser import parser
from dateutil.relativedelta  import relativedelta
import sched
import time
import pytz
import os
from dotenv import load_dotenv
from service.MessageEmbedService import MessageEmbedService
import discord

class repeatedMsgService:
    tugas = TugasModel()
    scheduler = sched.scheduler(time.time, time.sleep)

    def __init__(self) -> None:
          load_dotenv()

    def get_time_difference(self,deadline):
        deadline = datetime.fromisoformat(deadline).replace(tzinfo=pytz.timezone(os.getenv('TIMEZONE')))
        timeNow = datetime.now(pytz.timezone(os.getenv('TIMEZONE')))
        # timeNow = pytz.timezone(os.getenv('TIMEZONE')).localize(timeNow)

        print(deadline)
        print(timeNow)

        time_difference = deadline - timeNow
        return time_difference

    def get_assignment_to_notif(self):
        assignmentList = self.tugas.get_upcoming_tugas()
        assignmentToNotif = []
        for i, course in enumerate(assignmentList):
            
            time_difference = self.get_time_difference(course.deadline)
            time_difference_minutes = time_difference.total_seconds() // 60
            time_difference_hour = time_difference.total_seconds() // 3600
            time_difference_days = time_difference.days
            # print(time_difference_minutes)

            if time_difference_minutes > 0 and 58 <= time_difference_minutes <= 62: #check if under 1 hour
                    assignmentToNotif.append(course)
            elif time_difference_hour > 0 and 358 <= time_difference_minutes <= 360: # check deadline in 6 hour with tolerance 2 minute 
                    assignmentToNotif.append(course)
            elif time_difference_hour > 0 and 718 <= time_difference_minutes <= 722: # check deadline in 12 hour with tolerance 2 minute
                    assignmentToNotif.append(course)
            elif time_difference_hour > 0 and 1438 <= time_difference_minutes <= 1442: # check deadline in 24 hour with tolerance 2 minute
                    assignmentToNotif.append(course)
        # print(assignmentToNotif)
        return assignmentToNotif
    
    def get_new_assignment(self):
        assignmentList = self.tugas.get_tugas_not_send()
        assignmentToNotif = []
        for i, course in enumerate(assignmentList):
           assignmentToNotif.append(course)
        return assignmentToNotif
    
    def get_embed(self):
        assignment_list = self.get_assignment_to_notif()
        if assignment_list != []:
            embed = []
            embedObj = MessageEmbedService()
            for i,course in enumerate(assignment_list):
                embedTemp = embedObj.embed_tugas(course)
                embed.append(embedTemp)
        else :
            embed = []
        return embed
    
    def get_embed_new_assignment(self):
        model = TugasModel()
        assignment_list = self.get_new_assignment()
        if assignment_list != []:
            embed = []
            embedObj = MessageEmbedService()
            for i,course in enumerate(assignment_list):
                embedTemp = embedObj.embed_tugas(course)
                embed.append(embedTemp)
        else :
            embed = []
        model.update_notified(assignment_list)
        return embed
    