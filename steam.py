import discord
from discord.ext import commands
from discord.utils import get
import requests
from bs4 import BeautifulSoup
import urllib.request
import time, json, pprint, os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('TRACKER_CSGO_TOKEN')

class CSGO(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name='csgo', aliases=['cs'])
    async def csgo(self, ctx, username):
        """!cs <steamId> | Show CSGO stats"""
        await ctx.channel.purge(limit=1)
        try:
            url = 'https://public-api.tracker.gg/v2/csgo/standard/profile/steam/'+username
            session = requests.Session()
            response = session.get(url, headers={'TRN-Api-Key':TOKEN,'User-Agent': 'Mozilla/5.0', 'Content-Type' : 'application/json'})
            data = json.load(response.text) 
            pprint.pprint(data)
            player_name =  data['data']['platformInfo']['platformUserHandle']
            steamID = data['data']['platformInfo']['platformUserId']
            avatar = data['data']['platformInfo']['avatarUrl']
            countryCode =  data['data']['userInfo']['countryCode']
            timePlayed = data['data']['segments'][0]['stats']['timePlayed']['displayValue']
            lifetime =  data['data']['segments'][0]['metadata']['name']
            matchesPlayed = data['data']['segments'][0]['stats']['matchesPlayed']['displayValue']
            mvp = data['data']['segments'][0]['stats']['mvp']['displayValue']
            wlPercentage = data['data']['segments'][0]['stats']['wlPercentage']['displayValue']
            wins =  data['data']['segments'][0]['stats']['wins']['displayValue']
            losses =  data['data']['segments'][0]['stats']['losses']['displayValue']
            kills =  data['data']['segments'][0]['stats']['kills']['displayValue']
            deaths =  data['data']['segments'][0]['stats']['deaths']['displayValue']
            kd =  data['data']['segments'][0]['stats']['kd']['displayValue']
            headshotPct =  data['data']['segments'][0]['stats']['headshotPct']['displayValue']
            bombsPlanted =  data['data']['segments'][0]['stats']['bombsPlanted']['displayValue']

            # print(player_name, lifetime)
            
            #MAKE EMBEDS
            embed=discord.Embed(title="Lifetime Overview ", description=f"`{player_name}`  ⌚{timePlayed}   🎮{matchesPlayed}", color=0xff0000)
            embed.set_author(name=ctx.message.author.name, icon_url=avatar)
            embed.set_thumbnail(url=avatar)
            embed.add_field(name="K/D", value=f"{kd}", inline=True)
            embed.add_field(name="Headshot %", value=f"{headshotPct}", inline=True)
            embed.add_field(name="Win %", value=f"{wlPercentage}", inline=True)
            embed.add_field(name="MVP", value=f"{mvp}", inline=True)
            embed.add_field(name="Wins", value=f"{wins}", inline=True)
            embed.add_field(name="Losses", value=f"{losses}", inline=True)
            embed.add_field(name="Kills", value=f"{kills}", inline=True)
            embed.add_field(name="Deaths", value=f"{deaths}", inline=True)
            embed.add_field(name="Bombs Planted", value=f"{bombsPlanted}", inline=True)
            embed.set_footer(text=f"SteamID: {steamID}                                                                                                                                                                                                      {countryCode}")
            await ctx.send(embed=embed)
            
        except urllib.request.HTTPError as e:
            if e.code==404:
                print(f"{url} is not found")
            elif e.code==503:
                print(f'{url} base webservices are not available')
            else:
                print('http error',e)
                
def setup(client):
    client.add_cog(CSGO(client))

