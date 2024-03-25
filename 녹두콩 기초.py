import discord
from dico_token import Token
import youtube_dl
from discord import voice_client
from discord import FFmpegPCMAudio

client = discord.Client()


@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(name='Music Playing'))
    print("접속")
@client.event
async def on_message(message):
    if message.content == "/in":
        await message.author.voice.channel.connect()
    if message.content == "/out":
        await message.guild.voice_client.disconnect()
    if message.content.startswith("/test"):
        music_name = message.content.split("test ")[1]
    YDL_OPTIONS = {'format':'bestaudio','noplaylist':'True','outtmpl':f"test/{music_name}.mp3"}
    with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
        info = ydl.extract_info(music_name, download=False)
        URL = info['format'][0]['url']
    FFMPEG_OPTIONS = {'before_options':'-reconnect 1 -reconnect_streamed 1'}
    try:
        voice = await message.author.voice.channel.connect()
    except:
        voice = None
        await message.guild.voice_client.disconnect()
    if not voice or not voice.is_playing():
        await message.channel.send(embed=discord.Embed(title=f"🎵{music_name}", description="Playing",color=0xB66FF))
        