from replit import db
from server import keep_running
import discord
import random
import requests
import json
import os

client = discord.Client()

sad_words = ["i suck", "sad", "depression", "depressed"]

def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + " -" + json_data[0]['a']
  return quote

def update_positive(new_positive):
  if "positive_words" in db.keys():
    positive_words = db["positive_words"]
    positive_words.append(new_positive)
    db["positive_words"] = positive_words
  else:
    db["positive_words"] = [new_positive]

def delete_positive(index):
  positive_words = db["positive_words"]
  if len(positive_words) > index:
    del positive_words[index]
    db["positive_words"] = positive_words

@client.event
async def on_ready():
  print("Logged in as {0.user}".format(client))

@client.event
async def on_message(message):
  if message.author == client.user:
    return

  if message.content.startswith('!quote'):
    quote = get_quote()
    await message.channel.send(quote)
    print("Quote sent: " + quote)
  
  options = []
  options = options + db["positive_words"]

  if any(word in message.content for word in sad_words):
    positive_message = random.choice(options)
    await message.channel.send(positive_message)
    print("postitve message sent: " + positive_message)

  if message.content.startswith("!new"):
    new_positive = message.content.split("!new ", 1)[1]
    update_positive(new_positive)
    await message.channel.send("New positive word added")
    print("New positive message added: " + new_positive)

  if message.content.startswith("!delete"):
    positive_words = []
    if "positive_words" in db.keys():
      index = int(message.content.split("!delete",1)[1])
      delete_positive(index)
      positive_words = db["positive_words"]
      await message.channel.send("deleted index: " + str(index))
      print("Word " + str(index) + " Was deleted")

  if message.content.startswith("!list"):
    if "positive_words" in db.keys():
      show_list = db["positive_words"]
      if len(show_list) < 1:
        await message.channel.send("No words found.")
        print("No words found to list")
      words = ""
      for show_str in show_list:
        words = words + show_str + ", "
      await message.channel.send(words)
      print("positve words were listed: " + words)

  if message.content.startswith("!commands"):
    print("Showed all commands")
    await message.channel.send(
      "!list : list all positive messages\n!delete (index) : delete an message from positive words\n!new (message) : creates a new positive message\n!commands : show this menu"
    )

keep_running()
client.run(os.getenv('TOKEN'))