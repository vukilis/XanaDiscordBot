import os, json
import discord
from discord import message
from dotenv import load_dotenv
from discord.ext import commands
import music, requests, rocket_league, steam
from discord.utils import get
from discord_components import *
from bs4 import BeautifulSoup
from datetime import datetime

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

cogs = [music, rocket_league, steam]
client = commands.Bot(command_prefix='!', owner_id = 269115882251223052, intents = discord.Intents.all())

for i in range(len(cogs)):
    cogs[i].setup(client)

@client.event
async def on_ready(*args, **kwargs):
    print(f'{client.user} has connected to Discord!')
    channel_id_server = [913805324966830130]
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="!help"))
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

@client.event
async def on_member_join(member):
    channel = client.get_channel(916150378381328386)
    
    embed= discord.Embed(
        title=f'Welcome',
        description=f'{member.mention} Joined {member.guild.name}',
        color=discord.Color.random(),
        timestamp=datetime.utcnow(),
        ).add_field(
            name=f'Attention',
            value=f'Please, wait to admin to give you an role', 
            inline=False
        ).add_field(
            name=f'Total members',
            value=f'{member.guild.member_count}', 
            inline=False
        ).set_footer(
            text=f'{member.name} just joined'
        ).set_thumbnail(
            url = member.avatar_url
        )
    
    await channel.send(embed=embed)
    
@client.event
async def on_member_remove(member):
    channel = client.get_channel(916150378381328386)
    
    embed= discord.Embed(
        title=f'Goodbye',
        description=f'{member.mention} has left {member.guild.name}',
        color=discord.Color.random(),
        timestamp=datetime.utcnow(),
        ).add_field(
            name=f'Total members',
            value=f'{member.guild.member_count}', 
            inline=False
        ).set_footer(
            text=f'{member.name} just left'
        ).set_thumbnail(
            url = member.avatar_url
        )
    
    await channel.send(embed=embed)

@client.command(name='avatar')
async def avatar(ctx, member: discord.Member):
    """!avatar <@mention> | Show User Avatar"""
    await ctx.channel.purge(limit=1)
    show_avatar = discord.Embed(
        color = discord.Color.dark_blue()
    )
    show_avatar.set_image(url='{}'.format(member.avatar_url))
    await ctx.send(embed=show_avatar)

@client.command()
async def uptime(ctx):
    """!uptime | Show channel uptime"""
    delta_uptime = datetime.utcnow() - client.launch_time
    hours, remainder = divmod(int(delta_uptime.total_seconds()), 3600)
    minutes, seconds = divmod(remainder, 60)
    days, hours = divmod(hours, 24)
    e = discord.Embed(title=f"I've been up for {days}d : {hours}h : {minutes}m : {seconds}s", color=discord.Color.green())
    await ctx.send(embed=e)

@client.command()
async def ping(ctx):
    """!ping | Show User Latency"""
    e = discord.Embed(title=f"Latency: {round(client.latency*1000)}ms", color=discord.Color.green())
    await ctx.send(embed=e)

###Bot leave channel if empty###
@client.event
async def on_voice_state_update(member, before, after):
    voice_state = member.guild.voice_client
    channel1 = client.get_channel(913805324966830130)
    if voice_state is None:
        return 
    if len(voice_state.channel.members) == 1:
        await channel1.send("Goodbye! 👋 ⏏️")
        await voice_state.disconnect()

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