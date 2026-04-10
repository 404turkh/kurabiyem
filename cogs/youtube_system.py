import re
import aiohttp
import feedparser
import discord
from discord.ext import commands, tasks
from utils.storage import load_config, get_guild_config, update_guild_config

CHANNEL_ID_RE = re.compile(r"/channel/(UC[a-zA-Z0-9_-]+)")

async def resolve_youtube_feed_url(channel_url: str):
    channel_match = CHANNEL_ID_RE.search(channel_url)
    if channel_match:
        channel_id = channel_match.group(1)
        return f"https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}"

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(channel_url) as resp:
                html = await resp.text()

        match = re.search(r'"channelId":"(UC[a-zA-Z0-9_-]+)"', html)
        if match:
            channel_id = match.group(1)
            return f"https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}"
    except Exception:
        return None

    return None

class YouTubeSystemCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.youtube_loop.start()

    def cog_unload(self):
        self.youtube_loop.cancel()

    @tasks.loop(minutes=5)
    async def youtube_loop(self):
        await self.bot.wait_until_ready()
        config = load_config()

        for gid, conf in config.items():
            channel_url = conf.get("youtube_channel_url")
            post_channel_id = conf.get("youtube_post_channel_id")
            last_video_url = conf.get("youtube_last_video_url")

            if not channel_url or not post_channel_id:
                continue

            try:
                feed_url = await resolve_youtube_feed_url(channel_url)
                if not feed_url:
                    continue

                feed = feedparser.parse(feed_url)
                if not feed.entries:
                    continue

                latest = feed.entries[0]
                latest_link = latest.link

                if latest_link != last_video_url:
                    guild = self.bot.get_guild(int(gid))
                    if not guild:
                        continue

                    channel = guild.get_channel(post_channel_id)
                    if not channel:
                        continue

                    if last_video_url is not None:
                        embed = discord.Embed(
                            title="📺 New YouTube Video",
                            description=f"**{latest.title}**\n{latest_link}",
                            color=discord.Color.red()
                        )
                        await channel.send(embed=embed)

                    update_guild_config(int(gid), "youtube_last_video_url", latest_link)
            except Exception as e:
                print(f"YouTube loop error in guild {gid}: {e}")

    @youtube_loop.before_loop
    async def before_youtube_loop(self):
        await self.bot.wait_until_ready()

async def setup(bot):
    await bot.add_cog(YouTubeSystemCog(bot))
