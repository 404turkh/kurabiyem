import discord
from utils.translations import tr

class CloseOnlyView(discord.ui.View):
    def __init__(self, guild_id: int):
        super().__init__(timeout=180)
        self.guild_id = guild_id

    @discord.ui.button(label="Close", style=discord.ButtonStyle.danger)
    async def close_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        button.label = tr(self.guild_id, "close")
        await interaction.response.edit_message(content=tr(self.guild_id, "close"), embed=None, view=None)
