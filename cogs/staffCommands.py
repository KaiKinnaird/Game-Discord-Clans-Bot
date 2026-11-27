import discord, re, demoji, datetime
from discord.ext import commands
from discord.ext.commands import Cog
from utils.miscUtilities import miscUtils
from utils.clanUtilities import clanUtils

class staffCommands(Cog):
    def __init__(self, bot):
        self.bot = bot
        
        self.miscutils = miscUtils(bot)
        self.clanutils = clanUtils(bot)
    
    @commands.command(name="forcedisband", aliases=["fd"])
    async def forcedisband(self, ctx, clantag):
        ## Check if staff
        staffList = await self.miscutils.genStaffList()
        if ctx.author.id in staffList:
            ## Check if the clan exists
            
            isclan, clan = await self.clanutils.isClan(clantag)
            if isclan:
                return await self.clanutils.disbandClan(ctx, clan["tag"])
            else:
                return await ctx.reply(embed = discord.Embed(description = "> Clan has not been found. If this persists please contact higher authority staff.", color = discord.Color.red()))
        else:
            return await ctx.reply(embed = discord.Embed(description = "> You are not permitted to use this command.", color = discord.Color.red()))
    
    
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"Cog {self.__class__.__name__} has been successfully initiated\n------------")

async def setup(bot):
    await bot.add_cog(staffCommands(bot))