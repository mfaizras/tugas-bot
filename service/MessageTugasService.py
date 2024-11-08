import discord
from service.newRepeatedMsgAssignment import repeatedMsgService
import datetime
import os
from service.SystemMessage import SystemMessage
from models.TugasModel import TugasModel

class MessageTugasService:
    def __init__(self,bot:discord) -> None:
        self.bot = bot

    async def create_new_channel(self,guild,channel_name):
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=True),
            guild.me: discord.PermissionOverwrite(read_messages=True)
        }

        new_channel = await guild.create_text_channel(channel_name, overwrites=overwrites)
        SystemMessage().log(f"Service Assignment Repeated Message Complete {guild.name}")

        return new_channel
    
    async def send_repeated_message(self):
        message_automation = repeatedMsgService()
        embedList = message_automation.get_embed()
        if embedList != []:
            target_channel_name = os.getenv("CHANNEL_NAME")

            for guild in self.bot.guilds:
                target_channel = discord.utils.get(guild.channels, name=target_channel_name)
                if target_channel == None:
                    target_channel = await self.create_new_channel(guild,target_channel_name)

                if target_channel:
                    message = ""
                    message += "***Reminder***\n"
                    await target_channel.send(message)
                    for i, embed in enumerate(embedList):
                        await target_channel.send(embed=embed)
        SystemMessage().log("Service Assignment Repeated Message Complete")

    async def notify_new_assignment(self):
        message_automation = repeatedMsgService()
        model = TugasModel()
        embedList = message_automation.get_embed_new_assignment()
        if embedList != []:
            target_channel_name = os.getenv("CHANNEL_NAME")

            for guild in self.bot.guilds:
                target_channel = discord.utils.get(guild.channels, name=target_channel_name)
                if target_channel == None:
                    target_channel = await self.create_new_channel(guild,target_channel_name)

                if target_channel:
                    message = ""
                    message += "***Tugas Baru***\n"
                    await target_channel.send(message)
                    for i, embed in enumerate(embedList):
                        print(embed)
                        await target_channel.send(embed=embed)    

        SystemMessage().log("Service Assignment Repeated Message Complete")