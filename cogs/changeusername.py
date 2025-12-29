import discord
from discord.ext import commands
from db.database import get_connection

class ChangeUsernameCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='changeusername')
    async def change_username(self, ctx, *, new_username: str = None):
        if ctx.guild is not None:
            return  # DM only

        if not new_username:
            await ctx.send("❌ Please provide a new username. Usage: `!changeusername <new_username>`")
            return

        discord_id = str(ctx.author.id)

        try:
            with get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT 1 FROM [DMOX].[Account].[Account]
                    WHERE [DiscordId] = ?
                """, (discord_id,))
                if not cursor.fetchone():
                    await ctx.send("❌ You don't have an account.")
                    return

                cursor.execute("""
                    UPDATE [DMOX].[Account].[Account]
                    SET [Username] = ?
                    WHERE [DiscordId] = ?
                """, (new_username, discord_id))
                conn.commit()

            await ctx.send("✅ Your username has been successfully changed.")

        except Exception as e:
            await ctx.send(f"❌ Failed to update username: {str(e)}")

async def setup(bot):
    await bot.add_cog(ChangeUsernameCog(bot))
