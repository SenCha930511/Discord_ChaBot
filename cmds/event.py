import discord
import asyncio
import json
import datetime
import time
from discord.ext import commands
from core.classes import Cog_Extension


class Event(Cog_Extension):

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = member.guild.system_channel
        await channel.send(f"════════════════════\n👏 熱烈歡迎 { member.mention } :fire:\n:high_brightness: 來到  __**{ member.guild }**__  !\n:zap: 目前成員數 ➤ __**{ member.guild.member_count }**__\n════════════════════\n{ member.avatar_url }\n════════════════════")
        if member.guild.id == 629610708559986689:
            count_channel = self.bot.get_channel(870177698037772288)
            await count_channel.edit(name = f"🌟群組人數：{member.guild.member_count}")
            await member.add_roles(member.guild.get_role(630040833307050019))

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        if member.guild.id == 629610708559986689:
            count_channel = self.bot.get_channel(870177698037772288)
            await count_channel.edit(name = f"🌟群組人數：{member.guild.member_count}")

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, data):
        try:
            if str(data.emoji) == "<:tester:764174607762325534>" and data.message_id == 764177495921786910:
                guild = self.bot.get_guild(data.guild_id)
                role = guild.get_role(764000988017065984)
                await data.member.add_roles(role)
                await data.member.send(f"【 煎茶院 🍵 】 你加入了「{ role }」身分組")
            elif str(data.emoji) == "<:ghost_1:764173464755765278>" and data.message_id == 764177495921786910:
                guild = self.bot.get_guild(data.guild_id)
                role = guild.get_role(631422596251910144)
                await data.member.add_roles(role)
                await data.member.send(f"【 煎茶院 🍵 】 你加入了「{ role }」身分組")
        except Exception as e:
            print(f"【錯誤】<event - on_raw_reaction_add> {e}")


    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, data):
        await self.bot.wait_until_ready()
        try:
            if str(data.emoji) == "<:tester:764174607762325534>" and data.message_id == 764177495921786910:
                guild = self.bot.get_guild(data.guild_id)
                user = guild.get_member(data.user_id)
                role = guild.get_role(764000988017065984)
                await user.remove_roles(role)
                await user.send(f"【 煎茶院 🍵 】 你移除了「{ role }」身分組")
            elif str(data.emoji) == "<:ghost_1:764173464755765278>" and data.message_id == 764177495921786910:
                guild = self.bot.get_guild(data.guild_id)
                user = guild.get_member(data.user_id)
                role = guild.get_role(631422596251910144)
                await user.remove_roles(role)
                await user.send(f"【 煎茶院 🍵 】 你移除了「{ role }」身分組")
        except Exception as e:
            print(f"【錯誤】<event - on_raw_reaction_remove> {e}")


    @commands.Cog.listener()
    async def on_message(self, msg):
        try:
            if not msg.author.bot and not msg.author.guild_permissions.administrator:
                if "IOS" in msg.content.upper() or "IPHONE" in msg.content.upper() or "蘋果" in msg.content.upper() and msg.author != self.bot.user:
                    await msg.channel.send(f"【{ msg.author.mention }】iOS因為系統權限設置，**無法支援修改器**")
                if "安卓" in msg.content.upper() and "11" in msg.content.upper() or "Android" in msg.content.upper() and "11" in msg.content.upper() and msg.author != self.bot.user:
                    await msg.channel.send(f"【{ msg.author.mention }】Android 11因為系統權限設置，**無法支援修改器**")
                if "@everyone" in msg.content and "leaving CS:GO" in msg.content or "@everyone" in msg.content and "check this lol" in msg.content and msg.author != self.bot.user:
                    await msg.delete()
                if msg.guild.id == 629610708559986689:
                    if "載點" in msg.content.upper() or "下載" in msg.content.upper() and msg.author != self.bot.user:
                        await msg.channel.send(f"【{ msg.author.mention }】修改器請至 <#761196601175572490> 下載")
                if msg.guild.id != 786885689073074197:
                    if "魔法牆" in msg.content.upper() or "灰魔法" in msg.content.upper() or "WALL" in msg.content.upper() and msg.author != self.bot.user:
                        await msg.delete()
        except Exception as e:
            print(f"【錯誤】<event - on_message> {e}")


    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        try:
            if after.guild.id != 786885689073074197:
                if "魔法牆" in after.content.upper() or "灰魔法" in after.content.upper() or "WALL" in after.content.upper():
                    await after.delete()
        except Exception as e:
            print(f"【錯誤】<event - on_message_edit> {e}")


def setup(bot):
    bot.add_cog(Event(bot))
