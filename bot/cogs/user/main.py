import nextcord
from nextcord.ext.commands import Cog, Bot, command

from bot.misc import Env
from bot.utils.GPTHandler import GPTHandler

TESTING_GUILD_ID = Env.TESTING_GUILD_ID


# todo: UserCogs
class __MainUserCog(Cog):

    def __init__(self, bot: Bot):
        self.bot = bot

    @command()
    async def hello(self, ctx):
        await ctx.send("hi")

    @nextcord.slash_command(description="Get ping of bot", guild_ids=[TESTING_GUILD_ID])
    async def ping(self, interaction: nextcord.Interaction) -> None:
        await interaction.send(f"Ping: {round(self.bot.latency * 1000)} ms")


def register_user_cogs(bot: Bot) -> None:
    bot.add_cog(__MainUserCog(bot))
