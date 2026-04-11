from discord.ext import commands
from utils.translations import tr

class ModerationCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="clear")
    @commands.has_permissions(manage_messages=True)
    async def clear_messages(self, ctx, number: int):
        if number < 1 or number > 100:
            return await ctx.send(tr(ctx.guild.id, "clear_invalid"))

        await ctx.channel.purge(limit=number + 1)
        msg = await ctx.send(f"{number} {tr(ctx.guild.id, 'clear_done')}")
        await msg.delete(delay=3)

async def setup(bot):
    await bot.add_cog(ModerationCog(bot))
