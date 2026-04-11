import discord
from discord.ui import View, Button, Select, Modal, TextInput, ChannelSelect, RoleSelect
from utils.storage import get_guild_config, update_guild_config
from utils.translations import tr, LANGUAGE_NAMES

CREATOR_TAG = "@5harambro"
SUPPORT_SERVER = "https://discord.gg/d8PMsjEhGp"

def is_admin(member: discord.Member) -> bool:
    return member.guild_permissions.administrator

def nice_channel(guild: discord.Guild, cid):
    if not cid:
        return tr(guild.id, "not_set")
    ch = guild.get_channel(cid)
    return ch.mention if ch else f"`{cid}`"

def nice_role(guild: discord.Guild, rid):
    if not rid:
        return tr(guild.id, "not_set")
    role = guild.get_role(rid)
    return role.mention if role else f"`{rid}`"

def build_main_embed(guild: discord.Guild, bot_user: discord.ClientUser):
    embed = discord.Embed(
        title=tr(guild.id, "panel_title"),
        description=tr(guild.id, "panel_desc"),
        color=discord.Color.from_rgb(188, 132, 255),
    )
    if bot_user:
        embed.set_thumbnail(url=bot_user.display_avatar.url)

    embed.add_field(name="✦ Main", value="Setup • Welcome • Tickets • YouTube • Emoji • Tools", inline=False)
    embed.add_field(name=f"👤 {tr(guild.id, 'creator')}", value=CREATOR_TAG, inline=True)
    embed.add_field(name=f"🔗 {tr(guild.id, 'support_server')}", value=SUPPORT_SERVER, inline=True)
    embed.set_footer(text="私のクッキー • Premium Control Center")
    return embed

def build_setup_embed(guild: discord.Guild):
    conf = get_guild_config(guild.id)
    embed = discord.Embed(
        title=tr(guild.id, "setup_panel"),
        description=tr(guild.id, "current_settings"),
        color=discord.Color.blurple(),
    )
    embed.add_field(name="Welcome", value=nice_channel(guild, conf["welcome_channel_id"]), inline=True)
    embed.add_field(name="Goodbye", value=nice_channel(guild, conf["goodbye_channel_id"]), inline=True)
    embed.add_field(name="Logs", value=nice_channel(guild, conf["log_channel_id"]), inline=True)
    embed.add_field(name="Auto Role", value=nice_role(guild, conf["autorole_id"]), inline=True)
    embed.add_field(name="Support Role", value=nice_role(guild, conf["support_role_id"]), inline=True)
    embed.add_field(name="Ticket Category", value=str(conf["ticket_category_id"] or tr(guild.id, "not_set")), inline=True)
    embed.add_field(name="YouTube Link", value=conf["youtube_channel_url"] or tr(guild.id, "not_set"), inline=False)
    embed.add_field(name="YouTube Channel", value=nice_channel(guild, conf["youtube_post_channel_id"]), inline=False)
    return embed

def build_welcome_embed(guild: discord.Guild):
    conf = get_guild_config(guild.id)
    embed = discord.Embed(
        title=tr(guild.id, "welcome_panel"),
        description=tr(guild.id, "current_settings"),
        color=discord.Color.from_rgb(255, 150, 210),
    )
    embed.add_field(name="Welcome", value=nice_channel(guild, conf["welcome_channel_id"]), inline=False)
    embed.add_field(name="Goodbye", value=nice_channel(guild, conf["goodbye_channel_id"]), inline=False)
    embed.add_field(name="Auto Role", value=nice_role(guild, conf["autorole_id"]), inline=False)
    embed.add_field(
        name=tr(guild.id, "dm_welcome"),
        value=tr(guild.id, "enabled") if conf["dm_welcome_enabled"] else tr(guild.id, "disabled"),
        inline=False
    )
    return embed

