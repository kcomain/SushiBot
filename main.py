import discord
from discord.ext import commands
import os
import requests
import json
from threading import Thread
import asyncio
from flask import Flask, render_template, redirect
from discord.utils import get
from geopy.geocoders import Nominatim
import urllib.request
import random
import base64
from datetime import datetime

key=os.getenv('key')

wkey=os.getenv('wkey')

okey=os.getenv('okey')

app = Flask(__name__, static_url_path='/static')

players={}

@app.route('/')
def hello_world():
  return render_template('home.html')

client=discord.Client()

bot = commands.Bot(command_prefix='s?')

bot.remove_command('help')

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name="s?help | Developed by Sushi#4347"))
    print(f'{bot.user.name} has connected to Discord!')

@bot.event
async def on_message(message):
  if message.author == bot.user:
    return
  if message.content.startswith('s?test'):
    await message.channel.send("Youve stumbled upon the test command!")
  await bot.process_commands(message)

@bot.command(pass_context=True)
async def user(ctx, user: discord.User):
  embedColor = random.choice([3800852, 4149685, 10233776, 16635957])
  embed = discord.Embed(title=f"{user.name}'s Stats", color=embedColor)
  embed.set_image(url=str(user.avatar_url))
  embed.add_field(name="Name", value=user.name, inline=False)
  embed.add_field(name="Nickname (if any)", value=user.display_name, inline=False)
  embed.add_field(name="ID", value=user.id, inline=False)
  embed.add_field(name="Tag", value=user.discriminator, inline=False)
  embed.add_field(name="Account Creation", value=user.created_at.strftime('%Y-%m-%d at %H:%M:%S'), inline=False)
  embed.add_field(name="Bot", value=user.bot, inline=False)
  print(user.avatar_url)
  await ctx.send(embed=embed)

@bot.command()
async def fact(ctx):
  json = requests.get('https://uselessfacts.jsph.pl/random.json?language=en')
  json = json.json()
  embedColor = random.choice([3800852, 4149685, 10233776, 16635957])
  embed = discord.Embed(title=f'Random Useless Fact', color=embedColor)
  embed.add_field(name="Fact", value=json["text"], inline=False)
  embed.add_field(name="ID", value=json["id"], inline=False)
  await ctx.send(embed=embed)

@bot.command()
async def cat(ctx):
  json = requests.get('https://api.thecatapi.com/v1/images/search')
  json = json.json()
  await ctx.send(json[0]['url'])

@bot.command()
async def dog(ctx):
  url = "http://random.dog/woof"
  file = urllib.request.urlopen(url)

  for line in file:
    decoded_line = line.decode("utf-8")
    print(decoded_line)
    await ctx.send(f'https://random.dog/{decoded_line}')

@bot.command()
async def b64d(ctx, *, string):
  base64_bytes = string.encode('ascii')
  message_bytes = base64.b64decode(base64_bytes)
  message = message_bytes.decode('ascii')
  await ctx.send(message)

@bot.command()
async def b64e(ctx, *, string):
  message_bytes = string.encode('ascii')
  base64_bytes = base64.b64encode(message_bytes)
  base64_message = base64_bytes.decode('ascii')
  await ctx.send(base64_message)

