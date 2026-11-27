import discord, datetime
from discord.ext import commands

class clanUtils:
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    async def genStaffList(self):
        staffList = []
        ## Fetch guild
        guild = self.bot.get_guild(self.bot.config["Guild ID"])
        
        for role in self.bot.config["Roles"]["Staff Roles"]:
            role = guild.get_role(role)
            for member in role.members:
                staffList.append(member.id)
        
        return staffList
    
    async def createClan(self, ctx, tag: str, leader: discord.User):
        db = self.bot.pendingclans
        
        if tag and leader:
            pass
        else:
            return False
        
        channel = await self.bot.fetch_channel(self.bot.config["Channels"]["Accept Clan Request ChannelID"])
        embed = discord.Embed(title = f"Request for: {tag}", description = f"Clan tag: `{tag}`\nLeader: {leader.mention} `({leader.id})`", color = self.bot.embedColour)
        embed.timestamp = datetime.datetime.utcnow()
        try:
            embed.set_footer(text=ctx.author.display_name, icon_url=ctx.author.avatar.url)
        except:
            embed.set_footer(text=ctx.author.display_name)
        
        msg = await channel.send(embed = embed, view = AcceptDenyClan(self.bot))
        
        
        data = {
            "_id": tag.lower(),
            "tag": tag,
            "channel_id": None,
            "role_id": None,
            "role_colour": None,
            "leader_id": leader.id,
            "co_leaders": [],
            "members": [],
            "created_at": datetime.datetime.now().strftime("%H:%M:%S %d/%m/%Y"),
            "pending_message_id": msg.id,
            "KOTH_wins": 0,
            "Maze_wins": 0,
            "Roam_wins": 0,
            "discord_link": None,
            "youtube_link": None,
            "logo_link": None,
            "banner_link": None
        }
        try:
            db.insert_one(data)
        except:
            await msg.delete()
            embed = discord.Embed(description = f"There is already a clan with the tag `{tag}`", color = 0xff0000)
            embed.timestamp = datetime.datetime.utcnow()
            try:
                embed.set_footer(text=ctx.author.display_name, icon_url=ctx.author.avatar.url)
            except:
                embed.set_footer(text=ctx.author.display_name)
            
            await ctx.reply(embed = embed)
        
        
        
        embed = discord.Embed(description = f"> Submitted request for `{tag}`", color = 0x57F287)
        embed.timestamp = datetime.datetime.utcnow()
        try:
            embed.set_footer(text=ctx.author.display_name, icon_url=ctx.author.avatar.url)
        except:
            embed.set_footer(text=ctx.author.display_name)
        
        await ctx.reply(embed = embed)
    
    async def disbandClan(self, ctx: discord.Interaction, clantag: str):
        ## Delete clan from DB
        db = self.bot.clandb
        clan = db.find_one({"_id": clantag.lower()})
        role = clan["role_id"]
        channel = clan["channel_id"]
        tag = clan["tag"]
        guild = self.bot.get_guild(self.bot.config["Guild ID"])
        if not clan:
            return await ctx.response.send_message(embed = discord.Embed(description = "> Clan does not exist", color = 0xE74C3C))
        
        ## Remove leader role
        temp = guild.get_role(self.bot.config["Roles"]["Clan Leader Role"])

        
        ## Remove co-leader roles from co-leaders
        temp = guild.get_role(self.bot.config["Roles"]["Co-Leader Role"])
        
        for leader in clan["co_leaders"]:
            member = await guild.fetch_member(leader)
            await member.remove_roles(role)
        
        db.delete_one(clan)
        
        ## Delete role
        role = guild.get_role(role)
        await role.delete()
        
        ## Delete channel
        channel = guild.get_channel(channel)
        await channel.delete()
        
        embed = discord.Embed(description = f"> Successfully disbanded {clan['tag']}")
        try:
            try:
                await ctx.response.send_message(embed = embed)
            except:
                pass
        except:
            await ctx.reply(embed = embed)
        
        logchannel = await self.bot.guild.fetch_channel(self.bot.config["Channels"]["Clan Logs ChannelID"])
        embed = discord.Embed(description = f"`{tag}` has been disbanded", color = 0xE74C3C)
        embed.timestamp = datetime.datetime.utcnow()
        try:
            embed.set_footer(text = f"{ctx.author.display_name}", icon_url=ctx.author.avatar.url)
        except:
            try:
                embed.set_footer(text=f"{ctx.author.display_name}")
            except:
                try:
                    embed.set_footer(text = f"{ctx.user.name}", icon_url=ctx.user.avatar.url)
                except:
                    embed.set_footer(text = f"{ctx.user.name}")
        await logchannel.send(embed=embed)
        
        
    async def inviteMember(self, ctx, clan, member: discord.Member):
        db = self.bot.clandb
        pendinginvites = self.bot.db.pendinginvitesdb
        
        if not clan:
            return await ctx.reply(embed = discord.Embed(description = "> Clan does not exist", color = 0xE74C3C))
        
        if member.id in clan["members"]:
            return await ctx.reply(embed = discord.Embed(description = "> Member is already in clan", color = 0xE74C3C))
        
        if member.id in clan["co_leaders"]:
            return await ctx.reply(embed = discord.Embed(description = "> Member is already a co-leader", color = 0xE74C3C))
        
        if member.id == clan["leader_id"]:
            return await ctx.reply(embed = discord.Embed(description = "> You cannot invite the leader of a clan to their own clan", color = 0xE74C3C))
        
        invites = pendinginvites.find()
        for invite in invites:
            if invite["clan_id"] == clan["_id"] and invite["invitee_id"] == member.id:
                return await ctx.reply(embed = discord.Embed(description = "> You have already invited this member", color = 0xE74C3C))
            elif invite["invitee_id"] == member.id:
                return await ctx.reply(embed = discord.Embed(description = "> This member has a pending invite from another clan", color = 0xE74C3C))
        
        embed = discord.Embed(description = f"> Successfully invited {member.mention} to <@&{clan['role_id']}>", color = 0x57F287)
        await ctx.reply(embed = embed)
        
        try:
            msg = await member.send(embed = discord.Embed(description = f"You have been invited to `{clan['tag']}`. Please select below if you would like to accept or deny their offer.", color = discord.Color.green()), view = AcceptDenyInvite(self.bot))
            
            data = {
            "invitee_id": member.id,
            "clan_id": clan["_id"],
            "clan_tag": clan['tag'],
            "pending_message_id": msg.id
            }
            
            self.bot.pendinginvitesdb.insert_one(data)
        except discord.Forbidden:
            return await  ctx.reply(embed = f"> Unable to send invite to {member.mention}. Please tell them to open their DM's to me.", color = 0xE74C3C)
        
        


    async def removeMember(self, ctx, clan, member: discord.Member):
        db = self.bot.clandb
        pendinginvites = self.bot.db.pendinginvitesdb
        
        if not clan:
            return await ctx.reply(embed = discord.Embed(description = "> Clan does not exist", color = 0xE74C3C))
        
        
        if member.id not in clan["members"] and member.id != clan["leader_id"]:
            return await ctx.reply(embed = discord.Embed(description = f"> Member is not in <@&{clan['role_id']}>", color = 0xE74C3C))
        
        if member.id in clan["co_leaders"] and ctx.author.id in clan["co_leaders"]:
            return await ctx.reply(embed = discord.Embed(description = "> You cannot remove another co-leader", color = 0xE74C3C))
        
        if member.id == clan["leader_id"]:
            return await ctx.reply(embed = discord.Embed(description = "> You cannot remove the leader of a clan from their own clan", color = 0xE74C3C))
        
        
        ## Remove the member from the clan members and ensure they arent in the co-leaders
        
        try:
            clan["members"].remove(member.id)
        except ValueError: pass
        try:
            clan["co_leaders"].remove(member.id)
        except ValueError: pass
        
        ## Update database
        
        db.update_one({"_id": clan["_id"]}, {"$set": {"members": clan["members"], "co_leaders": clan["co_leaders"]}})
        
        ## Remove users role
        
        guild = self.bot.get_guild(self.bot.config["Guild ID"])
        role = guild.get_role(clan["role_id"])
        coleaderrole = guild.get_role(self.bot.config["Roles"]["Co-Leader Role"])
        
        await member.remove_roles(role)
        try:
            await member.remove_roles(coleaderrole)
        except:
            pass
        
        ## Conirmation msg to action user and member
        
        embed = discord.Embed(description = f"> Successfully removed {member.mention} from <@&{clan['role_id']}>", color = discord.Color.red())
        await ctx.reply(embed = embed)
        
        try:
            msg = await member.send(embed = discord.Embed(description = f"You have been removed from `{clan['_id']}`.", color = discord.Color.red()))
        except discord.Forbidden:
            return await ctx.reply(embed = f"> Unable to send invite to {member.mention}. Please tell them to open their DM's to me.", color = discord.Color.red())
        
        
    
    async def isClan(self, ClanTag: str) -> bool:
        db = self.bot.clandb
        clan = db.find_one({"_id": ClanTag.lower()})
        db = self.bot.pendingclans
        pendingclan = db.find_one({"_id": ClanTag.lower()})
        if clan == None and pendingclan == None: return False, None 
        else: return True, clan
    
    async def isMemberInClan(self, MemberID: int) -> bool:
        db = self.bot.clandb
        clans = db.find()
        
        for clan in clans:
            if MemberID in clan["members"]:
                return True, clan
    
    async def isLeaderOfClan(self, MemberID: int, ClanTag: str) -> bool:
        db = self.bot.clandb
        clan = db.find_one({"_id": ClanTag.lower()})
        
        if MemberID == clan["leader_id"]:
            return True, clan
    
    async def isAuthorised(self, MemberID: int, ClanTag: str):
        db = self.bot.clandb
        clan = db.find_one({"_id": ClanTag.lower()})
        
        if MemberID == clan["leader_id"]:
            return True, clan
        elif MemberID in clan["co_leaders"]:
            return True, clan
        else: return False, None
    
    async def isInClan(self, MemberID: int):
        db = self.bot.clandb
        clans = db.find()
        pendingdb = self.bot.pendingclans
        pendingclans = pendingdb.find()

        for clan in clans:
            if MemberID == clan["leader_id"]:
                return True, clan
            if MemberID in clan["co_leaders"]:
                return True, clan
            if MemberID in clan["members"]:
                return True, clan
        
        for clan in pendingclans:
            if MemberID == clan["leader_id"]:
                return True, clan
            if MemberID in clan["co_leaders"]:
                return True, clan
            if MemberID in clan["members"]:
                return True, clan
        
        return False, None
        
    



