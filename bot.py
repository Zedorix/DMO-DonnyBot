import discord
from discord.ext import commands
import asyncio
from dotenv import load_dotenv
import os

intents = discord.Intents.default()
intents.messages = True
intents.dm_messages = True
intents.message_content = True  # MUST ENABLE THIS IN DISCORD DEVELOPER PORTAL TOO

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

bot = commands.Bot(command_prefix='!', intents=intents)

initial_extensions = [ #if adding commands initial them here
    "cogs.register",
    "cogs.deleteaccount",
    "cogs.changepassword",
    "cogs.resetsecondpassword",
    "cogs.username",
    "cogs.email",
    "cogs.changeusername"
]

@bot.event
async def on_ready():
    print(f"✅ Bot is ready. Logged in as {bot.user}")
    print(f"Registered commands: {[cmd.name for cmd in bot.commands]}")

async def main():
    for ext in initial_extensions:
        try:
            await bot.load_extension(ext)  # ✅ must await
            print(f"Loaded: {ext}")
        except Exception as e:
            print(f"❌ Failed to load {ext}: {e}")

    await bot.start(TOKEN)

if __name__ == "__main__":
    asyncio.run(main())