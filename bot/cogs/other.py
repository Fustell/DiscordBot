from nextcord import Status, Activity, ActivityType
from nextcord.ext.commands import Bot, Cog, Context

from bot.misc import Env
from bot.utils.GPTHandler import GPTHandler

TESTING_GUILD_ID = 954101176532615408

openai_api = Env.OPENAI_API_KEY
chatGPT = GPTHandler(openai_api)


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

    @Cog.listener()
    async def on_message(self, message: str):

        # developers = ["292963893725102080"]
        #
        # if str(message.author.id) not in developers:
        #     return

        if message.author.bot:
            return

        if message.guild.id == TESTING_GUILD_ID and message.channel.id == 1076864191379550248:
            answer_message = await message.channel.send("`Очікуйте, бот генерує відповідь`")
            response = await chatGPT.make_response(message.content)
            await answer_message.edit(content=response)


def register_other_cogs(bot: Bot) -> None:
    bot.add_cog(__MainOtherCog(bot))
