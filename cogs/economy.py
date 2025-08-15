import discord
from discord.ext import commands

class Economy(commands.Cog):
    def __init__(self, client):
        self.client = client
        
    @commands.hybrid_command(name="balance", description="Check you're balance.")
    async def balance(self, ctx):
        cursor = self.client.cursor
        cursor.execute('SELECT balance FROM economy WHERE user_id = ?', (ctx.author.id,))
        results = cursor.fetchone()
        balance = results[0] if results else 0
        bal = discord.Embed(title="Balance", description=f"__Balance__: **${balance}**", colour=discord.Colour.green())
        bal.set_footer(text=f"Requested by {ctx.author.name}", icon_url=ctx.author.display_avatar.url)
        await ctx.send(embed=bal)
    @commands.command(name="bal", description="Check you're balance.")
    async def bal(self, ctx):
        cursor = self.client.cursor
        conn = self.client.conn
        cursor.execute('SELECT balance FROM economy WHERE user_id = ?', (ctx.author.id,))
        results = cursor.fetchone()
        if results is None:
            cursor.execute("INSERT INTO economy (user_id, balance) VALUES (?, ?)", (ctx.author.id, 0))
            conn.commit()
            balance = 0
        else:
            balance = results[0]
        bal = discord.Embed(title="Balance", description=f"__Balance__: **${balance}**", colour=discord.Colour.green())
        bal.set_footer(text=f"Requested by {ctx.author.name}", icon_url=ctx.author.display_avatar.url)
        await ctx.send(embed=bal)
async def setup(client):
    await client.add_cog(Economy(client))