def build_ticket_embed(guild: discord.Guild):
    conf = get_guild_config(guild.id)
    embed = discord.Embed(
        title=tr(guild.id, "ticket_panel"),
        description=tr(guild.id, "current_settings"),
        color=discord.Color.green(),
    )
    embed.add_field(name="Support Role", value=nice_role(guild, conf["support_role_id"]), inline=False)
    embed.add_field(name="Ticket Category", value=str(conf["ticket_category_id"] or tr(guild.id, "not_set")), inline=False)
    return embed

def build_youtube_embed(guild: discord.Guild):
    conf = get_guild_config(guild.id)
    embed = discord.Embed(
        title=tr(guild.id, "youtube_panel"),
        description="Track a YouTube channel and auto-post new videos.",
        color=discord.Color.red(),
    )
    embed.add_field(name="YouTube Link", value=conf["youtube_channel_url"] or tr(guild.id, "not_set"), inline=False)
    embed.add_field(name="Post Channel", value=nice_channel(guild, conf["youtube_post_channel_id"]), inline=False)
    return embed

def build_language_embed(guild: discord.Guild):
    conf = get_guild_config(guild.id)
    embed = discord.Embed(
        title=tr(guild.id, "language_panel"),
        description=tr(guild.id, "select_language"),
        color=discord.Color.teal(),
    )
    embed.add_field(name="Current", value=LANGUAGE_NAMES.get(conf["language"], conf["language"]), inline=False)
    return embed

def build_emoji_embed(guild: discord.Guild):
    embed = discord.Embed(
        title=tr(guild.id, "emoji_panel"),
        description=(
            "Use `h!addemoji <:name:id> ...`\n"
            "Up to **50 custom emojis** per message.\n"
            "Unicode emojis are not supported."
        ),
        color=discord.Color.gold(),
    )
    return embed

def build_tools_embed(guild: discord.Guild):
    embed = discord.Embed(
        title=tr(guild.id, "server_tools"),
        description="`h!serverinfo`\n`h!userinfo [@user]`\n`h!clear <1-100>`",
        color=discord.Color.orange(),
    )
    return embed

def build_about_embed(guild: discord.Guild):
    embed = discord.Embed(
        title=tr(guild.id, "about_panel"),
        description=tr(guild.id, "about_text"),
        color=discord.Color.from_rgb(170, 130, 255),
    )
    embed.add_field(name=tr(guild.id, "creator"), value=CREATOR_TAG, inline=False)
    embed.add_field(name=tr(guild.id, "support_server"), value=SUPPORT_SERVER, inline=False)
    return embed

class YouTubeLinkModal(Modal):
    def __init__(self, guild_id: int):
        super().__init__(title="YouTube Link")
        self.guild_id = guild_id
        self.link_input = TextInput(
            label="Channel Link",
            placeholder="https://www.youtube.com/@example",
            required=True,
            max_length=200,
        )
        self.add_item(self.link_input)

    async def on_submit(self, interaction: discord.Interaction):
        url = str(self.link_input.value).strip()
        if "youtube.com/" not in url and "youtu.be/" not in url:
            return await interaction.response.send_message(tr(self.guild_id, "invalid_link"), ephemeral=True)

        update_guild_config(self.guild_id, "youtube_channel_url", url)
        await interaction.response.send_message(tr(self.guild_id, "youtube_saved"), ephemeral=True)

class BasePanelView(View):
    def __init__(self, guild_id: int, bot_client: discord.Client):
        super().__init__(timeout=300)
        self.guild_id = guild_id
        self.bot_client = bot_client

    async def deny_if_not_admin(self, interaction: discord.Interaction) -> bool:
        if not isinstance(interaction.user, discord.Member) or not is_admin(interaction.user):
            await interaction.response.send_message(tr(self.guild_id, "admin_only"), ephemeral=True)
            return True
        return False

    async def go_home(self, interaction: discord.Interaction):
        await interaction.response.edit_message(
            embed=build_main_embed(interaction.guild, interaction.client.user),
            view=MainPanelView(self.guild_id, self.bot_client),
        )

