from discord.ext import commands,tasks
from service.Vclass import VclassService as Vclass
import datetime
import asyncio
from service.MessageEmbedService import MessageEmbedService
from models.TugasModel import TugasModel
from service.MessageTugasService import MessageTugasService
from service.SystemMessage import SystemMessage
import os
from dotenv import load_dotenv
from runScrapper import runScrapper

class Tugas(commands.Cog):
	def __init__(self, bot):
		self.bot = bot # sets the bot variable so we can use it in cogs
		self.serviceTugas = MessageTugasService(self.bot)
		load_dotenv()

	@commands.Cog.listener()
	async def on_guild_join(self,guild):
		channel_name = os.getenv("CHANNEL_NAME")
		channel_exists = any(channel.name == channel_name for channel in guild.channels)

		if not channel_exists:
			create_channel = await self.serviceTugas.create_new_channel(guild,channel_name)
			create_channel.send("Hello From Bot!")
	
	@commands.Cog.listener()
	async def on_ready(self):
		repEvery = 5
		now = datetime.datetime.now()
		current_hour = datetime.datetime.now().hour
		current_minute = datetime.datetime.now().minute
		timeDif = repEvery-(current_minute%repEvery)
		next_time = datetime.datetime(year=datetime.datetime.now().year,month=datetime.datetime.now().month,day=datetime.datetime.now().day,hour=current_hour,minute=current_minute+timeDif,second=00,microsecond=00)
		
		time_difference =   next_time - now

		minutes_to_wait = time_difference.total_seconds()
		
		self.scrapeTugas.start()
		await asyncio.sleep(minutes_to_wait)
		self.send_message.start()

	@tasks.loop(minutes=30,reconnect=True)
	async def scrapeTugas(self):
		SystemMessage.log("Task for Scraping Tugas")
		runScrapper.scrape_assignment()

	@tasks.loop(minutes=5,reconnect=True) 
	async def send_message(self):
		SystemMessage.log("Checking Upcoming Task, Repeated Service")
		await self.serviceTugas.send_repeated_message()
		
	@commands.command(name='tugas', help='Show List Upcoming Assignment')
	async def tugas(self, ctx):
		tugas = TugasModel()
		embedService = MessageEmbedService()
		datas = tugas.get_upcoming_tugas()

		print(type(ctx))

		countDatas = len(datas)
		if countDatas == 0:
			await ctx.send(f"Tidak Ada tugas dalam Waktu Dekat, Selamat Beristirahat :person_in_bed:")
			return

		await ctx.send(f"**Terdapat {countDatas} Tugas yang akan datang**")
		for i, data in enumerate(datas):
			await ctx.send(embed=embedService.embed_tugas(data))




async def setup(bot):
	await bot.add_cog(Tugas(bot))