import discord
from discord.ext import commands
from utils.storage import get_guild_config, update_guild_config
from utils.translations import LANGUAGE_NAMES, tr

class SetupCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def settings(self, ctx):
        conf = get_guild_config(ctx.guild.id)

        def channel_text(cid):
            if not cid:
                return tr(ctx.guild.id, "not_set")
            ch = ctx.guild.get_channel(cid)
            return ch.mention if ch else f"`{cid}`"

        def role_text(rid):
            if not rid:
                return tr(ctx.guild.id, "not_set")
            role = ctx.guild.get_role(rid)
            return role.mention if role else f"`{rid}`"

        embed = discord.Embed(
            title=tr(ctx.guild.id, "settings_title"),
            description="✨ Anime premium setup panel",
            color=discord.Color.blurple()
        )

        if self.bot.user:
            embed.set_thumbnail(url=self.bot.user.display_avatar.url)

        embed.add_field(name="Language", value=LANGUAGE_NAMES.get(conf["language"], conf["language"]), inline=False)
        embed.add_field(name="Welcome Channel", value=channel_text(conf["welcome_channel_id"]), inline=False)
        embed.add_field(name="Goodbye Channel", value=channel_text(conf["goodbye_channel_id"]), inline=False)
        embed.add_field(name="Log Channel", value=channel_text(conf["log_channel_id"]), inline=False)
        embed.add_field(name="Auto Role", value=role_text(conf["autorole_id"]), inline=False)
        embed.add_field(name="Ticket Category", value=str(conf["ticket_category_id"] or tr(ctx.guild.id, "not_set")), inline=False)
        embed.add_field(name="Support Role", value=role_text(conf["support_role_id"]), inline=False)
        embed.add_field(name="YouTube Channel", value=conf["youtube_channel_url"] or tr(ctx.guild.id, "not_set"), inline=False)
        embed.add_field(name="YouTube Post Channel", value=channel_text(conf["youtube_post_channel_id"]), inline=False)
        embed.add_field(name="DM Welcome", value="On" if conf["dm_welcome_enabled"] else "Off", inline=False)

        embed.set_footer(text="私のクッキー • Premium Settings")
        await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def setwelcome(self, ctx, channel: discord.TextChannel):
        update_guild_config(ctx.guild.id, "welcome_channel_id", channel.id)
        await ctx.send(f"Welcome channel set to {channel.mention}")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def setgoodbye(self, ctx, channel: discord.TextChannel):
        update_guild_config(ctx.guild.id, "goodbye_channel_id", channel.id)
        await ctx.send(f"Goodbye channel set to {channel.mention}")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def setlog(self, ctx, channel: discord.TextChannel):
        update_guild_config(ctx.guild.id, "log_channel_id", channel.id)
        await ctx.send(f"Log channel set to {channel.mention}")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def setautorole(self, ctx, role: discord.Role):
        update_guild_config(ctx.guild.id, "autorole_id", role.id)
        await ctx.send(f"Auto role set to {role.mention}")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def setticketcategory(self, ctx, category_id: int):
        update_guild_config(ctx.guild.id, "ticket_category_id", category_id)
        await ctx.send(f"Ticket category set to `{category_id}`")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def setsupportrole(self, ctx, role: discord.Role):
        update_guild_config(ctx.guild.id, "support_role_id", role.id)
        await ctx.send(f"Support role set to {role.mention}")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def setlanguage(self, ctx, code: str):
        code = code.lower().strip()
        if code not in LANGUAGE_NAMES:
            await ctx.send("Available: `tr`, `en`, `ja`, `fr`, `de`, `ar`")
            return

        update_guild_config(ctx.guild.id, "language", code)
        await ctx.send(f"Language set to **{LANGUAGE_NAMES[code]}**")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def setdmwelcome(self, ctx, state: str):
        state = state.lower().strip()
        if state not in ["on", "off"]:
            await ctx.send("Usage: `h!setdmwelcome on` or `h!setdmwelcome off`")
            return

        update_guild_config(ctx.guild.id, "dm_welcome_enabled", state == "on")
        await ctx.send(f"DM welcome set to `{state}`")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def youtubechannel(self, ctx, *, channel_url: str):
        if "youtube.com/" not in channel_url and "youtu.be/" not in channel_url:
            await ctx.send("Please provide a valid YouTube channel link.")
            return

        update_guild_config(ctx.guild.id, "youtube_channel_url", channel_url.strip())
        await ctx.send(f"YouTube channel link set to `{channel_url}`")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def setyoutubepostchannel(self, ctx, channel: discord.TextChannel):
        update_guild_config(ctx.guild.id, "youtube_post_channel_id", channel.id)
        await ctx.send(f"YouTube post channel set to {channel.mention}")

async def setup(bot):
    await bot.add_cog(SetupCog(bot))import discord
