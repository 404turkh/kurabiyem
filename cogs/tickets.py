import asyncio
import discord
from discord.ext import commands
from utils.storage import get_guild_config
from utils.translations import tr

class TicketCloseView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Close Ticket", emoji="🔒", style=discord.ButtonStyle.danger, custom_id="close_ticket_button")
    async def close_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not interaction.guild or not interaction.channel:
            return

        if not interaction.channel.name.startswith("ticket-"):
            await interaction.response.send_message(tr(interaction.guild.id, "not_ticket_channel"), ephemeral=True)
            return

        await interaction.response.send_message(tr(interaction.guild.id, "ticket_closing"))
        await asyncio.sleep(5)
        await interaction.channel.delete(reason=f"Ticket closed by {interaction.user}")

class TicketCreateView(discord.ui.View):
    def __init__(self, bot):
        super().__init__(timeout=None)
        self.bot = bot

    @discord.ui.button(label="Create Ticket", emoji="🎫", style=discord.ButtonStyle.success, custom_id="create_ticket_button")
    async def create_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        guild = interaction.guild
        user = interaction.user
        if guild is None:
            return

        conf = get_guild_config(guild.id)
        category_id = conf.get("ticket_category_id")
        support_role_id = conf.get("support_role_id")

        existing = discord.utils.get(guild.text_channels, name=f"ticket-{user.id}")
        if existing:
            await interaction.response.send_message(tr(guild.id, "already_ticket"), ephemeral=True)
            return

        overwrites = {
            guild.default_role: discord.PermissionOverwrite(view_channel=False),
            user: discord.PermissionOverwrite(view_channel=True, send_messages=True, read_message_history=True),
        }

        me = guild.me or guild.get_member(self.bot.user.id)
        if me:
            overwrites[me] = discord.PermissionOverwrite(
                view_channel=True,
                send_messages=True,
                manage_channels=True,
                manage_messages=True
            )

        if support_role_id:
            role = guild.get_role(support_role_id)
            if role:
                overwrites[role] = discord.PermissionOverwrite(
                    view_channel=True,
                    send_messages=True,
                    read_message_history=True
                )

        category = guild.get_channel(category_id) if category_id else None

        channel = await guild.create_text_channel(
            name=f"ticket-{user.id}",
            category=category,
            overwrites=overwrites,
            reason=f"Ticket created by {user}"
        )

        embed = discord.Embed(
            title=tr(guild.id, "ticket_title"),
            description=f"{user.mention}, {tr(guild.id, 'ticket_desc')}",
            color=discord.Color.from_rgb(160, 120, 255)
        )
        if support_role_id:
            await channel.send(f"<@&{support_role_id}>", embed=embed, view=TicketCloseView())
        else:
            await channel.send(embed=embed, view=TicketCloseView())

        await interaction.response.send_message(f"{tr(guild.id, 'ticket_created')}: {channel.mention}", ephemeral=True)

class TicketsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.add_view(TicketCreateView(self.bot))
        self.bot.add_view(TicketCloseView())

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def sendtickets(self, ctx):
        embed = discord.Embed(
            title=tr(ctx.guild.id, "ticket_title"),
            description=tr(ctx.guild.id, "ticket_desc"),
            color=discord.Color.from_rgb(160, 120, 255)
        )
        await ctx.send(embed=embed, view=TicketCreateView(self.bot))

async def setup(bot):
    await bot.add_cog(TicketsCog(bot))
