from discord.ext import commands,tasks
import discord
from dotenv import load_dotenv
import os
import asyncio

# Create an instance of the bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='/', intents=intents)

@bot.event
async def on_ready():
	print(f'\033[96mLogged in as {bot.user.name} ({bot.user.id}) \033[0m')

async def load_extensions():
	for f in os.listdir("./cogs"):
		if f.endswith(".py"):
			await bot.load_extension("cogs." + f[:-3])

load_dotenv()
asyncio.run(load_extensions())
BOT_TOKEN = os.getenv("TOKEN_DISCORD")
bot.run(BOT_TOKEN)