import discord
from discord.ext import commands

class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="ping", description="Check bot latency.")
    async def ping(self, ctx):
        await ctx.send(f'Pong! **{round(self.bot.latency * 1000)}ms**')
    @commands.hybrid_command(name="help", description="help command.")
    async def help(self, ctx):
        help = discord.Embed(title="List of all commands", description="Supported types: **message** & **application commands**\n\n__General__:\ndn!help\ndn!ping\n\n__Economy__:\ndn!bal\ndn!add (admin only)\ndn!set (admin only)", colour=discord.Colour.orange())
        help.set_footer(text=f"requested by {ctx.author.name}", icon_url=ctx.author.display_avatar.url)
        await ctx.send(embed=help)

async def setup(bot):
    await bot.add_cog(General(bot))