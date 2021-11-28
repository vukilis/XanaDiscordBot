import os
import discord
from discord import message
from dotenv import load_dotenv
from discord.ext import commands
import music
from discord.utils import get

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')


# class CustomHelpCommand(commands.HelpCommand):
#     def __init__(self):
#         super().__init__()
        
#     async def send_bot_help(self, mapping):
#         for cog in mapping:
#             await self.get_destination().send(f'{cog.qualified_name}: {[command.name for command in mapping[cog]]}')
    
#     async def send_cog_help(self, cog):
#         await self.get_destination().send(f'{cog.qualified_name}: {[command.name for command in cog.get_commands()]}')
    
#     async def send_group_help(self, group):
#         await self.get_destination().send(f'{group.name}: {[command.name for index, command in enumerate(group.commands)]}')
    
#     async def send_command_help(self, command):
#         await self.get_destination().send(command.name)

cogs = [music]
client = commands.Bot(command_prefix='!', intents = discord.Intents.all())

for i in range(len(cogs)):
    cogs[i].setup(client)

# user = bot.get_user(user_id)
# username = client.get_user(user_id)

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    await client.get_channel(913805324966830130).send('Xana is awake, say \"!hello\" to Xana')
@client.event
async def on_message(message):
    username = message.author.display_name
    if message.author == client.user:
        return 
    if message.content.startswith('!hello'):
        await message.channel.send('Hello ' +username+ ', my name is Xana. \nFor commands type !help')
    await client.process_commands(message)


client.run(TOKEN)