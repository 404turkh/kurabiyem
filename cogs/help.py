import discord
from discord.ext import commands
from utils.translations import tr, LANGUAGE_NAMES

def build_main_help_embed(guild_id: int, bot_user):
    embed = discord.Embed(
        title=tr(guild_id, "help_title"),
        description=f"🌸 **{tr(guild_id, 'help_desc')}**",
        color=discord.Color.from_rgb(180, 120, 255)
    )

    if bot_user:
        embed.set_thumbnail(url=bot_user.display_avatar.url)

    embed.add_field(
        name=f"📜 {tr(guild_id, 'commands')}",
        value="Setup • Utility • Support",
        inline=False
    )
    embed.add_field(
        name=f"⚙️ {tr(guild_id, 'systems')}",
        value="Welcome • Auto Role • Logs • Language",
        inline=False
    )
    embed.add_field(
        name=f"🎫 {tr(guild_id, 'tickets')}",
        value="Premium support ticket center",
        inline=False
    )
    embed.add_field(
        name=f"📺 {tr(guild_id, 'youtube')}",
        value="Automatic YouTube channel tracking",
        inline=False
    )

    embed.set_footer(text="私のクッキー • Anime Premium Command Center")
    return embed

class HelpCategorySelect(discord.ui.Select):
    def __init__(self, guild_id: int):
        self.guild_id = guild_id
        options = [
            discord.SelectOption(label=tr(guild_id, "commands"), value="commands", emoji="📜"),
            discord.SelectOption(label=tr(guild_id, "systems"), value="systems", emoji="⚙️"),
            discord.SelectOption(label=tr(guild_id, "tickets"), value="tickets", emoji="🎫"),
            discord.SelectOption(label=tr(guild_id, "server_tools"), value="server_tools", emoji="🧰"),
            discord.SelectOption(label=tr(guild_id, "youtube"), value="youtube", emoji="📺"),
            discord.SelectOption(label=tr(guild_id, "language"), value="language", emoji="🌐"),
        ]
        super().__init__(
            placeholder="Select a menu category...",
            min_values=1,
            max_values=1,
            options=options
        )

    async def callback(self, interaction: discord.Interaction):
        value = self.values[0]

        if value == "commands":
            embed = discord.Embed(
                title=f"📜 {tr(self.guild_id, 'commands')}",
                description=(
                    "`h!help`\n"
                    "`h!serverinfo`\n"
                    "`h!userinfo [@user]`\n"
                    "`h!settings`\n"
                    "`h!setwelcome #channel`\n"
                    "`h!setgoodbye #channel`\n"
                    "`h!setlog #channel`\n"
                    "`h!setautorole @role`\n"
                    "`h!setticketcategory <category_id>`\n"
                    "`h!setsupportrole @role`\n"
                    "`h!setlanguage <tr/en/ja/fr/de/ar>`\n"
                    "`h!setdmwelcome on/off`\n"
                    "`h!youtubechannel <youtube_link>`\n"
                    "`h!setyoutubepostchannel #channel`\n"
                    "`h!sendtickets`"
                ),
                color=discord.Color.blurple()
            )
        elif value == "systems":
            embed = discord.Embed(
                title=f"⚙️ {tr(self.guild_id, 'systems')}",
                description=(
                    "• Advanced anime premium welcome card\n"
                    "• Automatic role for every new member\n"
                    "• Goodbye channel system\n"
                    "• Log system\n"
                    "• Multi-language system\n"
                    "• Premium menu interface"
                ),
                color=discord.Color.purple()
            )
        elif value == "tickets":
            embed = discord.Embed(
                title=f"🎫 {tr(self.guild_id, 'tickets')}",
                description=(
                    "• Premium ticket panel\n"
                    "• Button-based ticket creation\n"
                    "• Support role ping\n"
                    "• Category-based ticket creation\n"
                    "• Close button system"
                ),
                color=discord.Color.green()
            )
        elif value == "server_tools":
            embed = discord.Embed(
                title=f"🧰 {tr(self.guild_id, 'server_tools')}",
                description=(
                    "• `h!serverinfo`\nShows server information.\n\n"
                    "• `h!userinfo [@user]`\nShows user information.\n\n"
                    "• `h!settings`\nShows current bot settings."
                ),
                color=discord.Color.orange()
            )
        elif value == "youtube":
            embed = discord.Embed(
                title=f"📺 {tr(self.guild_id, 'youtube')}",
                description=(
                    "• Add a YouTube channel link\n"
                    "• Bot checks that channel automatically\n"
                    "• When a new video is uploaded, it posts the link to the selected Discord channel\n\n"
                    "Commands:\n"
                    "`h!youtubechannel <youtube_link>`\n"
                    "`h!setyoutubepostchannel #channel`"
                ),
                color=discord.Color.red()
            )
        else:
            langs = "\n".join([f"`{code}` - {name}" for code, name in LANGUAGE_NAMES.items()])
            embed = discord.Embed(
                title=f"🌐 {tr(self.guild_id, 'language')}",
                description=(
                    "All panels, buttons, messages, system texts, welcome messages, ticket texts, "
                    "settings texts, and info screens change based on the selected language.\n\n"
                    f"{langs}\n\n"
                    "Command:\n`h!setlanguage <code>`"
                ),
                color=discord.Color.teal()
            )

        embed.set_footer(text="私のクッキー • Anime Premium Menu")
        await interaction.response.edit_message(embed=embed, view=HelpMenuView(self.guild_id))

class HelpMenuView(discord.ui.View):
    def __init__(self, guild_id: int):
        super().__init__(timeout=180)
        self.guild_id = guild_id
        self.add_item(HelpCategorySelect(guild_id))

    @discord.ui.button(label="Main Menu", style=discord.ButtonStyle.primary, emoji="🏠")
    async def main_menu(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = build_main_help_embed(interaction.guild.id, interaction.client.user)
        await interaction.response.edit_message(embed=embed, view=HelpMenuView(self.guild_id))

    @discord.ui.button(label="Close", style=discord.ButtonStyle.danger, emoji="❌")
    async def close_menu(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.edit_message(content=tr(self.guild_id, "close"), embed=None, view=None)

class HelpCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="help")
    async def help_command(self, ctx):
        embed = build_main_help_embed(ctx.guild.id, self.bot.user)
        await ctx.send(embed=embed, view=HelpMenuView(ctx.guild.id))

async def setup(bot):
    await bot.add_cog(HelpCog(bot))