@bot.command()
async def movie(ctx, *, search):
  moviejson = requests.get(f'http://www.omdbapi.com/?t={search}&apikey={okey}')
  moviejson = moviejson.json()
  embedColor = random.choice([3800852, 4149685, 10233776, 16635957])
  embed = discord.Embed(title=f'{moviejson["Title"]} Stats', color=embedColor)
  embed.set_image(url=moviejson["Poster"])
  embed.add_field(name="Title", value=moviejson["Title"], inline=False)
  embed.add_field(name="Rated", value=moviejson["Rated"], inline=False)
  embed.add_field(name="Release Date", value=moviejson["Released"], inline=False)
  embed.add_field(name="Runtime", value=moviejson["Runtime"], inline=False)
  embed.add_field(name="Genre", value=moviejson["Genre"], inline=False)
  embed.add_field(name="Director(s)", value=moviejson["Director"], inline=False)
  embed.add_field(name="Writer(s)", value=moviejson["Writer"], inline=False)
  embed.add_field(name="Lead Actors", value=moviejson["Actors"], inline=False)
  embed.add_field(name="Plot", value=moviejson["Plot"], inline=False)
  embed.add_field(name="Awards (If Any)", value=moviejson["Awards"], inline=False)
  for i in moviejson["Ratings"]:
    print(i)
    embed.add_field(name=i["Source"], value=i["Value"], inline=False)
  await ctx.send(embed=embed)

@bot.command()
async def mc(ctx, ip):
  print(ip)
  srvapi = requests.get(f'https://mcapi.us/server/status?ip={ip}')
  srvapi=srvapi.json()
  print(srvapi)
  lastOn = datetime.utcfromtimestamp(int(srvapi["last_online"])).strftime('%Y-%m-%d %H:%M:%S')
  embedColor = random.choice([3800852, 4149685, 10233776, 16635957])
  embed = discord.Embed(title=f'{ip} Stats', color=embedColor)
  embed.set_image(url=f"https://mcapi.us/server/image?ip={ip}")
  embed.add_field(name="Online", value=srvapi["online"], inline=False)
  embed.add_field(name="MOTD", value=srvapi["motd"], inline=False)
  embed.add_field(name="Players Online", value=srvapi["players"]["now"], inline=False)
  embed.add_field(name="Player Limit", value=srvapi["players"]["max"], inline=False)
  embed.add_field(name="Version", value=srvapi["server"]["name"], inline=False)
  embed.add_field(name="Last Online", value=lastOn, inline=False)
  await ctx.send(embed=embed)


@bot.command()
async def testctx(ctx):
  await ctx.send('Yeah.')

@bot.command()
async def abc(ctx, arg):
  arg = arg.upper()
  letter = requests.get('https://replphabet.sushipython.repl.co/api')
  letter = letter.json()
  embedColor = random.choice([3800852, 4149685, 10233776, 16635957])
  embed = discord.Embed(title=f'{arg} ReplPhabet', color=embedColor)
  for i in range(0,5):
    try:
      embed.add_field(name=f"{arg} Stands for", value=(letter[arg][i]), inline=False) 
    except:
      pass 
  await ctx.send(embed=embed)

@bot.command()
async def say(ctx, *, arg):
  await ctx.send(arg)

@bot.command()
async def dmself(ctx):
  print(ctx.author)
  await ctx.author.send('Hey!')

@bot.command()
async def meme(ctx):
  response = requests.get("https://meme-api.herokuapp.com/gimme/wholesomememes")
  response = response.json()
  img = (response['url'])
  title = (response['title'])
  sub = (response['subreddit'])
  await ctx.send("> Name: "+title+"\n> Subreddit: r/"+sub+"\n"+img)
    
@bot.command()
async def hypixel(ctx,arg1):
  rsp=requests.get("https://api.slothpixel.me/api/players/"+arg1)
  rsp=rsp.json()
  try:
    rank = rsp['rank']
    rank = rank.replace('_', ' ')
  except:
    rank = 'No Rank'
  hlevel = str(round((rsp['level'])))
  try:
    dc = rsp['links']['DISCORD']
  except:
    dc = 'Unlinked' 
  karma = str(rsp['karma'])
  coins = str(rsp['total_coins'])
  exp = str(rsp['exp'])
  embedColor = random.choice([3800852, 4149685, 10233776, 16635957])
  embed = discord.Embed(title=f'{arg1} Stats', color=embedColor)
  embed.add_field(name="UUID", value=rsp['uuid'], inline=False)
  embed.add_field(name="Rank", value=rank, inline=False)
  embed.add_field(name="Discord", value=dc, inline=False)
  embed.add_field(name="Karma", value=karma, inline=False)
  embed.add_field(name="Total Coins", value=coins, inline=False)
  embed.add_field(name="EXP", value=exp, inline=False)
  embed.add_field(name="Last Game", value=rsp['last_game'], inline=False)  
  await ctx.send(embed=embed)
  