class MainPanelView(BasePanelView):
    @discord.ui.button(label="Setup", style=discord.ButtonStyle.primary, emoji="🛠️")
    async def setup_btn(self, interaction: discord.Interaction, button: Button):
        await interaction.response.edit_message(embed=build_setup_embed(interaction.guild), view=SetupPanelView(self.guild_id, self.bot_client))

    @discord.ui.button(label="Welcome", style=discord.ButtonStyle.secondary, emoji="🌸")
    async def welcome_btn(self, interaction: discord.Interaction, button: Button):
        await interaction.response.edit_message(embed=build_welcome_embed(interaction.guild), view=WelcomePanelView(self.guild_id, self.bot_client))

    @discord.ui.button(label="Tickets", style=discord.ButtonStyle.success, emoji="🎫")
    async def ticket_btn(self, interaction: discord.Interaction, button: Button):
        await interaction.response.edit_message(embed=build_ticket_embed(interaction.guild), view=TicketPanelView(self.guild_id, self.bot_client))

    @discord.ui.button(label="YouTube", style=discord.ButtonStyle.danger, emoji="📺")
    async def yt_btn(self, interaction: discord.Interaction, button: Button):
        await interaction.response.edit_message(embed=build_youtube_embed(interaction.guild), view=YouTubePanelView(self.guild_id, self.bot_client))

    @discord.ui.button(label="Emoji", style=discord.ButtonStyle.secondary, emoji="✨")
    async def emoji_btn(self, interaction: discord.Interaction, button: Button):
        await interaction.response.edit_message(embed=build_emoji_embed(interaction.guild), view=SimpleBackView(self.guild_id, self.bot_client))

    @discord.ui.button(label="Language", style=discord.ButtonStyle.secondary, emoji="🌐")
    async def lang_btn(self, interaction: discord.Interaction, button: Button):
        await interaction.response.edit_message(embed=build_language_embed(interaction.guild), view=LanguagePanelView(self.guild_id, self.bot_client))

    @discord.ui.button(label="Tools", style=discord.ButtonStyle.secondary, emoji="🧰")
    async def tools_btn(self, interaction: discord.Interaction, button: Button):
        await interaction.response.edit_message(embed=build_tools_embed(interaction.guild), view=SimpleBackView(self.guild_id, self.bot_client))

    @discord.ui.button(label="About", style=discord.ButtonStyle.secondary, emoji="💠")
    async def about_btn(self, interaction: discord.Interaction, button: Button):
        await interaction.response.edit_message(embed=build_about_embed(interaction.guild), view=SimpleBackView(self.guild_id, self.bot_client))

    @discord.ui.button(label="Close", style=discord.ButtonStyle.danger, emoji="❌")
    async def close_btn(self, interaction: discord.Interaction, button: Button):
        await interaction.response.edit_message(content=tr(self.guild_id, "close"), embed=None, view=None)

class SimpleBackView(BasePanelView):
    @discord.ui.button(label="Main Menu", style=discord.ButtonStyle.primary, emoji="🏠")
    async def back_btn(self, interaction: discord.Interaction, button: Button):
        await self.go_home(interaction)

class WelcomeChannelSelect(ChannelSelect):
    def __init__(self, guild_id: int):
        super().__init__(placeholder="Select welcome channel...", channel_types=[discord.ChannelType.text], min_values=1, max_values=1)
        self.guild_id = guild_id

    async def callback(self, interaction: discord.Interaction):
        update_guild_config(self.guild_id, "welcome_channel_id", self.values[0].id)
        await interaction.response.send_message(tr(self.guild_id, "channel_saved"), ephemeral=True)

class GoodbyeChannelSelect(ChannelSelect):
    def __init__(self, guild_id: int):
        super().__init__(placeholder="Select goodbye channel...", channel_types=[discord.ChannelType.text], min_values=1, max_values=1)
        self.guild_id = guild_id

    async def callback(self, interaction: discord.Interaction):
        update_guild_config(self.guild_id, "goodbye_channel_id", self.values[0].id)
        await interaction.response.send_message(tr(self.guild_id, "channel_saved"), ephemeral=True)

