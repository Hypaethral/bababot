import os

import discord
import random
import datetime
from discord.ext import commands
from croniter import croniter

from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='~', intents=intents)

@bot.command()
async def vgn_bulk_clear(ctx: commands.Context):
    await ctx.message.add_reaction("👀")
    events = await ctx.guild.fetch_scheduled_events()
    for event in events:
        await event.delete(reason = "bulk clear command")
    await ctx.send('done!')

@bot.command()
async def vgn_bulk_create(ctx: commands.Context):
    await ctx.message.add_reaction("👀")
    # todo: check for existing events count
    now = discord.utils.utcnow()
    satCron = "0 1 * * sun#1,sun#2"
    wedCron = "0 23 * * wed#3,wed#4"
    satIter = croniter(satCron, now)
    wedIter = croniter(wedCron, now)
    for i in range(50):
        await schedule(ctx.guild, satIter.get_next(datetime.datetime))
        await schedule(ctx.guild, wedIter.get_next(datetime.datetime))
    await ctx.send("done!")

async def schedule(guild, time):
    await guild.create_scheduled_event(
        name = "VGN NIGHT",
        description = "Rockem Sockem",
        start_time = time,
        entity_type = discord.EntityType.voice,
        channel = random.choice(guild.voice_channels)
    )

bot.run(TOKEN)