@bot.command()
async def item(ctx, *, arg):
  argn = arg
  arg = arg.upper().replace(" ", "_") # still human readable with minimal effort, neater on one line
  baseLink = "https://api.slothpixel.me/api/skyblock"
  slothItemApi = requests.get(f"{baseLink}/items/").json()
  slothAhApi = requests.get(f"{baseLink}/auctions/"+arg).json() # neater, still obvious though
  colours = {
    "COMMON": 10923183,
    "UNCOMMON": 3800852,
    "RARE": 4149685,
    "EPIC": 10233776,
    "LEGENDARY": 16635957,
    # add one for Mythic rarities too?
  }
  tier = slothItemApi[arg]['tier']
  if tier in colours.keys():
    embedColour = colours[tier]
  else: # as to not break the next section for mythic items
    embedColour = 0
  item, ah = slothItemApi[arg], slothAhApi # more obvious to read in below embed code
  embed = discord.Embed(title=argn, color=embedColor)
  embed.add_field(name="Item ID", value=item['item_id'], inline=False)
  embed.add_field(name="Category", value=item['category'], inline=False)
  embed.add_field(name="Average Price", value=ah['average_price'], inline=False)
  embed.add_field(name="Median Price", value=ah['median_price'], inline=False)
  embed.add_field(name="Price Range", value=f"{ah['min_price']} to {ah['max_price']} in last {ah['sold']}", inline=False)
  await ctx.send(embed=embed)
    
@bot.command()
async def info(ctx):
  embed = discord.Embed(title="BotName", description="SushiBot", color=0x00ff00)
  embed.add_field(name="Author", value="Sushi", inline=False)
  embed.add_field(name="Source Code", value="https://repl.it/@SushiPython/bot", inline=False)
  await ctx.send(embed=embed)

@bot.command()
async def help(ctx):
  embed = discord.Embed(title="Help Page", color=0x00ff00)
  embed.add_field(name="s?help", value="Displays this message", inline=False)
  embed.add_field(name="s?info", value="Basic bot info", inline=False)
  embed.add_field(name="s?movie [movie/show]", value="Displays info about the given movie or show", inline=False)
  embed.add_field(name="s?weather [location]", value="Weather data for that location", inline=False)
  embed.add_field(name="s?user [tag]", value="Discord data for the given user", inline=False)
  embed.add_field(name="s?mc [server ip]", value="Displays info about the given server", inline=False)
  embed.add_field(name="s?bazaar", value="Shows profitable bazaar flips", inline=False)
  embed.add_field(name="s?joke", value="Random dad joke", inline=False)
  embed.add_field(name="s?meme", value="Random reddit meme", inline=False)
  embed.add_field(name="s?hypixel [user]", value="Hypixel data for the user", inline=False)
  embed.add_field(name="s?item [item]", value="Skyblock item data", inline=False)
  embed.add_field(name="s?dog", value="Random dog photo", inline=False)
  embed.add_field(name="s?cat", value="Random cat photo", inline=False)
  embed.add_field(name="s?say [text]", value="Says the text", inline=False)
  await ctx.send(embed=embed)