class AcceptDenyInvite(discord.ui.View):
    def __init__(self, bot):
        self.bot = bot
        super().__init__(timeout = None)
    
    @discord.ui.button(label = "Accept", style = discord.ButtonStyle.green, custom_id = "acceptinvite")
    async def acceptinvite(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer(thinking = True)
        pendinginvites = self.bot.pendinginvitesdb
        invite = pendinginvites.find_one({"invitee_id": interaction.user.id})
        if invite == None:
            return await interaction.followup.send(embed = discord.Embed(description = "Something has gone wrong and your invite could not be found. Please ask the leader/co-leader to re-send the invite.", color = discord.Color.green()))
        
        db = self.bot.clandb
        clan = db.find_one({"_id": invite["clan_id"]})
        
        ## Update clan
        
        clan["members"].append(invite["invitee_id"])
        db.update_one({"_id": clan["_id"]}, {"$set": {"members": clan["members"]}})
        
        ## Give user clan role
        
        guild = await self.bot.fetch_guild(self.bot.config["Guild ID"])
        role = guild.get_role(clan["role_id"])
        member = await guild.fetch_member(invite["invitee_id"])
        await member.add_roles(role)
        
        ## Reply to user
        
        await interaction.followup.send(embed = discord.Embed(description = f"> You have successfully joined `{invite['clan_tag']}`", color = discord.Color.green()))
        
        ## Notify leader
        
        leader = await guild.fetch_member(clan["leader_id"])
        await leader.send(embed = discord.Embed(description = f"> <@{member.id}> ({member.name}) has accepted your offer to join `{invite['clan_tag']}`", color = discord.Color.green()))
        
        self.stop()
        await interaction.message.edit(content = "Joined", view=None)
    
    @discord.ui.button(label = "Decline", style = discord.ButtonStyle.red, custom_id = "declineinvite")
    async def declineinvite(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer(thinking = True)
        pendinginvites = self.bot.pendinginvitesdb
        invite = pendinginvites.find_one({"invitee_id": interaction.user.id})
        if invite == None:
            await interaction.followup.send(embed = discord.Embed(description = "Something has gone wrong and your invite could not be found. Please ask the leader/co-leader to re-send the invite.", color = discord.Color.green()))
        copy = invite
        pendinginvites.delete_one(invite)
        
        db = self.bot.clandb
        clan = db.find_one({"tag": copy["clan_tag"]})
        
        guild = await self.bot.fetch_guild(self.bot.config["Guild ID"])
        member = await guild.fetch_member(copy["invitee_id"])
        
        ## Notify leader
        
        leader = await guild.fetch_member(clan["leader_id"])
        await leader.send(embed = discord.Embed(description = f"> <@{member.id}> ({member.name}) has declined your offer to join `{clan['tag']}`", color = discord.Color.red()))
        
        ## Reply to user
        
        await interaction.followup.send(embed = discord.Embed(description = f"> You have declined the offer to join `{clan['tag']}`", color = discord.Color.red()))
        
        self.stop()
        await interaction.message.edit(content = "Denied", view=None)
        
        

class AcceptDenyClan(discord.ui.View):
    def __init__(self, bot):
        self.bot = bot
        
        super().__init__(timeout = None)
    
    @discord.ui.button(label='Accept', style=discord.ButtonStyle.green, custom_id = "clanaccept")
    async def accept(self, interaction: discord.Interaction, button: discord.ui.Button):
        
        ## Check if they're staff
        
        guild = self.bot.get_guild(self.bot.config["Guild ID"])
        stafflist = []
        
        for role in self.bot.config["Roles"]["Staff Roles"]:
            role = guild.get_role(role)
            for member in role.members:
                stafflist.append(member.id)
        
        if interaction.user.id in stafflist:
            pass
        else:
            return await interaction.response.send_message(embed = discord.Embed(description = "You are not staff", color = discord.Color.red()), ephemeral = True)
        
        self.stop()
        await interaction.message.edit(content = "Accepted", view=None)
        
        await interaction.response.defer(thinking = True)
        pendingdb = self.bot.pendingclans
        clansdb = self.bot.clandb
        clan = pendingdb.find_one({"pending_message_id": interaction.message.id})

        ## Create Role
        role = await self.bot.guild.create_role(name = clan["tag"])


        ## Create channel
        overwrites = {
            self.bot.guild.default_role: discord.PermissionOverwrite(read_messages=True, send_messages=False, view_channel = True),
            role: discord.PermissionOverwrite(read_messages=True, send_messages=True, view_channel = True)
        }
        
        for srole in self.bot.config["Roles"]["Staff Roles"]:
            staffrole = self.bot.guild.get_role(srole)
            overwrites[staffrole] = discord.PermissionOverwrite(read_messages=True, send_messages=False, view_channel = True)
        
        category = await self.bot.fetch_channel(self.bot.config["ClanCategoryID"])
        channel = await self.bot.guild.create_text_channel(clan["tag"], category = category, topic = f"Clan channel for {clan['tag']}", overwrites = overwrites)
        prefix = self.bot.config["Bot Prefix"]
        await channel.send(f"<@&{role.id}>", embed = discord.Embed(title = "Clan Bot", description = f"""**Clan Leader Commands**
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
- `{prefix}clansetcolor` `#ffffff`""", color = self.bot.embedColour))
        
        clan["channel_id"] = channel.id
        clan["role_id"] = role.id
        
        
        clansdb.insert_one(clan)
        pendingdb.delete_one({"_id": clan["_id"]})
        
        guild = await self.bot.fetch_guild(self.bot.config["Guild ID"])
        leader = await guild.fetch_member(clan["leader_id"])
        
        await leader.add_roles(role)
        leaderrole = self.bot.guild.get_role(self.bot.config["Roles"]["Clan Leader Role"])
        await leader.add_roles(leaderrole)
        
        await leader.send(embed = discord.Embed(description = f"> Your clan `{clan['tag']}` has been accepted by staff", color = 0x57F287))
        await interaction.followup.send(embed = discord.Embed(description = f"> Accepted `{clan['tag']}`", color = 0x57F287))
        
        logchannel = await guild.fetch_channel(self.bot.config["Channels"]["Clan Logs ChannelID"])
        embed = discord.Embed(description = f"`{clan['tag']}` ({channel.mention}) has been created", color = 0x57F287)
        embed.timestamp = datetime.datetime.utcnow()
        try:
            embed.set_footer(text = f"Accepted by {interaction.user.display_name}", icon_url=interaction.user.avatar.url)
        except:
            embed.set_footer(text=f"Accepted by {interaction.user.display_name}")
        await logchannel.send(embed=embed)
            
    
    @discord.ui.button(label='Decline', style=discord.ButtonStyle.red, custom_id = "clandecline")
    async def deny(self, interaction: discord.Interaction, button: discord.ui.Button): 
        ## Check if they're staff
        clanutils = clanUtils(self.bot)
        stafflist = clanutils.genStaffList()
        
        guild = self.bot.get_guild(self.bot.config["Guild ID"])
        stafflist = []
        
        for role in self.bot.config["Roles"]["Staff Roles"]:
            role = guild.get_role(role)
            for member in role.members:
                stafflist.append(member.id)
        
        if interaction.user.id in stafflist:
            pass
        else:
            return await interaction.response.send_message(embed = discord.Embed(description = "You are not staff", color = discord.Color.red()), ephemeral = True)
        
        
        pendingdb = self.bot.pendingclans
        clan = pendingdb.find_one({"pending_message_id": interaction.message.id})
        ## remove from database
        pendingdb.delete_one(clan)
        guild = await self.bot.fetch_guild(self.bot.config["Guild ID"])
        leader = await guild.fetch_member(clan["leader_id"])
        await leader.send(embed = discord.Embed(description = f"> Your clan `{clan['tag']}` has been denied by staff.", color = 0xE74C3C))
        await interaction.response.send_message(embed = discord.Embed(description = f"> Denied `{clan['tag']}`", color = 0xE74C3C))
        
        self.stop()
        await interaction.message.edit(content = "Denied", view=None)

