from nextcord import Status, Activity, ActivityType
from nextcord.ext.commands import Bot, Cog, Context


# todo: OtherCogs
class __MainOtherCog(Cog):

    def __init__(self, bot: Bot):
        self.bot = bot

    @Cog.listener()
    async def on_ready(self) -> None:
        await self.bot.change_presence(status=Status.do_not_disturb,
                                       activity=Activity(type=ActivityType.playing,name="In developing"))
        print(f'[LOGS]: {self.bot.user.display_name}#{self.bot.user.discriminator} was started at '
              f'{len(self.bot.guilds)} servers')


def register_other_cogs(bot: Bot) -> None:
    bot.add_cog(__MainOtherCog(bot))