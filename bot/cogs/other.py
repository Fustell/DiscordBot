import nextcord
from nextcord import Status, Activity, ActivityType, Colour
from nextcord.ext.commands import Bot, Cog

from bot.misc import Env
from bot.utils.GPTHandler import GPTHandler
from datetime import datetime

TESTING_GUILD_ID = 954101176532615408

openai_api = Env.OPENAI_API_KEY
chatGPT = GPTHandler(openai_api)


# todo: OtherCogs
class __MainOtherCog(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @Cog.listener()
    async def on_ready(self) -> None:
        channel = self.bot.get_channel(1074413253893046362)
        embed = nextcord.Embed(title="Technical messages",
                               description=f'{self.bot.user.display_name}#{self.bot.user.discriminator} '
                                           f'was started at {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}',
                               color=Colour.green())
        await channel.send(embed=embed)
        await self.bot.change_presence(status=Status.do_not_disturb,
                                       activity=Activity(type=ActivityType.playing, name="In developing"))
        print(f'[LOGS]: {self.bot.user.display_name}#{self.bot.user.discriminator} was started at '
              f'{len(self.bot.guilds)} servers')

    @Cog.listener()
    async def on_message(self, message):

        if message.author.bot:
            return

        if not message.content.strip().startswith("!"):
            return

        if len(message.content.strip()) < 10:
            return message.channel.send(content="`Мінімальна довжина запиту 10 символа`")

        if message.channel.name == "🤖chatgpt🤖":
            try:
                reply_message = await message.channel.send("`Очікуйте, бот генерує відповідь`")
                prompt = message.content[1::]
                test_message = ""
                response = await chatGPT.make_response(prompt, message.author.id)
                n = 2000
                divided_messages = [response[i:i + n] for i in range(0, len(response), n)]
                for i in divided_messages:
                    embed = nextcord.Embed(title=self.bot.user.display_name,
                                           description=f"`{i}`",
                                           timestamp=datetime.utcnow(),
                                           color=0x000000)
                    embed.set_footer(text="Created by Romko")
                    embed.set_author(name=message.author.display_name)
                    await message.channel.send(embed=embed)
                await reply_message.delete()
            except Exception as e:
                embed = nextcord.Embed(title=f"Error occured",
                                       description=f"{str(e)}",
                                       timestamp=datetime.utcnow(),
                                       color=0xff0000)
                embed.set_author(name=message.author.display_name)
                embed.set_footer(text="Created by Romko")
                await message.channel.send(embed=embed, content="")

    @Cog.listener()
    async def on_member_join(self, member):
        guild = member.guild
        if guild.system_channel is not None:
            to_send = f"Користувач {member.mention} приєднався до серверу"
            await guild.system_channel.send(to_send)


def register_other_cogs(bot: Bot) -> None:
    bot.add_cog(__MainOtherCog(bot))
