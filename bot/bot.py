# IMPORTING THE PACKAGES
import os, json, nextcord, logging, datetime, random, time
from pathlib import Path

from nextcord import Activity, ActivityType
from nextcord.ext import commands

# LOADING EXTENSIONS FROM UTILS
from util.mongo import Document
from util.constants import Client, Database



# CONFIGURATIONS
cwd = Path(__file__).parents[0]
cwd = str(cwd)
print(f"{cwd}\n-------")


# GETTING PREFIX FROM DATABASE
async def get_prefix(bot, message):
    if not message.guild:
        return commands.when_mentioned_or(Client.default_prefix)(bot, message)

    try:
        data = await client.config.find(message.guild.id)

        # Make sure we have a useable prefix
        if not data or "prefix" not in data:
            return commands.when_mentioned_or(Client.default_prefix)(bot, message)
        return commands.when_mentioned_or(data["prefix"])(bot, message)
    except:
        return commands.when_mentioned_or(Client.default_prefix)(bot, message)


# Changing Bot Presense
activity = Activity(type=ActivityType.playing, name="In developing")

# Intents
intents = nextcord.Intents.default()
intents.members = True
intents.message_content = True
    
# OUR CLIENT     
client = commands.AutoShardedBot(command_prefix=get_prefix, case_insensitive=True, activity=activity, intents=intents)


client.bot_version = Client.bot_version
client.guild_id= Client.guild_id
logging.basicConfig(level=logging.INFO)



# EVENTS
@client.event
async def on_ready():
    
    # Adding the start time
    client.start_time = time.time()
    start_log = client.get_channel(1080185431708160111)

    # On ready, print some details to standard out
    print(
        f"-----\nLogged in as: {client.user.name} : {client.user.id}\n"
        f"-----\nMy current prefix is: /\n"
        f"-----\nNumbers of servers: {len(client.guilds)}\n-----"
    )
    embed = nextcord.Embed(title="Technical messages",
                           description=f'```{client.user.display_name}#{client.user.discriminator} '
                                       f'was started at {datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")}```',
                           color=nextcord.Colour.green())
    await start_log.send(embed=embed)

    # Adding MongoDB to our bot
    client.db = Database.db
    client.config = Document(client.db, "config")   
    print("Initialized Database\n-----")
    for document in await client.config.get_all():
        print(f'{document}\n-----')

 
        
    for cog in client.cogs:
        print(f"Loaded {cog} \n-----")  



# RUNNING OUR CLIENT
if __name__ == "__main__":

    for file in os.listdir(cwd + "/cogs"):
        if file.endswith(".py") and not file.startswith("__pycache"):
            client.load_extension(f"cogs.{file[:-3]}")

client.run(Client.token)


           

