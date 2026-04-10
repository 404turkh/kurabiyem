import discord
from discord.ext import commands
from utils.storage import get_guild_config
from utils.translations import tr

class LoggingCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def send_log(self, guild: discord.Guild, message: str):
        conf = get_guild_config(guild.id)
        cid = conf.get("log_channel_id")
        if not cid:
            return

        channel = guild.get_channel(cid)
        if channel:
            await channel.send(message)

    @commands.Cog.listener()
    async def on_member_remove(self, member: discord.Member):
        await self.send_log(member.guild, f"🔴 {member} {tr(member.guild.id, 'goodbye')}")

    @commands.Cog.listener()
    async def on_message_delete(self, message: discord.Message):
        if not message.guild or message.author.bot:
            return

        await self.send_log(
            message.guild,
            f"🗑️ Deleted Message | User: {message.author} | Channel: #{message.channel.name} | Content: {message.content}"
        )

    @commands.Cog.listener()
    async def on_message_edit(self, before: discord.Message, after: discord.Message):
        if not before.guild or before.author.bot or before.content == after.content:
            return

        await self.send_log(
            before.guild,
            f"✏️ Edited Message | User: {before.author} | Channel: #{before.channel.name}\nOld: {before.content}\nNew: {after.content}"
        )

async def setup(bot):
    await bot.add_cog(LoggingCog(bot))
