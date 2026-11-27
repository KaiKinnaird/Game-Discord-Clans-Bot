import discord, validators, re, datetime, demoji
from discord.ext import commands
from discord.ext.commands import Cog
from utils.miscUtilities import miscUtils
from utils.clanUtilities import clanUtils


class clanInfo(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.miscutils = miscUtils(bot)
        self.clanutils = clanUtils(bot)
    
    @commands.command(name="claninfo", aliases=["info", "cinfo"])
    async def claninfo(self, ctx, clanidentifier: str = None):
        if clanidentifier == None:
            isInClan, clan = await self.clanutils.isInClan(ctx.author.id)
            clanidentifier = clan['tag']
            if not isInClan:
                return await ctx.reply(embed = discord.Embed(description = "You are not in a clan so you need to specify a clantag to see clan info"))
        
        if clanidentifier == None:
            return await ctx.reply(embed = discord.Embed(description = f"Clan `{clanidentifier}` does not exist", color = 0xE74C3C))
        
        if clanidentifier != None:
            clan = self.bot.clandb.find_one({"_id": clanidentifier.lower()})
            if clan == None:
                return await ctx.reply(embed = discord.Embed(description = f"Clan `{clanidentifier}` does not exist", color = 0xE74C3C))
        
        
        ## Construct embed
        
        ### Add discord and youtube
        discordYoutubeString = []
        
        if clan["discord_link"] != None:
            discordYoutubeString.append(f"[Discord]({clan['discord_link']})")
        
        if clan["youtube_link"] != None:
            discordYoutubeString.append(f"[Youtube]({clan['youtube_link']})")
        
        discordYoutubeString = " | ".join(discordYoutubeString)
        
        
        
        ### Construct members
        member_string = []
        for member in clan['members']:
            if member not in clan["co_leaders"]:
                member_string.append(f"<@{member}>")
        
        member_count = len(member_string) + len(clan["co_leaders"]) + 1
        member_string = "\n".join(member_string)     
        
        ### Construct co_leaders
        co_leaderString = []
        for co_leader in clan['co_leaders']:
            co_leaderString.append(f"<@{co_leader}>")
        
        co_leaderString = "\n".join(co_leaderString)
        
        if co_leaderString == "":
            co_leaderString = "None"
        
        if member_string == "":
            member_string = "None"
        
        if clan["role_colour"]:
            colour = clan["role_colour"]
        else:
            colour = self.bot.embedColour
        
        embed = discord.Embed(title = f"Clan | {clan['tag']}", description = f"""{discordYoutubeString}""", color = colour)
        
        embed.add_field(name = "Leader", value = f"<@{clan['leader_id']}>", inline = True)
        embed.add_field(name = "Co-Leader(s)", value = co_leaderString, inline = True)
        embed.add_field(name = "Member Count", value = f"{member_count}")
        embed.add_field(name = "Members", value = member_string, inline = False)
        
        ## Set graphics
        embed.set_thumbnail(url = clan['logo_link'])
        embed.set_image(url = clan['banner_link'])
        
        ## Set time of creation
        embed.set_footer(text = f"Created at {clan['created_at']} | Requested by {ctx.author.name}")
        
        ## Send embed
        await ctx.reply(embed = embed)
        
    
    @commands.command(name="clansetlogo", aliases=["csl", "setlogo"])
    async def clansetlogo(self, ctx, *, logourl: str):
        isInClan, clan = await self.clanutils.isInClan(ctx.author.id)
        
        if not isInClan:
            return await ctx.reply(embed = discord.Embed(description = "> You are not in a clan", color = discord.Color.red()))
        
        auth, clan = await self.clanutils.isAuthorised(ctx.author.id, clan["tag"])
        if auth:
            if not validators.url(logourl):
                return await ctx.reply(embed = discord.Embed(description = "> Invalid URL. Ensure your URL is in the format of https://imgur.com/image (NOTE: It just needs to be a direct URL to an image)", color = discord.Color.red()))
            
            ## Update DB
            
            self.bot.clandb.update_one({"_id": clan["_id"].lower()}, {"$set": {"logo_link": logourl}})
            
            ## Display it back to the user
            
            embed = discord.Embed(description = f"> Successfully set the logo to {logourl}", color = discord.Color.green())
            embed.set_thumbnail(url = logourl)
            return await ctx.reply(embed = embed)

    @commands.command(name="clansetbanner", aliases=["csb", "setbanner"])
    async def clansetbanner(self, ctx, *, bannerurl: str):
        isInClan, clan = await self.clanutils.isInClan(ctx.author.id)
        
        if not isInClan:
            return await ctx.reply(embed = discord.Embed(description = "> You are not in a clan", color = discord.Color.red()))
        
        auth, clan = await self.clanutils.isAuthorised(ctx.author.id, clan["tag"])
        if auth:
            if not validators.url(bannerurl):
                return await ctx.reply(embed = discord.Embed(description = "> Invalid URL. Ensure your URL is in the format of https://imgur.com/image (NOTE: It just needs to be a direct URL to an image)", color = discord.Color.red()))
            
            ## Update DB
            
            self.bot.clandb.update_one({"_id": clan["_id"]}, {"$set": {"banner_link": bannerurl}})
            
            ## Display it back to the user
            
            embed = discord.Embed(description = f"> Successfully set the banner to {bannerurl}", color = discord.Color.green())
            embed.set_image(url = bannerurl)
            return await ctx.reply(embed = embed)
    
    @commands.command(name="clansetdiscord", aliases=["csd", "setdiscord"])
    async def clansetdiscord(self, ctx, *, discordurl: str):
        isInClan, clan = await self.clanutils.isInClan(ctx.author.id)
        
        if not isInClan:
            return await ctx.reply(embed = discord.Embed(description = "> You are not in a clan", color = discord.Color.red()))
        
        auth, clan = await self.clanutils.isAuthorised(ctx.author.id, clan["tag"])
        if auth:
            if not validators.url(discordurl):
                return await ctx.reply(embed = discord.Embed(description = "> Invalid URL. Ensure your URL is in the format of https://discord.gg/yourinvitecode (NOTE: It just needs to be a direct URL to a discord)", color = discord.Color.red()))
            
            ## Update DB
            
            self.bot.clandb.update_one({"_id": clan["_id"]}, {"$set": {"discord_link": discordurl}})
            
            ## Display it back to the user
            
            embed = discord.Embed(description = f"> Successfully set the discord to {discordurl}", color = discord.Color.green())
            return await ctx.reply(discordurl, embed = embed)

    @commands.command(name="clansetyoutube", aliases=["csy", "setyoutube"])
    async def clansetyoutube(self, ctx, *, youtubeurl: str):
        isInClan, clan = await self.clanutils.isInClan(ctx.author.id)
        
        if not isInClan:
            return await ctx.reply(embed = discord.Embed(description = "> You are not in a clan", color = discord.Color.red()))
        
        auth, clan = await self.clanutils.isAuthorised(ctx.author.id, clan["tag"])
        if auth:
            if not validators.url(youtubeurl):
                return await ctx.reply(embed = discord.Embed(description = "> Invalid URL. Ensure your URL is in the format of https://youtube.com/videoorchannel (NOTE: It just needs to be a direct URL to a video or channel)", color = discord.Color.red()))
            
            ## Update DB
            
            self.bot.clandb.update_one({"_id": clan["_id"]}, {"$set": {"youtube_link": youtubeurl}})
            
            ## Display it back to the user
            
            embed = discord.Embed(description = f"> Successfully set the youtube url to {youtubeurl}", color = discord.Color.green())
            return await ctx.reply(youtubeurl, embed = embed)
    
    @commands.command(name="clansetcolor", aliases=["csc", "setcolor"])
    async def clansetcolor(self, ctx, *, colorhex):
        isInClan, clan = await self.clanutils.isInClan(ctx.author.id)
        
        if not isInClan:
            return await ctx.reply(embed = discord.Embed(description = "> You are not in a clan", color = discord.Color.red()))
        
        auth, clan = await self.clanutils.isAuthorised(ctx.author.id, clan["tag"])
        if auth:
            ## Verify that the colorhex is actual a hex code
            match = re.search(r"^#(?:[0-9a-fA-F]{3}){1,2}$", colorhex)
            
            if match:
                ## Conver hex to integer colour code. e.g: 0xffffff
                colorint = int(colorhex.replace("#", "0x"), 16)
                
                ## Fetch role and change role colour
                role = discord.utils.get(ctx.guild.roles, id = clan["role_id"])
                await role.edit(colour = colorint)
                
                ## Add to database
                self.bot.clandb.update_one({"_id": clan["_id"]}, {"$set": {"role_colour": colorint}})
                
                ## Respond to user displaying the colour
                return await ctx.reply(embed = discord.Embed(description = f"> Successfully set the clan colour to {colorhex}", color = colorint))
            else:
                return await ctx.reply(embed = discord.Embed(description = "> Invalid hex code. Ensure your hex code is in the format of #ffffff", color = discord.Color.red()))
    
    ## Changeleader command
    @commands.command(name = "changeleader", aliases = ["cl"])
    async def changeleader(self, ctx, *, user: discord.User):
        isInClan, clan = await self.clanutils.isInClan(ctx.author.id)
        
        if not isInClan:
            return await ctx.reply(embed = discord.Embed(description = "> You are not in a clan", color = discord.Color.red()))
        
        auth, clan = await self.clanutils.isAuthorised(ctx.author.id, clan["tag"])
        
        if not auth:
            return await ctx.reply(embed = discord.Embed(description = "> You are not the leader of this clan", color = discord.Color.red()))
        
        if ctx.author.id != clan["leader_id"]:
            return await ctx.reply(embed = discord.Embed(description = "> You are not the leader of this clan", color = discord.Color.red()))
        elif ctx.author.id == clan["leader_id"]:
            ## Verify that the user if not in another clan or a leader of another clan
            
            if user.id == ctx.author.id:
                return await ctx.reply(embed = discord.Embed(description = "> You cannot change the leader to yourself", color = discord.Color.red()))
            
            isInClan, _ = await self.clanutils.isInClan(user.id)
            if isInClan:
                return await ctx.reply(embed = discord.Embed(description = "> This user is already in a clan", color = discord.Color.red()))
            
            await ctx.reply(embed = discord.Embed(description = "> Are you sure you want to change the leader of your clan?", color = discord.Color.orange()), view = confirmChangeLeader(self.bot, clan, user, ctx.author))
        else:
            return await ctx.reply(embed = discord.Embed(description = "> You are not the leader of a clan", color = 0xE74C3C))
    
    @commands.command(label = "changename", aliases = ["cn"])
    async def changename(self, ctx, newname):
        isInClan, clan = await self.clanutils.isInClan(ctx.author.id)
        
        if not isInClan:
            return await ctx.reply(embed = discord.Embed(description = "> You are not in a clan", color = discord.Color.red()))
        
        auth, clan = await self.clanutils.isAuthorised(ctx.author.id, clan["tag"])
        
        if not auth:
            return await ctx.reply(embed = discord.Embed(description = "> You are not the leader of this clan", color = discord.Color.red()))
        
        if ctx.author.id != clan["leader_id"]:
            return await ctx.reply(embed = discord.Embed(description = "> You are not the leader of this clan", color = discord.Color.red()))
        elif ctx.author.id == clan["leader_id"]:
            ## Regex check for emoji
            emoji = demoji.findall(newname)
            if emoji:
                return await ctx.reply(embed = discord.Embed(description = "> You cannot have emojis in your clan tag", color = 0xE74C3C))
            
            
            ## Verify name is available and then pass to view
            
            if newname.lower() == clan["tag"].lower():
                return await ctx.reply(embed = discord.Embed(description = f"> `{newname}` is already your clans tag", color = discord.Color.red()))
            
            isInClan, _ = await self.clanutils.isClan(newname)
            if isInClan:
                return await ctx.reply(embed = discord.Embed(description = "> This name has already been taken by another clan", color = discord.Color.red()))
            
            await ctx.reply(embed = discord.Embed(description = "> Are you sure you want to change the name of your clan?", color = discord.Color.orange()), view = confirmChangeName(self.bot, clan, newname, clan['_id'], ctx.author))
        else:
            return await ctx.reply(embed = discord.Embed(description = "> You are not the leader of a clan", color = 0xE74C3C))
            
            
    
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"Cog {self.__class__.__name__} has been successfully initiated\n------------")

