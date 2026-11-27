import discord, re, demoji
from discord.ext import commands
from discord.ext.commands import Cog
from utils.miscUtilities import miscUtils
from utils.clanUtilities import clanUtils

class clanDisband(Cog):
    def __init__(self, bot):
        self.bot = bot
        
        self.miscutils = miscUtils(bot)
        self.clanutils = clanUtils(bot)
    
    @commands.command(name="clandisband", aliases=["cd"])
    async def clandisband(self, ctx):
        ## Check if user is in a clan
        isInClan, clan = await self.clanutils.isInClan(ctx.author.id)
        
        if not isInClan:
            return await ctx.reply(embed = discord.Embed(description = "> You are not the leader of a clan", color = 0xE74C3C))
        
        if clan["leader_id"] != ctx.author.id:
            return await ctx.reply(embed = discord.Embed(description = "> You are not the leader of a clan", color = 0xE74C3C))
        
        
        ## Validated and good to go
        
        if isInClan and clan["leader_id"] == ctx.author.id:
            ## Send confirmation message
            await ctx.reply(embed = discord.Embed(description = "> Are you sure you want to disband your clan?", color = 0xE74C3C), view = confirmDisband(self.bot, clan, ctx.author))
        else:
            return await ctx.reply(embed = discord.Embed(description = "> You are not the leader of a clan", color = 0xE74C3C))
        
    
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"Cog {self.__class__.__name__} has been successfully initiated\n------------")

async def setup(bot):
    await bot.add_cog(clanDisband(bot))
        



class confirmDisband(discord.ui.View):
    def __init__(self, bot, clan, originaluser):
        super().__init__()
        self.clan = clan
        self.originaluser = originaluser
        self.clanutils = clanUtils(bot)
    
    @discord.ui.button(label = "Confirm", style = discord.ButtonStyle.green, custom_id = "confirmdisband")
    async def confirmDisband(self, interaction: discord.Interaction, button: discord.Button):
        ## Check if the user is the original author
        
        if interaction.user.id != self.originaluser.id:
            return await interaction.message.edit(embed = discord.Embed(description = "> Only the original author can confirm this action", color = 0xE74C3C))
        
        return await self.clanutils.disbandClan(interaction, self.clan["tag"])

    @discord.ui.button(label = "Cancel", style = discord.ButtonStyle.red, custom_id = "canceldisband")
    async def cancelDisband(self, interaction: discord.Interaction, button: discord.Button):
        ## Check if the user is the original author
        
        if interaction.user.id != self.originaluser.id:
            return await interaction.message.edit(embed = discord.Embed(description = "> Only the original author can confirm this action", color = 0xE74C3C))
        
        await interaction.message.edit(embed = discord.Embed(description = "> Disband cancelled", color = 0xE74C3C))
        ## disable view
        self.stop()
        
        await interaction.message.edit(embed = discord.Embed(description = "> Disband cancelled", color = 0xE74C3C), view=self)
        return 



