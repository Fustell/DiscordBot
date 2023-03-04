import io
import os
import traceback
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
                chatgpt_log = self.bot.get_channel(1081352502995333250)
                reply_message = await message.channel.send("`Очікуйте, бот генерує відповідь`")
                prompt = message.content[1::]

                chatgpt_embed = nextcord.Embed(title=f"ChatGPT Log",
                                               description=f"```\nUSERNAME: {message.author.display_name}"
                                                           f"\nID: {message.author.id}\nSERVER NAME: {message.guild.name}"
                                                           f"\nSERVER ID: {message.guild.id}"
                                                           f"\nPROMPT:{prompt}```",
                                               timestamp=datetime.utcnow(),
                                               color=0x069e03)
                await chatgpt_log.send(embed=chatgpt_embed)
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

                    chatgpt_embed = nextcord.Embed(title=f"ChatGPT Log",
                                           description=f"```\nThis is answer to the prompt: {prompt}\nANSWER: {i}```",
                                           timestamp=datetime.utcnow(),
                                           color=0x069e03)
                    await chatgpt_log.send(embed=chatgpt_embed)
                await reply_message.delete()
            except Exception as e:
                error_log = self.bot.get_channel(1080185530911830086)
                embed = nextcord.Embed(title=f"ChatGPT Error",
                                       description=f"```py\n{io.StringIO().getvalue()}{traceback.format_exc()}\n```",
                                       timestamp=datetime.utcnow(),
                                       color=0xff0000)
                await error_log.send(embed=embed, content="")
