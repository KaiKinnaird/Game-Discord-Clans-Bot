import discord
from discord.ext import commands
from discord.ext.commands import Cog
from utils.miscUtilities import miscUtils
from utils.clanUtilities import clanUtils


class PromoteDemote(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.miscutils = miscUtils(bot)
        self.clanutils = clanUtils(bot)
    
    @commands.command(name="clanpromote", aliases=["promote"])
    async def clanpromote(self, ctx, member: discord.Member):
        isInClan, clan = await self.clanutils.isInClan(ctx.author.id)
        
        if not isInClan:
            return await ctx.reply(embed = discord.Embed(description = "> You are not in a clan", color = discord.Color.red()))
        
        auth, clan = await self.clanutils.isAuthorised(ctx.author.id, clan["tag"])
        
        if not auth:
            return await ctx.reply(embed = discord.Embed(description = "> You are not the leader of this clan", color = discord.Color.red()))
        
        if ctx.author.id != clan["leader_id"]:
            return await ctx.reply(embed = discord.Embed(description = "> You are not the leader of this clan", color = discord.Color.red()))
        elif ctx.author.id == clan["leader_id"]:
            if member.id == clan["leader_id"]:
                return await ctx.reply(embed = discord.Embed(description = "You cannot promote yourself", color = discord.Color.red()))
            elif member.id in clan["co_leaders"]:
                return await ctx.reply(embed = discord.Embed(description = "You cannot promote a co-leader", color = discord.Color.red()))
            
            isInClan, membersclan = await self.clanutils.isInClan(member.id)
            if membersclan['_id'] != clan['_id']:
                return await ctx.reply(embed = discord.Embed(description = "This member is not in your clan", color = discord.Color.red()))
            
            ## Give them co-leader role
            
            guild = self.bot.get_guild(self.bot.config["Guild ID"])
            role = guild.get_role(self.bot.config["Roles"]["Co-Leader Role"])
            
            await member.add_roles(role)
            
            clan["co_leaders"].append(member.id)
            self.bot.clandb.update_one({"_id": clan["_id"]}, {"$set": {"co_leaders": clan["co_leaders"]}})
            
            return await ctx.reply(embed = discord.Embed(description = f"> {member.mention} has been promoted to co-leader", color = discord.Color.green()))
            
        else:
            return await ctx.reply(embed = discord.Embed(description = "> You are not the leader of a clan", color = 0xE74C3C))

    @commands.command(label = "clandemote", aliases = ["demote"])
    async def clandemote(self, ctx, member: discord.Member):
        isInClan, clan = await self.clanutils.isInClan(ctx.author.id)
        
        if not isInClan:
            return await ctx.reply(embed = discord.Embed(description = "> You are not in a clan", color = discord.Color.red()))
        
        auth, clan = await self.clanutils.isAuthorised(ctx.author.id, clan["tag"])
        
        if not auth:
            return await ctx.reply(embed = discord.Embed(description = "> You are not the leader of this clan", color = discord.Color.red()))
        
        if ctx.author.id != clan["leader_id"]:
            return await ctx.reply(embed = discord.Embed(description = "> You are not the leader of this clan", color = discord.Color.red()))
        elif ctx.author.id == clan["leader_id"]:
            if member.id == clan["leader_id"]:
                return await ctx.reply(embed = discord.Embed(description = "You cannot demote yourself"), color = discord.Color.red())
            elif member.id in clan["members"] and not member.id in clan["co_leaders"]:
                return await ctx.reply(embed = discord.Embed(description = "You cannot demote a member"), color = discord.Color.red())
            
            isInClan, membersclan = await self.clanutils.isInClan(member.id)
            if membersclan['_id'] != clan['_id']:
                return await ctx.reply(embed = discord.Embed(description = "This member is not in your clan"), color = discord.Color.red())
            
            ## Give them co-leader role
            
            guild = self.bot.get_guild(self.bot.config["Guild ID"])
            role = guild.get_role(self.bot.config["Roles"]["Co-Leader Role"])
            
            await member.remove_roles(role)
            
            clan["co_leaders"].remove(member.id)
            self.bot.clandb.update_one({"_id": clan["_id"]}, {"$set": {"co_leaders": clan["co_leaders"]}})
            
            return await ctx.reply(embed = discord.Embed(description = f"> {member.mention} has been demoted to member", color = discord.Color.green()))
            
        else:
            return await ctx.reply(embed = discord.Embed(description = "> You are not the leader of a clan", color = 0xE74C3C))
    
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"Cog {self.__class__.__name__} has been successfully initiated\n------------")

async def setup(bot):
    await bot.add_cog(PromoteDemote(bot))
        
        