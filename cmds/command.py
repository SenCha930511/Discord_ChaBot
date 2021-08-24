import discord
import asyncio
import json
import datetime
import time
from discord.ext import commands
from core.classes import Cog_Extension


class Command(Cog_Extension):

    @commands.command()
    async def ping(self, ctx):
        t = time.perf_counter()
        message = await ctx.send("Loading...")
        t2 = time.perf_counter()
        await message.edit(content = f"Pong! `{round((t2 - t) * 1000)}` ms")


    @commands.command()
    async def help(self, ctx):
        end = time.time()
        embed = discord.Embed(title="**ChaBot Help**", description="List of Commands & Triggers",
                              color=0xd1b198, timestamp=datetime.datetime.utcfromtimestamp(end))
        embed.set_thumbnail(url="https://i.imgur.com/93EPgLu.png")
        embed.add_field(name="\a", value="\a", inline=False)
        embed.add_field(name="__**【Commads】**__",
                        value="**List of Commands & Description**", inline=False)
        embed.add_field(
            name="**help*", value="`View bot description`", inline=True)
        embed.add_field(name="**status*",
                        value="`View bot status`", inline=True)
        embed.add_field(name="**server*",
                        value="`View server info`", inline=True)
        embed.add_field(name="**invite*",
                        value="`View invitation link`", inline=True)
        embed.add_field(name="**avatar*",
                        value="`View someone's avatar`", inline=True)
        embed.add_field(name="**load*", value="`Load cogs`", inline=True)
        embed.add_field(name="**unload*", value="`Unload cogs`", inline=True)
        embed.add_field(name="**reload*", value="`Reload cogs`", inline=True)
        embed.add_field(name="\a", value="\a", inline=False)
        embed.add_field(name="__**【Triggers】**__",
                        value="**Keyword & Reaction**", inline=False)
        embed.add_field(
            name="*iOS*", value="`iOS因為系統權限設置，無法支援修改器`", inline=False)
        embed.add_field(name="*iPhone*",
                        value="`iOS因為系統權限設置，無法支援修改器`", inline=False)
        embed.add_field(name="*下載*", value="`修改器請至 #📝app更新日誌 下載`", inline=True)
        embed.add_field(name="*載點*", value="`修改器請至 #📝app更新日誌 下載`", inline=True)
        embed.add_field(name="\a", value="\a", inline=False)
        embed.add_field(name="**Developed by SenCha**",
                        value="<@339674731307466754>", inline=False)
        await ctx.send(embed=embed)


    @commands.command()
    async def server(self, ctx):
        try:
            start = int(time.mktime(time.strptime(
                str(ctx.guild.created_at).split('.')[0], "%Y-%m-%d %H:%M:%S")))
            end = time.time()
            second = end - start
            minute = int(second / 60)
            second = round(second - (minute * 60))
            hour = int(minute / 60)
            minute = minute - (hour * 60)
            day = int(hour / 24)
            hour = hour - (day * 24)
            if second < 10:
                second_str = f"0{ second }"
            else:
                second_str = second
            if minute < 10:
                minute_str = f"0{ minute }"
            else:
                minute_str = minute
            if hour < 10:
                hour_str = f"0{ hour }"
            else:
                hour_str = hour
            online = 0
            admin = ""
            ad_count = 0
            for member in ctx.guild.members:
                if str(member.status) != "offline":
                    online = online + 1
            for role in ctx.guild.roles:
                if role.permissions.administrator:
                    admin = f"{ admin }\n { role } "
                    ad_count = ad_count + 1
            embed = discord.Embed(
                color=0xbc25f4, timestamp=datetime.datetime.utcfromtimestamp(end))
            embed.set_author(name=ctx.guild, icon_url=ctx.guild.icon_url)
            embed.add_field(name=":id: Server ID",
                            value=f"`{ ctx.guild.id }`", inline=True)
            embed.add_field(name=":calendar: Created On",
                            value=f"`{ str(ctx.guild.created_at).split('.')[0] }`\n`{ day } day(s), { hour_str }:{ minute_str }:{ second_str } ago`", inline=True)
            embed.add_field(name=":crown: Owned by",
                            value=f"`{ ctx.guild.owner.name }`", inline=True)
            embed.add_field(
                name=f":busts_in_silhouette: Members({ ctx.guild.member_count })", value=f"`{ online } Online`", inline=True)
            embed.add_field(name=f":speech_balloon: Channels({ len(ctx.guild.text_channels) + len(ctx.guild.voice_channels)})",
                            value=f"`{ len(ctx.guild.text_channels) } Text | { len(ctx.guild.voice_channels)} Voice`", inline=True)
            embed.add_field(name=f":earth_africa: Region",
                            value=f"`{ ctx.guild.region }`", inline=True)
            embed.add_field(name=f":closed_lock_with_key: Roles({ len(ctx.guild.roles) })",
                            value=f"`Administrator({ ad_count }): { admin }`", inline=True)
            await ctx.send(embed=embed)
        except Exception as e:
            print(f"【錯誤】<command - server> {e}")


    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def mute(self, ctx, member: discord.Member, reason: str):
        mute_role = discord.utils.get(ctx.guild.roles, name='Muted')
        if mute_role == None:
            perms = discord.Permissions()
            perms.update(send_messages=False, read_messages=True, speak=False, send_tts_messages=False)
            mute_role = await ctx.guild.create_role(name='Muted', Permission=perms)
            await ctx.send('Role created!')
            await member.add_roles(mute_role, reason="Reason: {reason} | Requested by {mod}.".format(reason=reason, mod=ctx.author))
            embed = discord.Embed(color=0xfa144e)
            embed.add_field(name="Mute", value=f"{member} has been muted!")
            await ctx.send(embed=embed)
            try:
                await member.send(f"【{ctx.guild.name}】你已被禁言，原因：{reason}")
            except Exception as e:
                print(f"【錯誤】<command - mute> {e}")
        else:
            await member.add_roles(mute_role, reason="Reason: {reason} | Requested by {mod}.".format(reason=reason, mod=ctx.author))
            embed = discord.Embed(color=0xfa144e)
            embed.add_field(name="Mute", value=f"{member} has been muted!")
            await ctx.send(embed=embed)
            try:
                await member.send(f"【{ctx.guild.name}】你已被禁言，原因：{reason}")
            except Exception as e:
                print(f"【錯誤】<command - mute> {e}")

    
    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def unmute(self, ctx, member: discord.Member):
        mute_role = discord.utils.get(ctx.guild.roles, name='Muted')
        await member.remove_roles(mute_role)
        embed = discord.Embed(color=0x91e873)
        embed.add_field(name="Mute", value=f"{member} has been un-muted!")
        await ctx.send(embed=embed)
        try:
            await member.send(f"【{ctx.guild.name}】你的禁言處罰已解除")
        except Exception as e:
            print(f"【錯誤】<command - unmute> {e}")


    @commands.command()
    async def avatar(self, ctx, member: discord.Member = None):
        if member == None:
            member = ctx.message.author
        await ctx.send(member.avatar_url)


    @commands.command()
    async def invite(self, ctx):
        await ctx.send("ChaBot邀請連結: https://sencha.xyz/discord_bot")
           

def setup(bot):
    bot.add_cog(Command(bot))

