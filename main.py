from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import discord
import os

def get_coin(name):
  url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
  parameters = {
    'slug':name,
    'convert':'USD'
  }
  headers = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': '9583d52c-6569-4aaf-8870-9d18b5c0b80e',
  }
  
  session = Session()
  session.headers.update(headers)
  
  try:
    response = session.get(url, params=parameters)
    try:
      data = json.loads(response.text)
      id = list(data["data"])[0]
      price = data["data"][id]["quote"]["USD"]["price"]
      coin_name = data["data"][id]["name"]
      mcap = data["data"][id]["quote"]["USD"]["market_cap"]
      return format(price,".2f"), coin_name, format(mcap, ".2f")
    except:
      return "no such coin"
  except (ConnectionError, Timeout, TooManyRedirects) as e:
    return e


client = discord.Client()

@client.event
async def on_ready():
  print("We have logged in as {0.user}".format(client))

@client.event
async def on_message(message):
  if message.author==client.user:
    return
  coin = message.content[2:]  
  price, name, mcap = get_coin(coin)  
  if message.content.startswith("!p"):
    await message.channel.send(f"{name}'s price is ${price}")
  if message.content.startswith("!m"):
    await message.channel.send(f"{name}'s market cap is ${mcap}")  #market capteki virgülleri kaldır
  if "invest" in message.content:
    await message.channel.send("Be careful when reading someone else's ideas. Make sure you are making your own investment decisions")  
  secret_coin = "dogecoin" #this will be selected randomly
  if secret_coin in message.content:
    await message.channel.send(f"{client.user} found today's coin. it is {secret_coin}")  #

client.run("OTg5MTQ4OTc4NjAxOTQ3MTc2.G92gO6.-jRTLSBNfZGvgtVoFlLZkw-ZfBoQD1r7wq7BWw")


#bazı durumlarda ünlü birinin sözlerini söyle
#bazı davranışlarda bulunursa o kişiyi at
#eğer belli miktarda belli sözü söylediyse veya bir aksiyon aldıysa(beğenme vs) o kişiyi başka bir kanala ekle



#crypto fiyatını discorda kullanıcı olarak gibi sabitleme
#rastgele bir coin hakkında bilgi alma fiyat market cap coin açıklaması vs


#scoreboard yatırım tarzı bir şey olabilir mi değerlendir


#bazı twitter hesaplarından haberleri direk haber kanalına paylaş
#i will have to use tweepy module read the docs 