class LogChannelSelect(ChannelSelect):
    def __init__(self, guild_id: int):
        super().__init__(placeholder="Select log channel...", channel_types=[discord.ChannelType.text], min_values=1, max_values=1)
        self.guild_id = guild_id

    async def callback(self, interaction: discord.Interaction):
        update_guild_config(self.guild_id, "log_channel_id", self.values[0].id)
        await interaction.response.send_message(tr(self.guild_id, "channel_saved"), ephemeral=True)

class YouTubePostChannelSelect(ChannelSelect):
    def __init__(self, guild_id: int):
        super().__init__(placeholder="Select YouTube post channel...", channel_types=[discord.ChannelType.text], min_values=1, max_values=1)
        self.guild_id = guild_id

    async def callback(self, interaction: discord.Interaction):
        update_guild_config(self.guild_id, "youtube_post_channel_id", self.values[0].id)
        await interaction.response.send_message(tr(self.guild_id, "channel_saved"), ephemeral=True)

class AutoRoleSelect(RoleSelect):
    def __init__(self, guild_id: int):
        super().__init__(placeholder="Select auto role...", min_values=1, max_values=1)
        self.guild_id = guild_id

    async def callback(self, interaction: discord.Interaction):
        update_guild_config(self.guild_id, "autorole_id", self.values[0].id)
        await interaction.response.send_message(tr(self.guild_id, "role_saved"), ephemeral=True)

class SupportRoleSelect(RoleSelect):
    def __init__(self, guild_id: int):
        super().__init__(placeholder="Select support role...", min_values=1, max_values=1)
        self.guild_id = guild_id

    async def callback(self, interaction: discord.Interaction):
        update_guild_config(self.guild_id, "support_role_id", self.values[0].id)
        await interaction.response.send_message(tr(self.guild_id, "role_saved"), ephemeral=True)

