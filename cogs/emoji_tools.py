import re
import aiohttp
import discord
from discord.ext import commands
from utils.translations import tr

EMOJI_RE = re.compile(r"<(a?):([A-Za-z0-9_]+):(\d+)>")

class EmojiToolsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(manage_emojis_and_stickers=True)
    async def addemoji(self, ctx, *, emoji_text: str):
        matches = EMOJI_RE.findall(emoji_text)
        if not matches:
            return await ctx.send(tr(ctx.guild.id, "no_custom_emoji"))

        matches = matches[:50]

        added = 0
        failed = 0

        async with aiohttp.ClientSession() as session:
            for animated_flag, name, emoji_id in matches:
                ext = "gif" if animated_flag == "a" else "png"
                url = f"https://cdn.discordapp.com/emojis/{emoji_id}.{ext}?size=128&quality=lossless"

                try:
                    async with session.get(url) as resp:
                        if resp.status != 200:
                            failed += 1
                            continue
                        data = await resp.read()

                    await ctx.guild.create_custom_emoji(name=name, image=data, reason=f"Added by {ctx.author}")
                    added += 1
                except Exception:
                    failed += 1

        await ctx.send(
            f"{tr(ctx.guild.id, 'emoji_added')}: `{added}` | "
            f"{tr(ctx.guild.id, 'emoji_failed')}: `{failed}` | Max: `50`"
        )

async def setup(bot):
    await bot.add_cog(EmojiToolsCog(bot))
