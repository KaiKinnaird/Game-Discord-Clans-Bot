import discord
from discord.ext import commands
from discord.ext.commands import Cog
from utils.miscUtilities import miscUtils
from utils.clanUtilities import clanUtils


class ClanRemove(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.miscutils = miscUtils(bot)
        self.clanutils = clanUtils(bot)
        
    
    @commands.command(name="clanremove", aliases=["clankick", "ck", "cr"])
    async def clanremove(self, ctx, member: discord.Member):
        # Check if user is in a clan
        isInClan, clan = await self.clanutils.isInClan(ctx.author.id)
        
        if not isInClan:
            return await ctx.reply(embed = discord.Embed(description = "> You are not the leader/co-leader of a clan", color = 0xE74C3C))
        
        isAuth, clan = await self.clanutils.isAuthorised(ctx.author.id, clan["_id"])
        
        if not isAuth:
            return await ctx.reply(embed = discord.Embed(description = f"> You are not the leader/co-leader of your clan `{clan['_id']}`", color = 0xE74C3C))
        
        isUserInClan, theirclan = await self.clanutils.isInClan(member.id)
        if not isUserInClan or theirclan["_id"] != clan["_id"]:
            return await ctx.reply(embed = discord.Embed(description = f"> {member.mention} is not in your clan", color = 0xE74C3C))
        
        await self.clanutils.removeMember(ctx, clan, member)
        
    
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"Cog {self.__class__.__name__} has been successfully initiated\n------------")

async def setup(bot):
    await bot.add_cog(ClanRemove(bot))
        
        