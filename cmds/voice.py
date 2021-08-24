import discord
import asyncio
import youtube_dl
import os
from discord.ext import commands, tasks
from core.classes import Cog_Extension


class Voice(Cog_Extension):

    @commands.command(name = "play", aliases = ["p"])
    async def play(self, ctx, url: str):
        song_there = os.path.isfile("song.mp3")
        try:
            if song_there:
                os.remove("song.mp3")
        except PermissionError:
            await ctx.send("Wait for the current playing music to end or use the 'stop' command")
        message = await ctx.send(f"Loading. `{url}`")
        channel = ctx.message.author.voice.channel
        voice = discord.utils.get(self.bot.voice_clients, guild = ctx.guild)
        if channel != None:
            if voice == None:
                await channel.connect()
                await ctx.send(f"Joined **{channel}**")
                voice = discord.utils.get(self.bot.voice_clients, guild = ctx.guild)
        else:
            await ctx.send("You are NOT in a voice channel")
        
        ydl_opts = {
            "format": "bestaudio/best",
            "quiet": True,
            "no_warnings": True,
            "postprocessors": [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }],
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            await message.edit(content = f"Loading.. `{url}`")
            ydl.download([url])
            await message.edit(content = f"Loading... `{url}`")
        for file in os.listdir("./"):
            if file.endswith(".mp3"):
                await ctx.send(f"開始播放 `{file[:-16]}`")
                os.rename(file, "song.mp3")
        voice.play(discord.FFmpegPCMAudio("song.mp3"))



    @commands.command(name = "join", aliases = ["j"])
    async def join(self, ctx):
        channel = ctx.message.author.voice.channel
        voice = discord.utils.get(self.bot.voice_clients, guild = ctx.guild)
        if channel != None:
            if voice == None:
                await channel.connect()
                await ctx.send(f"Joined **{channel}**")
            else:
                await ctx.send(f"The bot is already in a voice channel")
        else:
            await ctx.send("You are NOT in a voice channel")


    @commands.command(name = "leave", aliases = ["l", "q"])
    async def leave(self, ctx):
        voice = discord.utils.get(self.bot.voice_clients, guild = ctx.guild)
        if voice != None:
            await voice.disconnect()
            await ctx.send(f"Left **{voice.channel}**")
        else:
            await ctx.send("The bot is NOT connected to a voice channel")


    @commands.command(name = "pause", aliases = ["pa"])
    async def pause(self, ctx):
        voice = discord.utils.get(self.bot.voice_clients, guild = ctx.guild)
        if voice.is_playing():
            voice.pause()
        else:
            await ctx.send("Currently no audio is playing")


    @commands.command(name = "resume", aliases = ["r"])
    async def resume(self, ctx):
        voice = discord.utils.get(self.bot.voice_clients, guild = ctx.guild)
        if voice.is_paused():
            voice.resume()
        else:
            await ctx.send("The audio is not pause")

    
    @commands.command(name = "stop", aliases = ["s"])
    async def stop(self, ctx):
        voice = discord.utils.get(self.bot.voice_clients, guild = ctx.guild)
        voice.stop()


    # @tasks.loop(seconds = 30)
    # async def check(self):
    #     voice = discord.utils.get(self.bot.voice_clients, guild = ctx.guild)
    #     member_count = len(voice.members)


def setup(bot):
    bot.add_cog(Voice(bot))
