import discord
from discord.ext import commands
# from discord.utils import get
import requests
from bs4 import BeautifulSoup
import urllib.request
import time, json, pprint

class RL(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot 
    
    @commands.command(name='epic')
    async def epic(self, ctx):
        """!epic | Show epic server status"""
        try:
            url = "https://status.epicgames.com/api/v2/status.json"
            session = requests.Session()
            response = session.get(url, headers={'User-Agent': 'Mozilla/5.0'})
            data = json.loads(response.text)
            
            name = data['page']['name']
            status =  data['status']['description']
            # pprint.pprint(status)
            
            #MAKE EMBEDS
            embed = discord.Embed(title="EPIC STATUS", description=f'`{name}`', color = discord.Color.from_rgb(102, 204, 0))
            embed.add_field(name="Mode:", value=status)   
            embed.set_thumbnail(url = 'https://raw.githubusercontent.com/vukilis/XanaDiscordBot/main/epic.png')
            await ctx.channel.purge(limit=1)
            await ctx.channel.send(embed=embed)
        except urllib.request.HTTPError as e:
            if e.code==404:
                print(f"{url} is not found")
            elif e.code==503:
                print(f'{url} base webservices are not available')
            else:
                print('http error',e)
                
    @commands.command(name='rocket_league', aliases=['rl'])
    async def rocket_league(self, ctx, platform, username):
        """!rl <platform> <ign> | Show rocket league stats"""
        await ctx.channel.purge(limit=1)
        try:
            url = "https://api.tracker.gg/api/v2/rocket-league/standard/profile/"+platform+"/"+username+"/segments/playlist?season=19"
            print(url)
            session = requests.Session()
            response = session.get(url, headers={'User-Agent': 'Mozilla/5.0'})
            soup = BeautifulSoup(response.content,'html5lib')
            data = json.loads(soup.text)
            # pprint.pprint(data)
            
            duo_name =  data['data'][1]['metadata']['name']
            duo_rank_name = data['data'][1]['stats']['tier']['metadata']['name']
            duo_rank = data['data'][1]['stats']['division']['metadata']['name']
            duo_matches = data['data'][1]['stats']['matchesPlayed']['displayValue']
            duo_rating = data['data'][1]['stats']['rating']['displayValue']
            duo_tier = data['data'][1]['stats']['tier']['metadata']['iconUrl']
            duo_streak = data['data'][1]['stats']['winStreak']['displayValue']
            # duo_percentile = data['data'][1]['stats']['rating']['percentile']
            
            doubles_name = data['data'][2]['metadata']['name']
            doubles_rank_name = data['data'][2]['stats']['tier']['metadata']['name']
            doubles_rank = data['data'][2]['stats']['division']['metadata']['name']
            doubles_matches = data['data'][2]['stats']['matchesPlayed']['displayValue']
            doubles_rating = data['data'][2]['stats']['rating']['displayValue']
            doubles_tier = data['data'][2]['stats']['tier']['metadata']['iconUrl']
            doubles_streak = data['data'][2]['stats']['winStreak']['displayValue']
            # doubles_percentile = data['data'][2]['stats']['rating']['percentile']

            standard_name = 'Mode ' + data['data'][3]['metadata']['name']
            standard_rank_name = data['data'][3]['stats']['tier']['metadata']['name']
            standard_rank = data['data'][3]['stats']['division']['metadata']['name']
            standard_matches = data['data'][3]['stats']['matchesPlayed']['displayValue']
            standard_rating = data['data'][3]['stats']['rating']['displayValue']
            standard_tier = data['data'][3]['stats']['tier']['metadata']['iconUrl']
            standard_streak=  data['data'][3]['stats']['winStreak']['displayValue']

            
            url2 = "https://api.tracker.gg/api/v2/rocket-league/standard/profile/"+platform+"/"+username
            session2 = requests.Session()
            response2 = session2.get(url2, headers={'User-Agent': 'Mozilla/5.0'})
            soup2 = BeautifulSoup(response2.content,'html5lib')
            data2 = json.loads(soup2.text) 
            # pprint.pprint(data2)
            platform_name = data2['data']['platformInfo']['platformSlug']
            name = data2['data']['platformInfo']['platformUserHandle']
            seasson_reward = data2['data']['segments'][0]['stats']['seasonRewardLevel']['metadata']['iconUrl']
            seasson_till_reward = data2['data']['segments'][0]['stats']['seasonRewardWins']['displayValue']
            
            duo_percentile = str(int(data2['data']['segments'][1]['stats']['rating']['percentile'])) + '%'
            doubles_percentile = str(int(data2['data']['segments'][2]['stats']['rating']['percentile'])) + '%'
            standard_percentile = str(int(data2['data']['segments'][3]['stats']['rating']['percentile'])) + '%'

        #MAKE EMBEDS
            embed = discord.Embed(title="RL-STATS", description=f'`{name}` `Season Reward Wins: {seasson_till_reward}/10`', color = discord.Color.from_rgb(0, 128, 255))
            embed.add_field(name="Mode:", value=standard_name)
            embed.add_field(name="Rank:", value=standard_rank_name)
            embed.add_field(name="Division:", value=standard_rank + " - Elo: " +standard_rating )
            embed.add_field(name="Better than:", value=standard_percentile + " of players")
            embed.add_field(name="Matches:", value=standard_matches)
            embed.add_field(name="Streak:", value=standard_streak)
            
            embed.add_field(name="Mode:", value=doubles_name)
            embed.add_field(name="Rank:", value=doubles_rank_name)
            embed.add_field(name="Division:", value=doubles_rank + " - Elo: " +doubles_rating )
            embed.add_field(name="Better than:", value=doubles_percentile + "  of players")
            embed.add_field(name="Matches:", value=doubles_matches)
            embed.add_field(name="Streak:", value=doubles_streak)
            
            embed.add_field(name="Mode:", value=duo_name)
            embed.add_field(name="Rank:", value=duo_rank_name)
            embed.add_field(name="Division:", value=duo_rank + " - Elo: " +duo_rating )
            embed.add_field(name="Better than:", value=duo_percentile + "  of players")
            embed.add_field(name="Matches:", value=duo_matches)
            embed.add_field(name="Streak:", value=duo_streak)
            
            embed.set_thumbnail(url = seasson_reward)
            # await ctx.channel.purge(limit=3)
            await ctx.channel.send(embed=embed)
        
        except urllib.request.HTTPError as e:
            if e.code==404:
                print(f"{url} is not found")
            elif e.code==503:
                print(f'{url} base webservices are not available')
            else:
                print('http error',e)
    
async def setup(client):
    await client.add_cog(RL(client))