@bot.command()
async def bazaar(ctx):
  await ctx.send('Getting Data, this may take a bit...')
  base_url = 'https://hypixel-skyblock-bazaar.mat1.repl.co'
  product_list = requests.get(base_url + '/products').json()

  items_sort = {}
  

  for i, product_id in enumerate(product_list):
    r = requests.get(base_url + '/product/' + product_id)
    product_data = r.json()

    current_hour_status = product_data['week_historic'][-1]
    if current_hour_status['sellVolume'] == 0: continue
    if current_hour_status['buyVolume'] == 0: continue
    instant_buy_price = current_hour_status['sellCoins'] / current_hour_status['sellVolume']
    instant_sell_price = current_hour_status['buyCoins'] / current_hour_status['buyVolume'] * .99
    buy_volume = current_hour_status['nowBuyVolume']
    sell_volume = current_hour_status['nowSellVolume']
    margin = instant_buy_price - instant_sell_price

    score = round(int(margin * sell_volume) / 1000000, 2)

    if margin < 100: continue
    if buy_volume < 50000: continue
    if sell_volume < 100000: continue
    if score < 20: continue

    items_sort[product_id] = {
      'margin': int(margin),
      'buy_volume': buy_volume,
      'sell_volume': sell_volume,
      'score': score,
      'instant_sell_price': round(instant_sell_price),
      'instant_buy_price': round(instant_buy_price)
    }

    
    print(str((int(i / len(product_list) * 100))) + '%', end='\r')
  everything = ''
  for product_id in sorted(items_sort, key=lambda product_id: items_sort[product_id]['score']):
    item = items_sort[product_id]
    product_style = product_id.replace('_', ' ')
    everything = (everything + f'\n\n> **{product_style}**')
    everything = (everything + '\nMargin: ' + str(item['margin']))
    everything = (everything + '\nBuy volume: ' + str(item['buy_volume']))
    everything = (everything + '\nSell volume: ' + str(item['sell_volume']))
    everything = (everything + '\nBuy Price: ' + str(item['instant_sell_price']))
    everything = (everything + '\nSell Price: ' + str(item['instant_buy_price']))
    everything = (everything + '\nScore: ' + str(item['score']))
  await ctx.send(everything)

@bot.command()
async def joke(ctx):
  j = requests.get("http://official-joke-api.appspot.com/jokes/random")
  j = j.json()
  embed = discord.Embed(title="Joke", description="Dad Jokes", color=0x00ff00)
  embed.add_field(name="Joke", value=j['setup'], inline=False)
  embed.add_field(name="Punchline", value=j['punchline'], inline=False)
  embed.add_field(name="Joke Number", value=j['id'], inline=False)
  await ctx.send(embed=embed)


@bot.command(pass_context=True, aliases=['j'])
async def join(ctx):
  global voice
  channel = ctx.message.author.voice.channel
  voice = get(bot.voice_clients, guild=ctx.guild)

  if voice and voice.is_connected():
    await voice.move_to(channel)
  else:
    voice = await channel.connect()
  
  await voice.disconnect()
  await ctx.send("Bot has joined the channel.")

  if voice and voice.is_connected():
    await voice.move_to(channel)
  else:
    voice = await channel.connect()
  print(f'The bot joined {channel}\n')

@bot.command(pass_context=True, aliases=['l'])
async def leave(ctx):
  channel = ctx.message.author.voice.channel
  voice = get(bot.voice_clients, guild=ctx.guild)

  if voice and voice.is_connected():
    await voice.disconnect()

