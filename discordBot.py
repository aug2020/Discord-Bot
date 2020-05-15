from time import sleep
import discord
import riotwatcher
from random import randint
import requests
from discord.ext import commands
from pathlib import Path
import io

bot = commands.Bot(command_prefix = '!')  # client commands begins with !
text_channel_id = 662509235980075032 #global varibale for the text channel id
 #global varaible for the text channel



@bot.event
async def on_ready():
    print('ready')
@bot.event
async def on_guild_join(member):
    print(f'{member} has joined the server')
@bot.event
async def on_guild_remove(member):
    print(f'{member} has left the server')

@bot.command() # prints out ping of computer
async def ping(ctx):
    latency = bot.latency

    await ctx.send(f'{round(latency * 1000)}ms')
@bot.command()
async def joke(ctx): #command that prints out bot jokes
    f = open('WoW.txt')  # open the file
    num = sum(1 for line in open('WoW.txt')) # add up all the lines to genereate a max random number
    num2 = randint(1,num) # genereate the random number line

    lines = f.readlines() #store each line in an array

    await ctx.send(f'{lines[num2]}')

    f.close()
@bot.command()
async def info(ctx,*arg):
    region = f'{arg[0]}'
    name = f'{arg[1]}'

    regionlist = ['na1','br1','eun1','euw1','jp1','kr','la1','la2','oc1','ru','tr1']
    for reg in regionlist:
        if reg == region:
            id = getSummoner(region, name)['id']
            summonerInfo = getinfo(region,id)
            getSum = getSummoner(region,name)

            #text_channel = bot.get_channel(text_channel_id)  # creating the channel the bot will speak into
            #server = bot.get_guild(662509235980075029)  # storing the server the bot will use

            iconId = getSum ['profileIconId']
            tier = summonerInfo[0]['tier']  # the current tier ie bronze,silver etc
            rank = summonerInfo[0]['rank']  # current ranking of player
            lp = summonerInfo[0]['leaguePoints']  # number of lp
            wins = summonerInfo[0]['wins']  # number of wins
            sumlevel = getSum ['summonerLevel']  # summoner level

            accountName = summonerInfo[0]['summonerName']
            emoji = await getemo(f'Emblem_{tier.lower()}min')
            await ctx.send(f'*** ACCOUNT INFORMATION FOR {name.upper()}*** \n Name: {accountName} \n Rank: {tier} {rank} {emoji} \n LP: {str(lp)}')
            break
        else:
            embed = discord.Embed(title='Region list', description='')
            for x in regionlist:
                embed.add_field(name=f'{regionlist.index(x)+1}. {x}',value=f'North America',inline=True)
            await ctx.send(f'There is no region with the  name {region} please try one of these regions',embed=embed)
            break

def getSummoner(region, name): #retrieves summoner base information like the summoner id
    URL = f'https://{region}.api.riotgames.com/lol/summoner/v4/summoners/by-name/'+name+'?api_key='+key
    return requests.get(URL).json()

def getinfo(region,id): # retrieves summoner ranking and etc
    URL = f'https://{region}.api.riotgames.com/lol/league/v4/entries/by-summoner/'+id+'?api_key='+key
    return requests.get(URL).json()

async def getemo(name):
    emo = bot.get_guild(708091859129597975)
    list = await emo.fetch_emojis()
    return discord.utils.get(list, name=name)

key = 'RGAPI-dd06df7a-9c28-4cd2-9eb5-b907770a6308'  # api key from the rio database

bot.run(' ') # bot token so that the code can run
