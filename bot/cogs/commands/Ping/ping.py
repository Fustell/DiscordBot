import nextcord
from nextcord.ext import commands


class Ping(commands.Cog, description="Get the ping of the bot."):
    COG_EMOJI = "🏓"

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="ping", description="Returns the ping of the bot.")
    async def ping(self, ctx):
        await ctx.send(f"**{self.COG_EMOJI} Ping: `{round(self.bot.latency*1000)}ms`**")

    @nextcord.slash_command(name="ping", description="Returns the ping of the bot.")
    async def ping_slash(self, interaction: nextcord.Interaction):
        await interaction.response.send_message(f"**{self.COG_EMOJI} Ping: `{round(self.bot.latency*1000)}ms`**")