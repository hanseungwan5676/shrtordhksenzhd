import discord
from discord.ext import commands
import youtube_dl
import asyncio
import os
import googleapiclient.discovery

# Discord Bot 토큰과 YouTube API 키
DISCORD_TOKEN = ''
YOUTUBE_API_KEY = ''

# 봇 및 YouTube API 초기화
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)
youtube = googleapiclient.discovery.build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)

playlist = []

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

@bot.command(name='play', help='Plays a song from YouTube')
async def play(ctx, *, search):
    if not ctx.voice_client:
        if ctx.author.voice:
            await ctx.author.voice.channel.connect()
        else:
            await ctx.send("You are not connected to a voice channel.")
            return

    video = youtube_search(search)
    if video:
        url = f"https://www.youtube.com/watch?v={video['id']}"
        playlist.append({'title': video['title'], 'url': url})
        await ctx.send(f"{video['title']} added to the playlist.")
        if not ctx.voice_client.is_playing():
            await download_and_play(ctx)
    else:
        await ctx.send("No video found.")

async def download_and_play(ctx):
    song = playlist.pop(0)
    url = song['url']
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': 'song.mp3',
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    ctx.voice_client.play(discord.FFmpegPCMAudio('song.mp3'), after=lambda e: asyncio.run_coroutine_threadsafe(download_and_play(ctx), bot.loop))

def youtube_search(search_query):
    request = youtube.search().list(
        part="snippet",
        q=search_query,
        type="video",
        maxResults=1
    )
    response = request.execute()

    for item in response.get('items', []):
        if item['id']['kind'] == "youtube#video":
            return {'title': item['snippet']['title'], 'id': item['id']['videoId']}
    return None

bot.run(DISCORD_TOKEN)


