import discord
from discord.ext import commands
from db.database import get_connection

class UsernameCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='username')
    async def get_username(self, ctx):
        if ctx.guild is not None:
            return  # Only allow in DMs

        discord_id = str(ctx.author.id)

        try:
            with get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT [Username] FROM [DMOX].[Account].[Account]
                    WHERE [DiscordId] = ?
                """, (discord_id,))
                row = cursor.fetchone()

                if not row:
                    await ctx.send("❌ You don't have an account.")
                    return

                await ctx.send(f"👤 Your username is: `{row.Username}`")

        except Exception as e:
            await ctx.send(f"❌ Database error: {str(e)}")

async def setup(bot):
    await bot.add_cog(UsernameCog(bot))
