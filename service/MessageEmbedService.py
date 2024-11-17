from models.Course import Course
from models.TugasModel import TugasDataHandler
import discord
import datetime
import pytz
import os
from dotenv import load_dotenv

class MessageEmbedService():
    def get_time_difference(self,deadline):
        load_dotenv()
        deadline = datetime.datetime.fromisoformat(deadline).replace(tzinfo=pytz.timezone(os.getenv('TIMEZONE')))
        timeNow = datetime.datetime.now(pytz.timezone(os.getenv('TIMEZONE'))).replace(tzinfo=pytz.timezone(os.getenv('TIMEZONE')))

        time_difference = deadline - timeNow
        return time_difference
    
    def embed_tugas(self,course:TugasDataHandler):
        isOpens = course.title.split()[-1] == "opens"
        dlSign = "Deadline"
        dlText = "Akan Berakhir dalam"
        color = discord.Color.blue()

        if(isOpens):
            dlText = "Akan Dibuka dalam"
            dlSign = "Dibuka pada"
            color = discord.Color.from_rgb(0, 153, 51)
        time_difference = self.get_time_difference(course.deadline)
        time_difference_minutes = time_difference.total_seconds() // 60
        time_difference_hour = time_difference.total_seconds() // 3600
        time_difference_days = time_difference.days

        embed = discord.Embed(title=course.title, url=course.assignment_url, description=course.description, color=color)
        # embed.set_author(name=course.course_name +" - " + course.assignment_source, url=course.assignment_url, icon_url="https://blog-edutore-partner.s3.ap-southeast-1.amazonaws.com/wp-content/uploads/2020/05/25120309/logo-universitas-gunadarma.png")
        embed.set_author(name=course.course_name +" - " + course.assignment_source, url=course.assignment_url)
        embed.add_field(name=dlSign, value=datetime.datetime.strptime(course.deadline, "%Y-%m-%dT%H:%M:%S").strftime("%Y-%m-%d %H:%M") + " WIB", inline=True)
        if time_difference_minutes > 59:
            embed.add_field(name=dlText, value=str(time_difference_hour) + " Jam", inline=True)
        else :
            embed.add_field(name=dlText, value=str(time_difference_minutes) + " Menit", inline=True)
        return embed