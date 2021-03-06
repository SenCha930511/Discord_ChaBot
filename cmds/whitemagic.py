import discord
import asyncio
import json
import datetime
import time
from discord.ext import commands
from core.classes import Cog_Extension


class WhiteMagic(Cog_Extension):

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, data):
        if str(data.emoji) == "π΅" and data.message_id == 787131367930593320:
            guild = self.bot.get_guild(data.guild_id)
            role = guild.get_role(839127265198997594)
            await data.member.add_roles(role)
            try:
                await data.member.send(f"γη½ι­ζ³ει‘θ¨θ«εγ δ½ ε ε₯δΊγ{ role }γθΊ«εη΅")
            except Exception as e:
                print(f"γι―θͺ€γ<whitemagic - on_raw_reaction_remove> {e}")


    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, data):
        await self.bot.wait_until_ready()
        if str(data.emoji) == "π΅" and data.message_id == 787131367930593320:
            guild = self.bot.get_guild(data.guild_id)
            user = guild.get_member(data.user_id)
            role = guild.get_role(839127265198997594)
            await user.remove_roles(role)
            try:
                await user.send(f"γη½ι­ζ³ει‘θ¨θ«εγ δ½ η§»ι€δΊγ{ role }γθΊ«εη΅")
            except Exception as e:
                print(f"γι―θͺ€γ<whitemagic - on_raw_reaction_remove> {e}")


def setup(bot):
    bot.add_cog(WhiteMagic(bot))

