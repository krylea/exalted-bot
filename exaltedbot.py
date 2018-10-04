import discord
from utils import *

TOKEN = "NDk3NDY3MzA2NTQ1NTEyNDU4.DpfmKQ.cCLmWW5HMba6kGXHhSX6yTD7MyY"

client = discord.Client()
sess = Session()

@client.event
async def on_ready():
    print("The bot is ready!")
    await client.change_presence(game=discord.Game(name="Making a bot"))

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if sess.is_command(message.content):
        command = message.content[2:]
        try:
            output = sess.execute_command(command)
            await client.send_message(message.channel, output)
        except:
            await client.send_message(message.channel, "Error!")

client.run(TOKEN)


