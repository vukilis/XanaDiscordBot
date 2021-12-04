import os, json
import discord
from discord import message
# from dotenv import load_dotenv
from discord.ext import commands, tasks
import music, rocket_league, steam
from discord.utils import get
from discord_components import *
from datetime import datetime
import keep_alive

# load_dotenv()
# TOKEN = os.getenv('DISCORD_TOKEN')
my_secret = os.environ['DISCORD_TOKEN']

cogs = [music, rocket_league, steam]
client = commands.Bot(command_prefix='!', owner_id = 269115882251223052, intents = discord.Intents.all())
client.launch_time = datetime.utcnow()

for i in range(len(cogs)):
    cogs[i].setup(client)

@client.event
async def on_ready(*args, **kwargs):
    change_status.start()
    print(f'{client.user} has connected to Discord!')
    channel_id_server = [913861842235953182]
    # await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="!help"))
    for i in channel_id_server:
        await client.get_channel(i).send('Xana is awake, say \"!hello\" to Xana')
    # DiscordComponents(client)

@tasks.loop(seconds=3)
async def change_status():
  await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="!help"))

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
    channel = client.get_channel[321712782481293322]
    
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
    channel = client.get_channel[321712782481293322]
    
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
    channel = client.get_channel(768871813936840779)
    if voice_state is None:
        return 
    if len(voice_state.channel.members) == 1:
        await channel.send("Goodbye! 👋 ⏏️")
        await voice_state.disconnect()

keep_alive.keep_alive()
client.run(my_secret)