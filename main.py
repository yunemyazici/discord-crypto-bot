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
    'X-CMC_PRO_API_KEY': 'YOUR KEY FROM DISCORD',
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
    await message.channel.send(f"{name}'s market cap is ${mcap}")
  if "invest" in message.content:
    await message.channel.send("Be careful when reading someone else's ideas. Make sure you are making your own investment decisions")

client.run("YOUR DISCORD KEY")
