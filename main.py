# This example requires the 'message_content' privileged intents

import os
import discord
from discord.ext import commands
import pytube
import asyncio


intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content.startswith('$play'):
        url = message.content.split(' ')[1]

        # Si el usuario no está conectado a ningún canal de voz
        if not message.author.voice:
            return await message.channel.send('Debes unirte a un canal de voz primero')

        voice_channel = message.author.voice.channel

        # Si el bot ya está conectado a un canal de voz
        if message.guild.voice_client:
            await message.guild.voice_client.move_to(voice_channel)
        else:
            await voice_channel.connect()

        video = pytube.YouTube(url)
        audio = video.streams.filter(only_audio=True).first()
        audio.download(output_path='./', filename=video.video_id)

        source = discord.FFmpegPCMAudio(f"./{video.video_id}.mp4")
        message.guild.voice_client.play(source)

        while message.guild.voice_client.is_playing():
            await asyncio.sleep(1)

        await message.guild.voice_client.disconnect()
        os.remove(f"./{video.video_id}.mp4")

@bot.command()
async def ping(ctx):
    await ctx.send('pong')

@bot.command()
async def hello(ctx):
    await ctx.send("Choo choo! 🚅")


bot.run(os.environ["DISCORD_TOKEN"])