class LanguageSelect(Select):
    def __init__(self, guild_id: int):
        self.guild_id = guild_id
        options = [discord.SelectOption(label=name, value=code) for code, name in LANGUAGE_NAMES.items()]
        super().__init__(placeholder="Select language...", min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        code = self.values[0]
        update_guild_config(self.guild_id, "language", code)
        await interaction.response.edit_message(embed=build_language_embed(interaction.guild), view=LanguagePanelView(self.guild_id, interaction.client))

class TicketCategoryView(SimpleBackView):
    @discord.ui.channel_select(
        placeholder="Select ticket category...",
        channel_types=[discord.ChannelType.category],
        min_values=1,
        max_values=1,
        row=0,
    )
    async def category_select(self, interaction: discord.Interaction, select: ChannelSelect):
        if await self.deny_if_not_admin(interaction):
            return
        update_guild_config(self.guild_id, "ticket_category_id", select.values[0].id)
        await interaction.response.send_message(tr(self.guild_id, "category_saved"), ephemeral=True)

class SetupPanelView(BasePanelView):
    def __init__(self, guild_id: int, bot_client: discord.Client):
        super().__init__(guild_id, bot_client)
        self.add_item(WelcomeChannelSelect(guild_id))
        self.add_item(GoodbyeChannelSelect(guild_id))
        self.add_item(LogChannelSelect(guild_id))
        self.add_item(AutoRoleSelect(guild_id))
        self.add_item(SupportRoleSelect(guild_id))

    @discord.ui.button(label="Ticket Category", style=discord.ButtonStyle.secondary, emoji="📁", row=3)
    async def ticket_category_btn(self, interaction: discord.Interaction, button: Button):
        if await self.deny_if_not_admin(interaction):
            return
        await interaction.response.edit_message(embed=build_setup_embed(interaction.guild), view=TicketCategoryView(self.guild_id, self.bot_client))

    @discord.ui.button(label="Main Menu", style=discord.ButtonStyle.primary, emoji="🏠", row=4)
    async def back_btn(self, interaction: discord.Interaction, button: Button):
        await self.go_home(interaction)

class WelcomePanelView(BasePanelView):
    def __init__(self, guild_id: int, bot_client: discord.Client):
        super().__init__(guild_id, bot_client)
        self.add_item(WelcomeChannelSelect(guild_id))
        self.add_item(GoodbyeChannelSelect(guild_id))
        self.add_item(AutoRoleSelect(guild_id))

    @discord.ui.button(label="Toggle DM Welcome", style=discord.ButtonStyle.success, emoji="✉️", row=3)
    async def toggle_dm_btn(self, interaction: discord.Interaction, button: Button):
        if await self.deny_if_not_admin(interaction):
            return
        conf = get_guild_config(self.guild_id)
        update_guild_config(self.guild_id, "dm_welcome_enabled", not conf["dm_welcome_enabled"])
        await interaction.response.edit_message(embed=build_welcome_embed(interaction.guild), view=WelcomePanelView(self.guild_id, self.bot_client))

    @discord.ui.button(label="Main Menu", style=discord.ButtonStyle.primary, emoji="🏠", row=4)
    async def back_btn(self, interaction: discord.Interaction, button: Button):
        await self.go_home(interaction)

class TicketPanelView(BasePanelView):
    def __init__(self, guild_id: int, bot_client: discord.Client):
        super().__init__(guild_id, bot_client)
        self.add_item(SupportRoleSelect(guild_id))

    @discord.ui.button(label="Set Category", style=discord.ButtonStyle.secondary, emoji="📁", row=1)
    async def category_btn(self, interaction: discord.Interaction, button: Button):
        if await self.deny_if_not_admin(interaction):
            return
        await interaction.response.edit_message(embed=build_ticket_embed(interaction.guild), view=TicketCategoryView(self.guild_id, self.bot_client))

    @discord.ui.button(label="Send Ticket Panel", style=discord.ButtonStyle.success, emoji="📨", row=1)
    async def send_panel_btn(self, interaction: discord.Interaction, button: Button):
        if await self.deny_if_not_admin(interaction):
            return
        from cogs.tickets import TicketCreateView
        embed = discord.Embed(
            title=tr(self.guild_id, "ticket_title"),
            description=tr(self.guild_id, "ticket_desc"),
            color=discord.Color.green()
        )
        await interaction.channel.send(embed=embed, view=TicketCreateView(self.bot_client))
        await interaction.response.send_message(tr(self.guild_id, "ticket_sent"), ephemeral=True)

    @discord.ui.button(label="Main Menu", style=discord.ButtonStyle.primary, emoji="🏠", row=2)
    async def back_btn(self, interaction: discord.Interaction, button: Button):
        await self.go_home(interaction)

class YouTubePanelView(BasePanelView):
    def __init__(self, guild_id: int, bot_client: discord.Client):
        super().__init__(guild_id, bot_client)
        self.add_item(YouTubePostChannelSelect(guild_id))

    @discord.ui.button(label="Set YouTube Link", style=discord.ButtonStyle.secondary, emoji="🔗", row=1)
    async def set_link_btn(self, interaction: discord.Interaction, button: Button):
        if await self.deny_if_not_admin(interaction):
            return
        await interaction.response.send_modal(YouTubeLinkModal(self.guild_id))

    @discord.ui.button(label="Main Menu", style=discord.ButtonStyle.primary, emoji="🏠", row=2)
    async def back_btn(self, interaction: discord.Interaction, button: Button):
        await self.go_home(interaction)

class LanguagePanelView(BasePanelView):
    def __init__(self, guild_id: int, bot_client: discord.Client):
        super().__init__(guild_id, bot_client)
        self.add_item(LanguageSelect(guild_id))

    @discord.ui.button(label="Main Menu", style=discord.ButtonStyle.primary, emoji="🏠", row=1)
    async def back_btn(self, interaction: discord.Interaction, button: Button):
        await self.go_home(interaction)
