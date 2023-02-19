from nextcord.ext.commands import Cog, Bot, is_owner
from nextcord import Interaction
import nextcord


class Code(nextcord.ui.Modal):
    def __init__(self, bot):
        self.bot = bot

        super().__init__(
            "Code runner"
        )

        self.description = nextcord.ui.TextInput(
            label="Description",
            style=nextcord.TextInputStyle.paragraph,
            placeholder="Run some code here",
            required=True,
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

    @nextcord.slash_command(name="eval", description="Run some code")
    @is_owner()
    async def _eval(self, interaction: Interaction):
        modal = Code(self.bot)
        await interaction.response.send_modal(modal)


def register_admin_cogs(bot: Bot) -> None:
    bot.add_cog(__MainAdminCog(bot))