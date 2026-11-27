import discord
from discord.ext import commands
from discord.ext.commands import Cog
from utils.miscUtilities import miscUtils


class Help(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.miscutils = miscUtils(bot)
    
    @commands.command(name="help", aliases=["clanhelp"])
    async def help(self, ctx):
        stafflist = await self.miscutils.genStaffList()
        prefix = self.bot.config["Bot Prefix"]
        
        if ctx.author.id in stafflist:
            embed = discord.Embed(title = "Clan Bot Help", description = f"""
**General Commands**
- `{prefix}help` - See this message
- `{prefix}clancreate` `tag` - Create a clan
- `{prefix}aliases` - See the aliases of all commands

**Clan Leader Commands**
- `{prefix}clandisband` - Disband your clan if you currently have one
- `{prefix}claninvite` `@member` - Invite a member to your clan
- `{prefix}clanremove` `@member` - Remove a member from your clan
- `{prefix}clanpromote` `@member` - Promotes a member in your clan to a Co-leader
- `{prefix}clandemote` `@member` - Demoted a Co-leader back to being a member
- `{prefix}changeleader` `@member` - Transfers the ownership of your clan to a different member
- `{prefix}changename` `newname` - Change your clan name

**Clan info Commands**
- `{prefix}claninfo` `tag` - See some information about a clan. Note: If you don't supply a tag, then your current clan will be displayed
- `{prefix}clansetdiscord` `discord.gg/discordlink`
- `{prefix}clansetyoutube` `youtube.com/videoorchannel`
- `{prefix}clansetlogo` `imgur.com/yourclanlogo`
- `{prefix}clansetbanner` `imgur.com/yourclanbanner`
- `{prefix}clansetcolor` `#ffffff`

**Staff Commands**
- `{prefix}forcedisband` `tag` - Force a clan to disband
- `{prefix}forceinvite` `tag` `@member` - Force invite a member to a clan
- `{prefix}forceremove` `tag `@member` - Force remove a member from a clan
- `{prefix}forcetransfer` `tag` `@newleader` - Force transfer a clan to another user
- `{prefix}addroamwin` `tag` - Add a roams win to a clan
- `{prefix}addkothwin` `tag` - Add a KOTH win to a clan
- `{prefix}addmazewin` `tag` - Add a maze win to a clan
- `{prefix}removeroamwin` `tag` - Remove a roams win from a clan
- `{prefix}removekothwin` `tag` - Remove a KOTH win from a clan
- `{prefix}removemazewin` `tag` - Remove a maze win from a clan
""", color = self.bot.embedColour)
            return await ctx.reply(embed = embed)
        
        
        embed = discord.Embed(title = "Clan Bot Help", description = f"""
**General Commands**
- `{prefix}help` - See this message
- `{prefix}clancreate` `tag` - Create a clan
- `{prefix}aliases` - See the aliases of all commands

**Clan Leader Commands**
- `{prefix}clandisband` - Disband your clan if you currently have one
- `{prefix}claninvite` `@member` - Invite a member to your clan
- `{prefix}clanremove` `@member` - Remove a member from your clan
- `{prefix}clanpromote` `@member` - Promotes a member in your clan to a Co-leader
- `{prefix}clandemote` `@member` - Demoted a Co-leader back to being a member
- `{prefix}changeleader` `@member` - Transfers the ownership of your clan to a different member

**Clan info Commands**
- `{prefix}claninfo` `tag` - See some information about a clan. Note: If you don't supply a tag, then your current clan will be displayed
- `{prefix}clansetdiscord` `discord.gg/discordlink`
- `{prefix}clansetyoutube` `youtube.com/videoorchannel`
- `{prefix}clansetlogo` `imgur.com/yourclanlogo`
- `{prefix}clansetbanner` `imgur.com/yourclanbanner`
- `{prefix}clansetcolor` `#ffffff`
""", color = self.bot.embedColour)
        return await ctx.reply(embed = embed)
    
    @commands.command(label = "aliases")
    async def aliases(self, ctx):
        prefix = self.bot.config["Bot Prefix"]
        stafflist = await self.miscutils.genStaffList()
        
        if ctx.author.id in stafflist:
            embed = discord.Embed(title = "Clan Bot Aliases", description = f"""
**General Commands**
- `{prefix}help` - `clanhelp`
- `{prefix}clancreate` - `cc` and `cinfo`

**Clan Leader Commands**
- `{prefix}clandisband` - `cd`
- `{prefix}claninvite` - `ci`
- `{prefix}clanremove` - `cr`
- `{prefix}clanpromote` - `promote`
- `{prefix}clandemote` - `demote`
- `{prefix}changeleader` - `cl`

**Clan info Commands**
- `{prefix}claninfo` - `info`
- `{prefix}clansetdiscord` - `csd`
- `{prefix}clansetyoutube` - `csy`
- `{prefix}clansetlogo` - `csl`
- `{prefix}clansetbanner` - `csb`
- `{prefix}clansetcolor` - `csc`

**Staff Commands**
- `{prefix}forcedisband` - `fd`
- `{prefix}forceinvite` - `fi`
- `{prefix}forceremove` - `fr`
- `{prefix}forcetransfer` - `ft`
- `{prefix}addroam` - `ar`
- `{prefix}addkoth` - `ak`
- `{prefix}addmaze` - `am`
- `{prefix}removeroam` - `rr`
- `{prefix}removekoth` - `rk`
- `{prefix}removemaze` - `rm`

    """, color = self.bot.embedColour)
            
            return await ctx.reply(embed = embed)
        
        
        embed = discord.Embed(title = "Clan Bot Aliases", description = f"""
**General Commands**
- `{prefix}help` - `clanhelp`
- `{prefix}clancreate` - `cc` and `cinfo`

**Clan Leader Commands**
- `{prefix}clandisband` - `cd`
- `{prefix}claninvite` - `ci`
- `{prefix}clanremove` - `cr`
- `{prefix}clanpromote` - `promote`
- `{prefix}clandemote` - `demote`
- `{prefix}changeleader` - `cl`

**Clan info Commands**
- `{prefix}claninfo` - `info`
- `{prefix}clansetdiscord` - `csd`
- `{prefix}clansetyoutube` - `csy`
- `{prefix}clansetlogo` - `csl`
- `{prefix}clansetbanner` - `csb`
- `{prefix}clansetcolor` - `csc`
""", color = self.bot.embedColour)
        
        return await ctx.reply(embed = embed)


    @commands.command(name = "test")
    async def test(self, ctx):
        await ctx.reply(embed=discord.Embed(description = "- test"))


    @commands.Cog.listener()
    async def on_ready(self):
        print(f"Cog {self.__class__.__name__} has been successfully initiated\n------------")

async def setup(bot):
    await bot.add_cog(Help(bot))
        
        