import discord
from discord.ext import commands
from utils.panels import build_main_embed, MainPanelView
from utils.storage import get_guild_config, update_guild_config
from utils.translations import LANGUAGE_NAMES, tr

class CoreCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="panel")
    async def panel_command(self, ctx):
        embed = build_main_embed(ctx.guild, self.bot.user)
        await ctx.send(embed=embed, view=MainPanelView(ctx.guild.id, self.bot))

    @commands.command(name="help")
    async def help_command(self, ctx):
        embed = build_main_embed(ctx.guild, self.bot.user)
        await ctx.send(embed=embed, view=MainPanelView(ctx.guild.id, self.bot))

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def settings(self, ctx):
        conf = get_guild_config(ctx.guild.id)
        embed = discord.Embed(title=tr(ctx.guild.id, "settings"), color=discord.Color.blurple())
        embed.add_field(name="Language", value=LANGUAGE_NAMES.get(conf["language"], conf["language"]), inline=False)
        embed.add_field(name="Welcome", value=str(conf["welcome_channel_id"]), inline=False)
        embed.add_field(name="Goodbye", value=str(conf["goodbye_channel_id"]), inline=False)
        embed.add_field(name="Logs", value=str(conf["log_channel_id"]), inline=False)
        embed.add_field(name="Auto Role", value=str(conf["autorole_id"]), inline=False)
        embed.add_field(name="Support Role", value=str(conf["support_role_id"]), inline=False)
        embed.add_field(name="Ticket Category", value=str(conf["ticket_category_id"]), inline=False)
        embed.add_field(name="YouTube", value=conf["youtube_channel_url"] or tr(ctx.guild.id, "not_set"), inline=False)
        embed.add_field(name="YouTube Post", value=str(conf["youtube_post_channel_id"]), inline=False)
        embed.add_field(name="DM Welcome", value=str(conf["dm_welcome_enabled"]), inline=False)
        await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def setwelcome(self, ctx, channel: discord.TextChannel):
        update_guild_config(ctx.guild.id, "welcome_channel_id", channel.id)
        await ctx.send(tr(ctx.guild.id, "channel_saved"))

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def setgoodbye(self, ctx, channel: discord.TextChannel):
        update_guild_config(ctx.guild.id, "goodbye_channel_id", channel.id)
        await ctx.send(tr(ctx.guild.id, "channel_saved"))

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def setlog(self, ctx, channel: discord.TextChannel):
        update_guild_config(ctx.guild.id, "log_channel_id", channel.id)
        await ctx.send(tr(ctx.guild.id, "channel_saved"))

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def setautorole(self, ctx, role: discord.Role):
        update_guild_config(ctx.guild.id, "autorole_id", role.id)
        await ctx.send(tr(ctx.guild.id, "role_saved"))

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def setsupportrole(self, ctx, role: discord.Role):
        update_guild_config(ctx.guild.id, "support_role_id", role.id)
        await ctx.send(tr(ctx.guild.id, "role_saved"))

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def setticketcategory(self, ctx, category_id: int):
        update_guild_config(ctx.guild.id, "ticket_category_id", category_id)
        await ctx.send(tr(ctx.guild.id, "category_saved"))

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def setlanguage(self, ctx, code: str):
        code = code.lower().strip()
        if code not in LANGUAGE_NAMES:
            return await ctx.send("Available: tr / en / ja / fr / de / ar")
        update_guild_config(ctx.guild.id, "language", code)
        await ctx.send(tr(ctx.guild.id, "language_set"))

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def setdmwelcome(self, ctx, state: str):
        state = state.lower().strip()
        if state not in {"on", "off"}:
            return await ctx.send("Usage: `h!setdmwelcome on` or `h!setdmwelcome off`")
        update_guild_config(ctx.guild.id, "dm_welcome_enabled", state == "on")
        await ctx.send(tr(ctx.guild.id, "saved"))

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def youtubechannel(self, ctx, *, channel_url: str):
        if "youtube.com/" not in channel_url and "youtu.be/" not in channel_url:
            return await ctx.send(tr(ctx.guild.id, "invalid_link"))
        update_guild_config(ctx.guild.id, "youtube_channel_url", channel_url.strip())
        await ctx.send(tr(ctx.guild.id, "youtube_saved"))

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def setyoutubepostchannel(self, ctx, channel: discord.TextChannel):
        update_guild_config(ctx.guild.id, "youtube_post_channel_id", channel.id)
        await ctx.send(tr(ctx.guild.id, "channel_saved"))

async def setup(bot):
    await bot.add_cog(CoreCog(bot))
