from nextcord.ext.commands import Cog, Bot, command
from nextcord import Interaction
import nextcord


class Code(nextcord.ui.Modal):
    def __init__(self):
        super().__init__(
            "Code runner"
        )

        self.description = nextcord.ui.TextInput(
            label="Description",
            style=nextcord.TextInputStyle.paragraph,
            placeholder="Run some code here",
            required=False,
            max_length=1800,
        )
        self.add_item(self.description)

    async def callback(self, interaction: nextcord.Interaction) -> None:
        try:
            eval(self.description.value)
        except Exception as e:
            await interaction.send(e, ephemeral=True)


# todo: AdminCogs
class __MainAdminCog(Cog):

    def __init__(self, bot: Bot):
        self.bot = bot

    @nextcord.slash_command(name="code", description="Run some code")
    async def code(self, interaction: Interaction):
        modal = Code()
        await interaction.response.send_modal(modal)


def register_admin_cogs(bot: Bot) -> None:
    bot.add_cog(__MainAdminCog(bot))