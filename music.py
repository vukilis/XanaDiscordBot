import asyncio
import discord
from discord.ext import commands, tasks
import youtube_dl
import voice
from discord.utils import get
import requests
from bs4 import BeautifulSoup
import re
import urllib.request
import time, json

# def get_voice_state(self, ctx: commands.Context):
    #     state = self.voice_states.get(ctx.guild.id)
    #     if not state or not state.exists:
    #         state = voice.VoiceState(self.bot, ctx)
    #         self.voice_states[ctx.guild.id] = state

    #     return state
    
class Music(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot 
        self.song_queue = {}
        
    @commands.command(name='join')
    async def join(self, ctx):
        """!join | Join to voice"""
        if ctx.author.voice is None:
            e = discord.Embed(title="⚠️ Please join in a voice channel! ⚠️", color=discord.Color.green())
            await ctx.send(embed=e)
        voice_channel = ctx.author.voice.channel
        await voice_channel.connect()
        if ctx.voice_client is None:
            e = discord.Embed(title="🎶 Hello Friend, lets music! 🎶", color=discord.Color.green())
            await ctx.send(embed=e)
            await voice_channel.connect()
        if Music.play(self, ctx):
            await ctx.voice_client.move_to(voice_channel)
        else:
            e = discord.Embed(title="You moved me to another voice channel! ☑️", color=discord.Color.green())
            await ctx.send(embed=e)
            await ctx.voice_client.move_to(voice_channel)
    
    @commands.command(name='disconnect', aliases=['dc', 'stop'])
    async def disconnect(self, ctx):
        """!dc | Disconnect from voice"""
        e = discord.Embed(title="Goodbye! 👋 ⏏️", color=discord.Color.red())
        await ctx.send(embed=e)
        await ctx.voice_client.disconnect()
        
###Bot leave channel if inactive 5 min###
    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after): 
        if not member.id == self.bot.user.id:
            return
        elif before.channel is None:
            voice = after.channel.guild.voice_client
            time = 0
            while True:
                await asyncio.sleep(1)
                time = time + 1
                if voice.is_playing() and not voice.is_paused():
                    time = 0
                if time == 300:
                    await voice.disconnect()
                if voice.is_playing() == False and time == 300:
                    await voice.disconnect()
                    break
                if not voice.is_connected():
                    break
    
    @commands.command()
    async def play(self, ctx, url):
        """!play | Play the music"""
        await ctx.channel.purge(limit=1)
        await Music.join(self, ctx)
        ctx.voice_client.stop()
        voice_channel = ctx.author.voice.channel
        voice_ch = get(self.bot.voice_clients, guild=ctx.guild)
        await ctx.guild.change_voice_state(channel=voice_channel, self_mute=False, self_deaf=True)

        YDL_OPTIONS = {
            'format': 'bestaudio/best',
            'extractaudio': True,
            'audioformat': 'mp3',
            'outtmpl': '%(title)s',
            'restrictfilenames': True,
            'nocheckcertificate': True,
            'ignoreerrors': False,
            'logtostderr': False,
            'quiet': True,
            'no_warnings': True,
            'source_address': '0.0.0.0',
        }
        FFMPEG_OPTIONS = {
            'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
            'options': '-vn',
        }
        voice_ch = ctx.voice_client
        with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
            if voice_channel and not voice_ch.is_playing():
                info = ydl.extract_info(url, download=False)
                url2 = info['formats'][0]['url']
                voice_ch.play(discord.FFmpegPCMAudio(executable="ffmpeg/ffmpeg", source=url2, **FFMPEG_OPTIONS))
                if 'entries' in info:
                    video = info['entries'][0]       
                else:
                    video = info
                print(YDL_OPTIONS['outtmpl'])
                print ("{0}".format((info['title'])))
                e = discord.Embed(title="🔹" + "{0}".format((info['title'])) + " ▶️", color=discord.Color.green())
                await ctx.send(embed=e)
                video_url = video['url']
        
    @commands.command()
    async def pause(self, ctx):
        """!pause | Pause the music"""
        await ctx.channel.purge(limit=1)
        e = discord.Embed(title="Paused ⏸️", color=discord.Color.dark_purple())
        await ctx.send(embed=e)
        ctx.voice_client.pause()
        
    @commands.command()
    async def resume(self, ctx):
        """!resume | Resume the music"""
        await ctx.channel.purge(limit=1)
        e = discord.Embed(title="Resume ▶️", color=discord.Color.dark_purple())
        await ctx.send(embed=e)
        ctx.voice_client.resume() 
    
    @commands.command(name='gigatron')
    async def gigatron(self ,ctx):
        """!gigatron | Show gigatron sales"""
        
        url = 'https://gigatron.rs/akcije'
        try:
            with urllib.request.urlopen(url) as response:
                html = response.read().decode('utf-8')
                headers = {'User-Agent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36"}
                page = requests.get(url,headers= headers, timeout=(3.05, 27))
                soup = BeautifulSoup(page.content,'html5lib')
            #PRODUCTS
                products = []
                product = soup.select("a.card-box h2", limit=12)
                for i in product:
                    products.append(i.get_text().strip())
                pr = '\n'.join(map(str, products))
                print(pr)
            #DATES
                dates = []
                date = soup.select("div.date-published", limit=12)
                for i in date:
                    dates.append(i.get_text().strip())
                dt = '\n'.join(map(str, dates))
                print(dt)
            #MAKE EMBEDS
                embed = discord.Embed(title="GIGATRON", description="What is on sale", color = discord.Color.from_rgb(255, 255, 0))
                embed.add_field(name="NAME", value=pr)
                embed.add_field(name="DATE", value=dt)
                embed.set_thumbnail(url = 'https://raw.githubusercontent.com/vukilis/XanaDiscordBot/main/gigatron.png')
                await ctx.channel.send(embed=embed)

        except urllib.request.HTTPError as e:
            if e.code==404:
                print(f"{url} is not found")
            elif e.code==503:
                print(f'{url} base webservices are not available')
                ## can add authentication here 
            else:
                print('http error',e)

#####get channel stats
    @commands.command(name='channel_stats', aliases=['stats', 'chstats'])
    async def channel_stats(self ,ctx):
        """!stats | Show channel stats"""
        channel = ctx.channel
        embed = discord.Embed(title=f"Stats for **{channel.name}**", description=f"{'Category: {}'.format(channel.category.name) if channel.category else 'This channel is not in a category'}", color=discord.Color.green())
        embed.add_field(name="Channel Guild", value=ctx.guild.name, inline=False)
        embed.add_field(name="Channel id", value=channel.id, inline=False)
        embed.add_field(name="Channel Creaion Time", value=channel.created_at, inline=False)
        
        await ctx.channel.send(embed=embed)

#####make new channel category
    @commands.command(name='category')
    @commands.is_owner()
    async def category(self ,ctx, role: discord.Role, *, name):
        """!category <role> <name> | Create channel category"""
        overwrites = {
            ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False),
            ctx.guild.me: discord.PermissionOverwrite(read_messages=True),
            role: discord.PermissionOverwrite(read_messages=True)
        }
        category = await ctx.guild.create_category(name=name, overwrites=overwrites)
        
        e = discord.Embed(title=f"Hey friend, I made {category.name} for you!", color=discord.Color.dark_purple())
        await ctx.send(embed=e)
        # await ctx.send(f"Hey friend, I made {category.name} for you!")
    
#####make new text channel
    @commands.command(name='channel')
    @commands.is_owner()
    async def channel(self ,ctx, role: discord.Role, *, name):
        """!channel <role> <name> | Create text channel"""
        overwrites = {
            ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False),
            ctx.guild.me: discord.PermissionOverwrite(read_messages=True),
            role: discord.PermissionOverwrite(read_messages=True)
        }
        channel = await ctx.guild.create_text_channel(name=name, overwrites=overwrites)
        e = discord.Embed(title=f"Hey friend, I made {channel.name} for you!", color=discord.Color.dark_purple())
        await ctx.send(embed=e)
        # await ctx.send(f"Hey friend, I made {channel.name} for you!")
    
    @commands.command(name='Invite link', aliases=['inv'])
    async def create_invite(self, ctx):
        """!inv | Create instant invite"""
        link = await ctx.channel.create_invite(max_age = 300)
        await ctx.send(link)


async def setup(client):
    await client.add_cog(Music(client))