async def setup(bot):
    await bot.add_cog(clanInfo(bot))


class confirmChangeName(discord.ui.View):
    def __init__(self, bot, clan, newname, oldID,  author):
        self.bot = bot
        self.newname = newname
        self.oldID = oldID
        self.clan = clan
        self.originalclan = clan
        self.author = author
        super().__init__(timeout = None)
    
    @discord.ui.button(label = "Confirm", style = discord.ButtonStyle.green, custom_id = "confirmchangename")
    async def confirmchangename(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.author.id:
            return await interaction.response.send_message(embed = discord.Embed(description = "> You cannot interact with this message", color = 0xE74C3C), ephemeral = True)
        
        clan = self.clan
        await interaction.response.defer(thinking = True, ephemeral = True)
        
        db = self.bot.clandb
        #db.update_one({"_id": clan["_id"]}, {"$set": {"tag": self.newname, "_id": self.newname.lower()}})
        
        clan["_id"] = self.newname.lower()
        clan["tag"] = self.newname
        
        db.delete_one({"_id": self.oldID})
        db.insert_one(clan)
        
        ## Change channel name
        
        guild = self.bot.get_guild(self.bot.config["Guild ID"])
        channel = guild.get_channel(clan["channel_id"])
        await channel.edit(name = self.newname)
        
        ## Change role name
        
        role = guild.get_role(clan["role_id"])
        await role.edit(name = self.newname)
        
        
        ## Send to log channel
        
        logchannel = await self.bot.guild.fetch_channel(self.bot.config["Channels"]["Clan Logs ChannelID"])
        embed = discord.Embed(description = f"Name of `{self.oldID}` has been changed to `{self.newname}`", color = 0xffffff)
        embed.timestamp = datetime.datetime.utcnow()
        try:
            embed.set_footer(text = f"{interaction.user.display_name}", icon_url=interaction.user.avatar.url)
        except:
            embed.set_footer(text=f"{interaction.user.display_name}")
        await logchannel.send(embed=embed)
        
        self.stop()
        await interaction.followup.send("Confirmed")
        return await interaction.message.edit(content = "Confirmed", embed = discord.Embed(description = f"> Successfully changed the name of `{self.oldID}` to `{self.newname}`", color = 0x2ECC71),  view=None)
        
          
    @discord.ui.button(label = "Cancel", style = discord.ButtonStyle.red, custom_id = "cancelchangename")
    async def cancelchangename(self, interaction: discord.Interaction, button: discord.Button):
        if interaction.user.id != self.author.id:
            return await interaction.response.send_message(embed = discord.Embed(description = "> You cannot interact with this message", color = 0xE74C3C), ephemeral = True)
        
        self.stop()
        return await interaction.message.edit(embed = discord.Embed(description = "> Change name cancelled", color = 0xE74C3C), content = "Cancelled", view=None)
    









class confirmChangeLeader(discord.ui.View):
    def __init__(self, bot, clan, user: discord.Member, author):
        self.bot = bot
        self.user = user
        self.clan = clan
        self.author = author
        super().__init__(timeout = None)
    
    @discord.ui.button(label = "Confirm", style = discord.ButtonStyle.green, custom_id = "confirmchangeleader")
    async def confirmchangeleader(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.author.id:
            return await interaction.response.send_message(embed = discord.Embed(description = "> You cannot interact with this message", color = 0xE74C3C), ephemeral = True)
        
        clan = self.clan
        user = self.user
        await interaction.response.defer(thinking = True)
        
        ## convert User obj to Member
        
        guild = self.bot.get_guild(self.bot.config["Guild ID"])
        user = guild.get_member(user.id)
        
        db = self.bot.clandb
        db.update_one({"_id": clan["_id"]}, {"$set": {"leader_id": user.id}})
        
        ## Remove leader role from ctx.author and add to user
        guild = self.bot.get_guild(self.bot.config["Guild ID"])
        leaderRole = guild.get_role(self.bot.config["Roles"]["Clan Leader Role"])
        
        await interaction.user.remove_roles(leaderRole)
        await user.add_roles(leaderRole)
        
        ## Remove clan role and add to user
        
        clanRole = guild.get_role(clan["role_id"])
        
        await interaction.user.remove_roles(clanRole)
        await user.add_roles(clanRole)
        
        
        ## Send to log channel
        
        logchannel = await self.bot.guild.fetch_channel(self.bot.config["Channels"]["Clan Logs ChannelID"])
        embed = discord.Embed(description = f"Leader of `{clan['tag']}` has been changed from {self.author.mention} to {user.mention}", color = 0xffffff)
        embed.timestamp = datetime.datetime.utcnow()
        try:
            embed.set_footer(text = f"{interaction.user.display_name}", icon_url=interaction.user.avatar.url)
        except:
            embed.set_footer(text=f"{interaction.user.display_name}")
        await logchannel.send(embed=embed)
        
        return await interaction.followup.send(embed = discord.Embed(description = "> Successfully changed the leader. Note you have been removed from the clan.", color = 0x2ECC71))
    
    @discord.ui.button(label = "Cancel", style = discord.ButtonStyle.red)
    async def cancelchangeleadercallback(self, interaction: discord.Interaction, button: discord.Button):
        if interaction.user.id != self.author.id:
            return await interaction.response.send_message(embed = discord.Embed(description = "> You cannot interact with this message", color = 0xE74C3C), ephemeral = True)
        
        return await interaction.response.send_message(embed = discord.Embed(description = "> Transfer leader cancelled", color = 0xE74C3C))