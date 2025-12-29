import discord
from discord.ext import commands
from db.database import get_connection

class ResetSecondPasswordCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='resetsecondpassword')
    async def reset_second_password(self, ctx):
        if ctx.guild is not None:
            return  # Only allow in DMs

        discord_id = str(ctx.author.id)

        try:
            with get_connection() as conn:
                cursor = conn.cursor()
                # Check if user has an account
                cursor.execute("""
                    SELECT 1 FROM [DMOX].[Account].[Account]
                    WHERE [DiscordId] = ?
                """, (discord_id,))
                if not cursor.fetchone():
                    await ctx.send("❌ You don't have an account.")
                    return

                # Reset SecondaryPassword to NULL
                cursor.execute("""
                    UPDATE [DMOX].[Account].[Account]
                    SET [SecondaryPassword] = NULL
                    WHERE [DiscordId] = ?
                """, (discord_id,))
                conn.commit()

            await ctx.send("✅ Your secondary password has been reset.")

        except Exception as e:
            await ctx.send(f"❌ Database error: {str(e)}")

async def setup(bot):
    await bot.add_cog(ResetSecondPasswordCog(bot))
