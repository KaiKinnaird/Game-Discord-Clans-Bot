import discord, json, os
from discord.ext import commands
from pymongo import MongoClient
from utils.clanUtilities import AcceptDenyClan
from utils.clanUtilities import AcceptDenyInvite


class Bot(commands.Bot):
	def __init__(self):
		
		self.config = json.load(open("config.json"))
		self.mongo = MongoClient(self.config["MongoDB Connection String"])
		self.db = self.mongo[self.config["MongoDB Database Name"]]
		self.clandb = self.db.clans
		self.pendingclans = self.db.pending_clans
		self.pendinginvitesdb = self.db.pending_invites
		self.wipelistdb = self.db.wipelist
		self.embedColour = self.config["Embed Colour"]
		self.embedColour = int(self.embedColour.replace("#", "0x"), 16)
		super().__init__(command_prefix=self.config["Bot Prefix"], intents = discord.Intents.all())

	async def on_ready(self):
		print(f"Logged in as {self.user} (ID: {self.user.id})")
		print("Make by Murder#0845")
		print("------")
	
	async def setup_hook(self):
		self.add_view(AcceptDenyClan(self))
		self.add_view(AcceptDenyInvite(self))

		self.guild = await self.fetch_guild(self.config["Guild ID"])
		for cogpath in os.listdir("cogs"):
			if cogpath.endswith(".py"):
				await bot.load_extension(f'cogs.{cogpath[:-3]}')


	async def on_command_error(self, ctx, error):
		## Error checking
		
		if isinstance(error, commands.CommandOnCooldown):
			await ctx.reply(embed=discord.Embed(description = f"Please wait {error.retry_after:.2f} seconds before using this command again. Cooldowns are in place to prevent spamming in case unauthorised users get access to run this command on accident or through other means.", color = discord.Color.red()), ephemeral=True)
			return
		if isinstance(error, commands.MissingRole):
			await ctx.reply(embed=discord.Embed(description = f"You do not have permission to use this command.", color = discord.Color.red()), ephemeral=True)
			return
		if isinstance(error, commands.MissingRequiredArgument):
			await ctx.reply(embed=discord.Embed(description = f"Please provide all required arguments.", color = discord.Color.red()), ephemeral=True)
			return
		if isinstance(error, commands.BadArgument):
			await ctx.reply(embed=discord.Embed(description = f"Please provide a valid argument.", color = discord.Color.red()), ephemeral=True)
			return
		if isinstance(error, commands.CommandNotFound):
			await ctx.reply(embed=discord.Embed(description = f"Command not found.", color = discord.Color.red()), ephemeral=True)
			return
		if isinstance(error, commands.BotMissingPermissions):
			await ctx.reply(embed=discord.Embed(description = f"Bot is missing permissions.", color = discord.Color.red()), ephemeral=True)
			return
		if isinstance(error, commands.MissingPermissions):
			await ctx.reply(embed=discord.Embed(description = f"You are missing permissions.", color = discord.Color.red()), ephemeral=True)
			return
		if isinstance(error, commands.CheckFailure):
			await ctx.reply(embed=discord.Embed(description = f"You do not have permission to use this command.", color = discord.Color.red()), ephemeral=True)
			return
		if isinstance(error, commands.UserInputError):
			await ctx.reply(embed=discord.Embed(description = f"Please provide a valid argument.", color = discord.Color.red()), ephemeral=True)
			return
		if isinstance(error, commands.DisabledCommand):
			await ctx.reply(embed=discord.Embed(description = f"This command is disabled.", color = discord.Color.red()), ephemeral=True)
			return 
		
		raise error
	
	async def on_command(self, ctx):
		print(f"{ctx.author} ran {ctx.command} in {ctx.guild}")

	async def on_guild_join(self, guild):
		print(f"Joined {guild.name}")
	
	async def on_guild_remove(self, guild):
		print(f"Left {guild.name}")

	def run(self):
		super().run(self.config["Bot Token"], reconnect=True)

bot = Bot()
bot.remove_command("help")

bot.run()