import discord
from discord.ext import commands
from utils.storage import get_guild_config
from utils.cards import create_welcome_card
from utils.translations import tr

class WelcomeCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def send_log(self, guild, message):
        conf = get_guild_config(guild.id)
        cid = conf.get("log_channel_id")
        if not cid:
            return
        ch = guild.get_channel(cid)
        if ch:
            await ch.send(message)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        conf = get_guild_config(member.guild.id)
        welcome_channel_id = conf.get("welcome_channel_id")
        autorole_id = conf.get("autorole_id")
        dm_welcome_enabled = conf.get("dm_welcome_enabled", True)

        if autorole_id:
            role = member.guild.get_role(autorole_id)
            if role:
                try:
                    await member.add_roles(role, reason="Auto role system")
                except Exception as e:
                    print(f"Auto role error: {e}")

        if welcome_channel_id:
            channel = member.guild.get_channel(welcome_channel_id)
            if channel:
                try:
                    card = await create_welcome_card(member)
                    file = discord.File(card, filename="welcome.png")
                    embed = discord.Embed(
                        title="🌸 Welcome",
                        description=f"{member.mention}",
                        color=discord.Color.from_rgb(255, 170, 230)
                    )
                    embed.set_image(url="attachment://welcome.png")
                    await channel.send(embed=embed, file=file)
                except Exception as e:
                    print(f"Welcome card error: {e}")
                    await channel.send(f"Welcome {member.mention}!")

        if dm_welcome_enabled:
            try:
                await member.send(tr(member.guild.id, "welcome_dm"))
            except Exception:
                pass

        await self.send_log(member.guild, f"🟢 {member.mention} joined the server.")

async def setup(bot):
    await bot.add_cog(WelcomeCog(bot))
