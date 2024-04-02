import discord
from dico_token import Token
import youtube_dl
from discord import voice_client
from discord import FFmpegPCMAudio
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.service import Service



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
        
    if message.content == "(out":
        await message.guild.voice_client.disconnect()
    if message.content.startswith("(test"):
        music_name = message.content.split("test ")[1]  
        
        driver_path =r"C:\Users\hsehe\Desktop\한승완 동아리 지울거면 좀 물어보고 지워라 제발\chromedriver-win64\chromedriver-win64\chromedriver.exe"  # WebDriver의 경로 설정
        service = Service(executable_path=driver_path)
        options = webdriver.ChromeOptions()
        driver = webdriver.Chrome(service=service, options=options)
        driver.get(f"https://www.youtube.com/results?search_query={music_name}")
        page_data = driver.page_source
        parsing_data = BeautifulSoup(page_data, 'lxml')
        music_title = parsing_data.find_all('a', {'id': 'video-title'})
        driver.close()
        
        music_selection = discord.Embed(title=f"Music Selection", description=f"Select track with (play 1~5", color=0x35B62C)
        music_selection.add_field(name=f"1️⃣ : {music_title[0].text.strip()}", value='(play 1', inline=False)
        music_selection.add_field(name=f"2️⃣ : {music_title[1].text.strip()}", value='(play 2', inline=False)
        music_selection.add_field(name=f"3️⃣ : {music_title[2].text.strip()}", value='(play 3', inline=False)
        music_selection.add_field(name=f"4️⃣ : {music_title[3].text.strip()}", value='(play 4', inline=False)
        music_selection.add_field(name=f"5️⃣ : {music_title[4].text.strip()}", value='(play 5', inline=False)
        music_station = await message.channel.send(embed=music_selection)
        
        def check(m):
            return m.content in ['(play 1','(play 2','(play 3','(play 4','(play 5',"(done"] and m.channel == music_station.channel
        m_data = await client.wait_for("message", check=check)
        
        
        if m_data.content == '(done)':
            raise ValueError
        else:
            select_num = int(m_data.content.split(' ')[1]) -1
            
        musicurl = music_title[select_num].get('href')
        url = f'https://www.youtube.com{musicurl}'
        
        YDL_OPTIONS = {'format':'bestaudio','noplaylist':'True','outtmpl':f"test/{music_name}.mp3"}
        with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(url, download=False)
            URL = info['url']
        FFMPEG_OPTIONS = {'before_options':'-reconnect 1 -reconnect_streamed 1'}
        try:
            voice = await message.author.voice.channel.connect()
        except:
            voice = None
            await message.guild.voice_client.disconnect()
        if not voice or not voice.is_playing():
            await message.channel.send(embed=discord.Embed(title=f"🎵{music_title[select_num].text.strip()}", description="Playing",color=0xB66FF))
        
            if not voice:
                voice = await message.author.voice.channel.connect()
            voice.play(discord.FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
    
        elif voice.is_playing ():
            await message.channel.send(embed=discord.Embed(title=f"😮NOW",description="Other music playing",color=0xFF9922))

client.run(Token)