import os
import discord
from discord import message
from dotenv import load_dotenv
from discord.ext import commands
import music, requests
from discord.utils import get
from discord_components import *
from bs4 import BeautifulSoup

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
    channel_id_server = [913805324966830130, 913861842235953182]
    for i in channel_id_server:
        await client.get_channel(i).send('Xana is awake, say \"!hello\" to Xana')
    DiscordComponents(client)

@client.event
async def on_message(message):
    username = message.author.display_name
    if message.author == client.user:
        return 
    if message.content.startswith('!hello'):
    
        await message.channel.send('Hello ' +username+ ', my name is Xana. \nFor commands type !help')
    await client.process_commands(message)
    
#NE RADIIII!!!!!!!!!!!!!
# @client.command()      
# async def winwin(ctx):
#     await ctx.send(
#         "Choose component",
#         components = [
#             ActionRow(
#                 Button(style=ButtonStyle.blue, label='Maticna'),
#                 Button(style=ButtonStyle.red, label='Ram'),
#                 Button(label='cpu')
#             )
#         ]
#     )
#     # components = discord.Component
#     interaction1 = await client.wait_for("button_click", check = lambda i: i.component.label.startswith("Maticna"))
#     await interaction1.respond(content = await maticna(ctx))
    

#     interaction2 = await client.wait_for("button_click", check = lambda i: i.component.label.startswith("Ram"))
#     await interaction2.respond(content = await ram(ctx))


# async def maticna(ctx):
#     url = "https://www.winwin.rs/filters/product/action/?cat=309"
#     session = requests.Session()
#     response = session.get(url, headers={'User-Agent': 'Mozilla/5.0'})
#     # print(response.status_code)
#     soup = BeautifulSoup(response.content,'html5lib')
#     product = soup.select("h2.product-name span", limit=12)
#     products = []
#     for i in product:
#         products.append(i.get_text().strip())
#     for x in range(len(products)):
#         await ctx.channel.send(products[x])

# async def ram(ctx):
#     url = "https://www.winwin.rs/filters/product/action/?cat=312"
#     session = requests.Session()
#     response = session.get(url, headers={'User-Agent': 'Mozilla/5.0'})
#     # print(response.status_code)
#     soup = BeautifulSoup(response.content,'html5lib')
#     product = soup.select("h2.product-name span", limit=12)
#     products = []
#     for i in product:
#         products.append(i.get_text().strip())
#     for x in range(len(products)):
#         await ctx.channel.send(products[x])

#/NE RADIIII!!!!!!!!!!!!!
client.run(TOKEN)