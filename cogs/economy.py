import discord
import typing
from typing import Optional
from discord.ext import commands

class Economy(commands.Cog):
    def __init__(self, client):
        self.client = client


    
    @commands.hybrid_group()
    async def eco(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send("Please specify a subcommand.")
        
    @eco.command(name="balance", description="Check you're balance.")
    @commands.guild_only()
    async def balance(self, ctx, member: typing.Optional[discord.Member]):
        if member is None:
            member = ctx.author
        cursor = self.client.cursor
        conn = self.client.conn
        cursor.execute('SELECT balance FROM economy WHERE user_id = ?', (member.id,))
        results = cursor.fetchone()
        if results is None:
            cursor.execute("INSERT INTO economy (user_id, balance) VALUES (?, ?)", (member.id, 0))
            conn.commit()
            balance = 0
        else:
            balance = results[0]
        formatted_balance = f"₹{balance:,}"
        bal = discord.Embed(title=f"{member.name}'s Balance", description=f"Balance: **{formatted_balance}**", colour=discord.Colour.green())
        bal.set_footer(text=f"Requested by {ctx.author.name}", icon_url=ctx.author.display_avatar.url)
        await ctx.send(embed=bal)
    
    @eco.command(name="add", description="adds a certain amount to you're balance.")
    @commands.guild_only()
    @commands.has_permissions(manage_guild=True)
    async def add(self, ctx, member: typing.Optional[discord.Member] ,amount: int):
        if member is None:
            member = ctx.author
        cursor = self.client.cursor
        conn = self.client.conn
        cursor.execute('SELECT balance FROM economy WHERE user_id = ?', (member.id,))
        results = cursor.fetchone()
        if results is None:
            total_balance = amount
            cursor.execute("INSERT INTO economy (user_id, balance) VALUES (?, ?)", (member.id, total_balance))
        else:
            balance = results[0]
            total_balance = balance + amount
            cursor.execute("UPDATE economy SET balance = ? WHERE user_id = ?", (total_balance ,member.id))
        conn.commit()
        formatted_balance = f"₹{total_balance:,}"
        await ctx.send(f"Successfully updated **{member.name}'s** balance to __{formatted_balance}__")
    
    @eco.command(name="set", description="sets the balance of a user to an certain amount.")
    @commands.guild_only()
    @commands.has_permissions(manage_guild=True)
    async def set(self, ctx, member: typing.Optional[discord.Member] ,amount: int):
        if member is None:
            member = ctx.author
        cursor = self.client.cursor
        conn = self.client.conn
        cursor.execute("""INSERT INTO economy (user_id, balance) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET balance = excluded.balance
""", (member.id, amount))
        
        conn.commit()
        formatted_balance = f"₹{amount:,}"
        await ctx.send(f"Successfully updated **{member.name}'s** balance to __{formatted_balance}__")
    
    @eco.command(name="bal", description="Check you're balance.")
    @commands.guild_only()
    async def bal(self, ctx, member: typing.Optional[discord.Member]):
        if member is None:
            member = ctx.author
        cursor = self.client.cursor
        conn = self.client.conn
        cursor.execute('SELECT balance FROM economy WHERE user_id = ?', (member.id,))
        results = cursor.fetchone()
        if results is None:
            cursor.execute("INSERT INTO economy (user_id, balance) VALUES (?, ?)", (member.id, 0))
            conn.commit()
            balance = 0
        else:
            balance = results[0]
        formatted_balance = f"₹{balance:,}"
        bal = discord.Embed(title=f"{member.name}'s Balance", description=f"Balance: **{formatted_balance}**", colour=discord.Colour.green())
        bal.set_footer(text=f"Requested by {ctx.author.name}", icon_url=ctx.author.display_avatar.url)
        await ctx.send(embed=bal)
        
async def setup(client):
    await client.add_cog(Economy(client))