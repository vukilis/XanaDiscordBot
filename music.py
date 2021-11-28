import asyncio
import discord
from discord.ext import commands
import youtube_dl
import voice
from discord.utils import get
import requests
from bs4 import BeautifulSoup
import re
import urllib.request
import time

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
        
    @commands.command()
    async def join(self, ctx):
        """!join | Join to voice"""
        if ctx.author.voice is None:
            await ctx.channel.send("⚠️ Please join in a voice channel! ⚠️")
        voice_channel = ctx.author.voice.channel
        if ctx.voice_client is None:
            await ctx.channel.send("🎶 Hello Friend, lets music! 🎶")
            await voice_channel.connect()
        else:
            await ctx.channel.send("You moved me to another voice channel! ☑️")
            await ctx.voice_client.move_to(voice_channel)
    
    @commands.command(name='disconnect', aliases=['dc', 'stop'])
    async def disconnect(self, ctx):
        """!dc | Disconnect from voice"""
        await ctx.channel.send("Goodbye! 👋 ⏏️")
        await ctx.voice_client.disconnect()

    @commands.command()
    async def play(self, ctx, url):
        """!play | Play the music"""
        ctx.voice_client.stop()
        # voice_channel = ctx.author.voice.channel
        # if ctx.voice_client is None:
        #     await ctx.channel.send("🎶 Hello Friend, lets music! 🎶")
        #     await voice_channel.connect()
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
            info = ydl.extract_info(url, download=False)
            url2 = info['formats'][0]['url']
            voice_ch.play(discord.FFmpegPCMAudio(executable="V:/Program Files (x86)/JDownloader/tools/Windows/ffmpeg/x64/ffmpeg.exe", source=url2, **FFMPEG_OPTIONS))
            # source = await discord.FFmpegOpusAudio.from_probe(url2, **FFMPEG_OPTIONS)
            # voice_ch.play(source)
            if 'entries' in info:
                video = info['entries'][0]       
            else:
                video = info
            print(YDL_OPTIONS['outtmpl'])
            print ("{0}".format((info['title'])))
            await ctx.channel.send("🔹" + "{0}".format((info['title'])) + " ▶️")
            # print(video)
            video_url = video['url']
        
    @commands.command()
    async def pause(self, ctx):
        """!pause | Pause the music"""
        await ctx.channel.send("Paused ⏸️")
        await ctx.voice_client.pause()
        
    @commands.command()
    async def resume(self, ctx):
        """!pause | Resume the music"""
        await ctx.channel.send("Resume ▶️")
        await ctx.voice_client.resume() 

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
                embed = discord.Embed(title="GIGATRON", description="What is on sale")
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
        embed = discord.Embed(title=f"Stats for **{channel.name}**", description=f"{'Category: {}'.format(channel.category.name) if channel.category else 'This channel is not in a category'}")
        embed.add_field(name="Channel Guild", value=ctx.guild.name, inline=False)
        embed.add_field(name="Channel id", value=channel.id, inline=False)
        embed.add_field(name="Channel Creaion Time", value=channel.created_at, inline=False)
        
        await ctx.channel.send(embed=embed)

    # @commands.command()
    # async def new(self, ctx):
    #     await ctx.send("Ivalid")

#####make new channel category
    @commands.command(name='category')
    async def category(self ,ctx, role: discord.Role, *, name):
        """!categorty <role> <name> | Create channel category"""
        overwrites = {
            ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False),
            ctx.guild.me: discord.PermissionOverwrite(read_messages=True),
            role: discord.PermissionOverwrite(read_messages=True)
        }
        category = await ctx.guild.create_category(name=name, overwrites=overwrites)
        await ctx.send(f"Hey friend, I made {category.name} for you!")
    
#####make new text channel
    @commands.command(name='channel')
    async def channel(self ,ctx, role: discord.Role, *, name):
        """!categorty <role> <name> | Create text channel"""
        overwrites = {
            ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False),
            ctx.guild.me: discord.PermissionOverwrite(read_messages=True),
            role: discord.PermissionOverwrite(read_messages=True)
        }
        channel = await ctx.guild.create_text_channel(name=name, overwrites=overwrites)
        await ctx.send(f"Hey friend, I made {channel.name} for you!")


def setup(client):
    client.add_cog(Music(client))