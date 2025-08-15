import discord
import typing
from typing import Optional
from discord.ext import commands

class Economy(commands.Cog):
    def __init__(self, client):
        self.client = client
        
    @commands.hybrid_command(name="balance", description="Check you're balance.")
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
        bal = discord.Embed(title="Balance", description=f"Balance: **${balance}**", colour=discord.Colour.green())
        bal.set_footer(text=f"Requested by {ctx.author.name}", icon_url=ctx.author.display_avatar.url)
        await ctx.send(embed=bal)
    
    @commands.hybrid_command(name="add", description="adds a certain amount to you're balance.")
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
        await ctx.send(f"Successfully updated **{member.name}'s** balance to __${total_balance}__")
    
    @commands.hybrid_command(name="set", description="sets the balance of a user to an certain amount.")
    @commands.has_permissions(manage_guild=True)
    async def set(self, ctx, member: typing.Optional[discord.Member] ,amount: int):
        if member is None:
            member = ctx.author
        cursor = self.client.cursor
        conn = self.client.conn
        cursor.execute("UPDATE economy SET balance = ? WHERE user_id = ?", (amount ,member.id))
        results = cursor.fetchone()
        if results is None:
            cursor.execute("INSERT INTO economy (user_id, balance) VALUES (?, ?)", (member.id, amount))
        conn.commit()
        await ctx.send(f"Successfully updated **{member.name}'s** balance to __${amount}__")
    
    @commands.command(name="bal", description="Check you're balance.")
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
        bal = discord.Embed(title="Balance", description=f"Balance: **${balance}**", colour=discord.Colour.green())
        bal.set_footer(text=f"Requested by {ctx.author.name}", icon_url=ctx.author.display_avatar.url)
        await ctx.send(embed=bal)
        
async def setup(client):
    await client.add_cog(Economy(client))