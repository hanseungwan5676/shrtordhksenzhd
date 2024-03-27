import discord
from dico_token import Token
from discord import voice_client

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(name='Music Playing'))
    print("접속")
    
    
@client.event
async def on_message(message):
    if message.content == "(in":
        await message.author.voice.channel.connect()
        
client.run(Token)