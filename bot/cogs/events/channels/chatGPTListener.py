import os
from datetime import datetime

import nextcord
from nextcord.ext import commands

from util.api import ChatGPTService

openai_api = os.getenv("OPENAI_API_KEY")
chatGPT = ChatGPTService(openai_api)


class ChatGPTListener(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
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
