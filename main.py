import os
import asyncio
import discord
from discord.ext import commands

TOKEN = os.getenv("DISCORD_BOT_TOKEN")

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True
intents.emojis_and_stickers = True

bot = commands.Bot(command_prefix="h!", intents=intents, help_command=None)

EXTENSIONS = [
    "cogs.core",
    "cogs.welcome",
    "cogs.tickets",
    "cogs.utility",
    "cogs.youtube_system",
    "cogs.emoji_tools",
    "cogs.moderation",
    "cogs.logging_system",
]

@bot.event
async def on_ready():
    print(f"私のクッキー is online: {bot.user} ({bot.user.id})")

async def main():
    if not TOKEN:
        raise ValueError("DISCORD_BOT_TOKEN is not set.")

    async with bot:
        for ext in EXTENSIONS:
            await bot.load_extension(ext)
        await bot.start(TOKEN)

if __name__ == "__main__":
    asyncio.run(main())
