import os
import discord
from discord.ext import commands
import asyncio

intents = discord.Intents.all()

bot = commands.Bot(command_prefix=".p ", intents=intents)

async def load_extensions():
    # Load all cogs from the 'cogs' folder
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            await bot.load_extension(f'cogs.{filename[:-3]}')

# Event handler for on_ready
@bot.event
async def on_ready():
    try:
        print(f"{bot.user} logged in!")

        
        await bot.change_presence(activity=discord.Game(name="Testing API"))

    except Exception as e:
        print(f"An error occurred during on_ready: {str(e)}")

if __name__ == "__main__":
    BOT_TOKEN = 'YOUR_DISCORD_BOT_TOKEN'

    # Use asyncio.run() to run the asynchronous function in a synchronous context
    asyncio.run(load_extensions())

    bot.run(BOT_TOKEN)
