import discord
from utils import *

TOKEN = "NDk3NDY3MzA2NTQ1NTEyNDU4.DpfmKQ.cCLmWW5HMba6kGXHhSX6yTD7MyY"

client = discord.Client()
sess = Session()



@client.event
async def on_ready():
    print("The bot is ready!")
    await client.change_presence(game=discord.Game(name="Ready!"))

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
            raise

@client.event
async def on_error(event, *args, **kwargs):
    if event.__class__ == KeyboardInterrupt:
        await client.change_presence(game=discord.Game(name="Asleep..."), afk=True)
        await client.logout()
        raise event

def run_bot(token):
    client.login(token)


client.run(TOKEN)