@bot.command()
async def weather(ctx,*,arg):
  address = arg
  geolocator = Nominatim(user_agent="SushiBot")
  location = geolocator.geocode(address)
  try:
	  await ctx.send("Location: " + location.address+"\nGathering Data...\n")
  except: 
    await ctx.send("Location not found, try again.")

  wj = requests.get("http://api.openweathermap.org/data/2.5/weather?appid="+wkey+"&lat=" + str(location.latitude) + "&lon=" + str(location.longitude))
  wj = wj.json()
  main=(wj['weather'][int(0)]['main'])
  wd=("\n\nWeather: "+main)
  desc=(wj['weather'][int(0)]['description'])
  wd=(wd+"\nWeather Description: "+desc)
  press=(wj['main']['pressure'])
  wd=(wd+"\nAir Pressure: "+str(press))
  hum=(wj['main']['humidity'])
  wd=(wd+"\nHumidity: "+str(hum))
  ktemp=(wj['main']['temp'])
  ktemp = int(round(ktemp))
  ftemp = 9/5 * (ktemp - 273) + 32
  ftemp = int(round(ftemp))
  ctemp = (ftemp - 32) * 5/9
  ctemp = int(round(ctemp))
  wd=(wd+"\nTemperature (in F): "+str(ftemp))
  wd=(wd+"\nTemperature (in C): "+str(ctemp))
  fktemp=(wj['main']['feels_like'])
  fktemp = int(round(ktemp))
  fftemp = 9/5 * (ktemp - 273) + 32
  fftemp = int(round(ftemp))
  fctemp = (ftemp - 32) * 5/9
  fctemp = int(round(ctemp))
  wd=(wd+"\nFeels Like (in F): "+str(fftemp))
  wd=(wd+"\nFeels Like (in C): "+str(fctemp))
  time=int((wj['timezone'])/3600)
  wd=(wd+"\nTime off of GMT/UTC: "+str(time)+" hours")

  sunriseunix=(wj['sys']['sunrise'])

  rsp = requests.get("https://showcase.linx.twenty57.net:8081/UnixTime/fromunixtimestamp?unixtimestamp=" + str(sunriseunix))
  rsp = rsp.json()

  sunrise=(rsp['Datetime'])
  wd=(wd+"\nSunrise (in GMT/UTC): "+str(sunrise))

  sunsetunix=(wj['sys']['sunset'])

  rsp = requests.get("https://showcase.linx.twenty57.net:8081/UnixTime/fromunixtimestamp?unixtimestamp=" + str(sunsetunix))
  rsp = rsp.json()

  sunset=(rsp['Datetime'])
  wd=(wd+"\nSunset (in GMT/UTC): "+str(sunset))
  vis=(wj['visibility'])
  wd=(wd+"\nVisibility: "+str(vis))
  await ctx.send(wd)

@bot.command()
async def isrepl(ctx):
  guildId = ctx.guild.id
  if guildId==437048931827056642:
    await ctx.send('yeah its repl')
  else:
    await ctx.send('no dumbo its not repl')

@bot.command()
async def serverCount(ctx):
  x = 0
  for i in bot.guilds:
    x += 1
  await ctx.send(x)

'''
@bot.command()
async def word(ctx,arg):
  await ctx.send("Getting Data...")
  wrd=requests.get("https://googledictionaryapi.eu-gb.mybluemix.net/?define="+str(word)).json()
  wd=''
  wd=(wd+"Word: "+wrd[int(0)]['word'])
  wd=(wd+"\nPhonetic: "+wrd[int(0)]['phonetic'])
  wd=(wd+"\nOrigin: "+wrd[int(0)]['origin'])
  pos=''
  def info(pos, wd):
    wd=(wd+"\nDefiniton: "+(wrd[int(0)]['meaning'][str(pos)][int(0)]['definition']))
    wd=(wd+"\nExample: "+(wrd[int(0)]['meaning'][str(pos)][int(0)]['example']))
    wd=(wd+"\nPart of Speech: "+pos+"\n\n")
    r=wd
    return(wd)


  pos = 'noun'
  try:
    info(pos, wd)
    await ctx.send(r)
  except:
    pass
  pos = 'verb'
  try:
    info(pos, wd)
  except:
    pass
  pos='adjective'
  try:
   info(pos, wd)
  except:
    pass
  pos='exclamation'
  try:
    info(pos, wd)
  except:
    pass
  pos='adverb'
  try:
    info(pos, wd)
  except: 
    pass
  pos='article'
  try:
    info(pos, wd)
  except:
    pass
'''


def start_bot():
  app.run(host="0.0.0.0",port="8000")
Thread(None, start_bot).start()
bot.run(key)



