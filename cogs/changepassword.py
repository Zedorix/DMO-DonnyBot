import discord
from discord.ext import commands
from db.database import get_connection
import base64

class ChangePasswordCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='changepassword')
    async def change_password(self, ctx, *, new_password: str = None):
        if ctx.guild is not None:
            return  # DM only

        if not new_password:
            await ctx.send("❌ Please provide a new password. Usage: `!changepassword <new_password>`")
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

                encoded_new_password = base64.b64encode(new_password.encode("utf-8")).decode("utf-8")

                cursor.execute("""
                    UPDATE [DMOX].[Account].[Account]
                    SET [Password] = ?
                    WHERE [DiscordId] = ?
                """, (encoded_new_password, discord_id))
                conn.commit()

            await ctx.send("✅ Your password has been successfully changed.")

        except Exception as e:
            await ctx.send(f"❌ Failed to update password: {str(e)}")

async def setup(bot):
    await bot.add_cog(ChangePasswordCog(bot))