from discord.ext import commands
from utils.storage import get_guild_config, update_guild_config
from utils.translations import LANGUAGE_NAMES, tr

class SetupCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def settings(self, ctx):
        conf = get_guild_config(ctx.guild.id)

        def channel_text(cid):
            if not cid:
                return tr(ctx.guild.id, "not_set")
            ch = ctx.guild.get_channel(cid)
            return ch.mention if ch else f"`{cid}`"

        def role_text(rid):
            if not rid:
                return tr(ctx.guild.id, "not_set")
            role = ctx.guild.get_role(rid)
            return role.mention if role else f"`{rid}`"

        embed = discord.Embed(
            title=tr(ctx.guild.id, "settings_title"),
            description="✨ Anime premium setup panel",
            color=discord.Color.blurple()
        )

        if self.bot.user:
            embed.set_thumbnail(url=self.bot.user.display_avatar.url)

        embed.add_field(name="Language", value=LANGUAGE_NAMES.get(conf["language"], conf["language"]), inline=False)
        embed.add_field(name="Welcome Channel", value=channel_text(conf["welcome_channel_id"]), inline=False)
        embed.add_field(name="Goodbye Channel", value=channel_text(conf["goodbye_channel_id"]), inline=False)
        embed.add_field(name="Log Channel", value=channel_text(conf["log_channel_id"]), inline=False)
        embed.add_field(name="Auto Role", value=role_text(conf["autorole_id"]), inline=False)
        embed.add_field(name="Ticket Category", value=str(conf["ticket_category_id"] or tr(ctx.guild.id, "not_set")), inline=False)
        embed.add_field(name="Support Role", value=role_text(conf["support_role_id"]), inline=False)
        embed.add_field(name="YouTube Channel", value=conf["youtube_channel_url"] or tr(ctx.guild.id, "not_set"), inline=False)
        embed.add_field(name="YouTube Post Channel", value=channel_text(conf["youtube_post_channel_id"]), inline=False)
        embed.add_field(name="DM Welcome", value="On" if conf["dm_welcome_enabled"] else "Off", inline=False)

        embed.set_footer(text="私のクッキー • Premium Settings")
        await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def setwelcome(self, ctx, channel: discord.TextChannel):
        update_guild_config(ctx.guild.id, "welcome_channel_id", channel.id)
        await ctx.send(f"Welcome channel set to {channel.mention}")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def setgoodbye(self, ctx, channel: discord.TextChannel):
        update_guild_config(ctx.guild.id, "goodbye_channel_id", channel.id)
        await ctx.send(f"Goodbye channel set to {channel.mention}")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def setlog(self, ctx, channel: discord.TextChannel):
        update_guild_config(ctx.guild.id, "log_channel_id", channel.id)
        await ctx.send(f"Log channel set to {channel.mention}")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def setautorole(self, ctx, role: discord.Role):
        update_guild_config(ctx.guild.id, "autorole_id", role.id)
        await ctx.send(f"Auto role set to {role.mention}")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def setticketcategory(self, ctx, category_id: int):
        update_guild_config(ctx.guild.id, "ticket_category_id", category_id)
        await ctx.send(f"Ticket category set to `{category_id}`")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def setsupportrole(self, ctx, role: discord.Role):
        update_guild_config(ctx.guild.id, "support_role_id", role.id)
        await ctx.send(f"Support role set to {role.mention}")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def setlanguage(self, ctx, code: str):
        code = code.lower().strip()
        if code not in LANGUAGE_NAMES:
            await ctx.send("Available: `tr`, `en`, `ja`, `fr`, `de`, `ar`")
            return

        update_guild_config(ctx.guild.id, "language", code)
        await ctx.send(f"Language set to **{LANGUAGE_NAMES[code]}**")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def setdmwelcome(self, ctx, state: str):
        state = state.lower().strip()
        if state not in ["on", "off"]:
            await ctx.send("Usage: `h!setdmwelcome on` or `h!setdmwelcome off`")
            return

        update_guild_config(ctx.guild.id, "dm_welcome_enabled", state == "on")
        await ctx.send(f"DM welcome set to `{state}`")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def youtubechannel(self, ctx, *, channel_url: str):
        if "youtube.com/" not in channel_url and "youtu.be/" not in channel_url:
            await ctx.send("Please provide a valid YouTube channel link.")
            return

        update_guild_config(ctx.guild.id, "youtube_channel_url", channel_url.strip())
        await ctx.send(f"YouTube channel link set to `{channel_url}`")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def setyoutubepostchannel(self, ctx, channel: discord.TextChannel):
        update_guild_config(ctx.guild.id, "youtube_post_channel_id", channel.id)
        await ctx.send(f"YouTube post channel set to {channel.mention}")

async def setup(bot):
    await bot.add_cog(SetupCog(bot))
