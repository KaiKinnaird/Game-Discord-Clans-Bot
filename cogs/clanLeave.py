import discord
from discord.ext import commands
from discord.ext.commands import Cog
from utils.miscUtilities import miscUtils
from utils.clanUtilities import clanUtils


class ClanLeave(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.miscutils = miscUtils(bot)
        self.clanutils = clanUtils(bot)
        
    
    @commands.command(name="clanleave", aliases=[])
    async def clanleave(self, ctx):
        ## Check they are in a clan
        
        isInClan, clan = await self.clanutils.isInClan(ctx.author.id)
        if not isInClan:
            return await ctx.reply(embed = discord.Embed(description = "> You are not in a clan", color = discord.Color.red()))
        
        if clan["leader_id"] == ctx.author.id:
            return await ctx.reply(embed = discord.Embed(description = "> You cannot leave a clan you are the leader of", color = discord.Color.red()))
        
        ## Leave the clan
        
        await self.clanutils.removeMember(ctx, clan, ctx.author)

        
    
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"Cog {self.__class__.__name__} has been successfully initiated\n------------")

async def setup(bot):
    await bot.add_cog(ClanLeave(bot))
        
        