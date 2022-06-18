# Importing libraries
import discord
import os
import asyncio
import youtube_dl
from dotenv import load_dotenv

load_dotenv()


# Discord bot Initialization
intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)
key = "OTM2NjIwMDk4MjM0NTExMzYy.GLMPAq.iacaYvKaASDYbbGuVCMVpvS3yeogqwjph0IYVY"

voice_clients = {}

yt_dl_opts = {'format': 'bestaudio/best'}
ytdl = youtube_dl.YoutubeDL(yt_dl_opts)

ffmpeg_options = {'options': "-vn"}


# This event happens when the bot gets run
@client.event
async def on_ready():
    print(f"Bot logged in as {client.user}")

@client.event
async def on_member_join(member):
    guild = client.get_guild(405958260739407882) # YOUR INTEGER GUILD ID HERE
    welcome_channel = guild.get_channel(967867726112653382) # YOUR INTEGER CHANNEL ID HERE
    await welcome_channel.send(f'Bienvenue sur le serveur discord {guild.name} {member.mention} !')
    await member.send(f'Nous sommes heureux de vous accueillir sur le serveur Discord {guild.name} {member.name} !')


@client.event
async def serverinfo(ctx):
	server = ctx.guild
	numberOfTextChannels = len(server.text_channels)
	numberOfVoiceChannels = len(server.voice_channels)
	numberOfPerson = server.member_count
	serverName = server.name
	message = f"Le serveur **{serverName}** contient `{numberOfPerson}` membres ! \nCe serveur possède `{numberOfTextChannels}` salons écrit et `{numberOfVoiceChannels}` salon vocaux."
	await ctx.send(message)


# This event happens when a message gets sent
@client.event
async def on_message(msg):
    if msg.content.startswith("<play"):

        try:
            url = msg.content.split()[1]

            voice_client = await msg.author.voice.channel.connect()
            voice_clients[voice_client.guild.id] = voice_client

            loop = asyncio.get_event_loop()
            data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=False))

            song = data['url']
            player = discord.FFmpegPCMAudio(song, **ffmpeg_options, executable="C:\ffmpeg")

        except:
            print("error")

        try:
            url = msg.content.split()[1]

            loop = asyncio.get_event_loop()
            data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=False))

            song = data['url']
            player = discord.FFmpegPCMAudio(song, **ffmpeg_options)

            voice_clients[msg.guild.id].play(player)

        except Exception as err:
            print(err)


    if msg.content.startswith("?pause"):
        try:
            voice_clients[msg.guild.id].pause()
        except Exception as err:
            print(err)

    # This resumes the current song playing if it's been paused
    if msg.content.startswith("?resume"):
        try:
            voice_clients[msg.guild.id].resume()
        except Exception as err:
            print(err)

    # This stops the current playing song
    if msg.content.startswith("?stop"):
        try:
            voice_clients[msg.guild.id].stop()
            await voice_clients[msg.guild.id].disconnect()
        except Exception as err:
            print(err)


client.run(os.getenv("TOKEN"))