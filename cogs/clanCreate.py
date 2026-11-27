import discord, re, demoji
from discord.ext import commands
from discord.ext.commands import Cog
from utils.miscUtilities import miscUtils
from utils.clanUtilities import clanUtils

class clanCreate(Cog):
    def __init__(self, bot):
        self.bot = bot
        
        self.miscutils = miscUtils(bot)
        self.clanutils = clanUtils(bot)
    
    @commands.command(name="clancreate", aliases=["cc"])
    async def clancreate(self, ctx, clantag):
        ## Check for emojis
        emoji = demoji.findall(clantag)
        if emoji:
            return await ctx.reply(embed = discord.Embed(description = "> You cannot have emojis in your clan tag", color = 0xE74C3C))
        
        ## Check for special characters
        if re.search("[^a-zA-Z0-9]", clantag):
            return await ctx.reply(embed = discord.Embed(description = "> You cannot have special characters in your clan tag", color = 0xE74C3C))
        

        ## Check if user is in a clan
        isinclan, _ = await self.clanutils.isInClan(ctx.author.id)
        if isinclan == True:
            return await ctx.reply(embed = discord.Embed(description = "> You are already in a clan", color = 0xE74C3C))
        
        ## Check if clan already exists
        
        isclan, _ = await self.clanutils.isClan(clantag)
        
        if isclan:
            return await ctx.reply(embed = discord.Embed(description = "> Clan already exists", color = 0xE74C3C))
        
        
        ## Validated clantag and good to go
        
        await self.clanutils.createClan(ctx, clantag, ctx.author)
        
        
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"Cog {self.__class__.__name__} has been successfully initiated\n------------")

async def setup(bot):
    await bot.add_cog(clanCreate(bot))
        
        