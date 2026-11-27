import discord
from discord.ext import commands

class miscUtils:
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

    
            