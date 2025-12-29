import discord
from discord.ext import commands
from db.database import get_connection
import base64
import asyncio

class DeleteAccountCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='deleteaccount')
    async def delete_account(self, ctx):
        if ctx.guild is not None:
            return  # Only allow in DMs

        discord_id = str(ctx.author.id)

        # Check if account exists
        try:
            with get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT 1 FROM [DMOX].[Account].[Account]
                    WHERE [DiscordId] = ?
                """, (discord_id,))
                if not cursor.fetchone():
                    await ctx.send("❌ You don't have an account to delete.")
                    return
        except Exception as e:
            await ctx.send(f"❌ Database error: {str(e)}")
            return

        await ctx.send("⚠️ Are you sure you want to delete your account? Type `Yes` or `No`. You have 10 seconds to reply.")

        def check_confirm(m):
            return (
                m.author == ctx.author and
                m.channel == ctx.channel and
                m.content.lower() in ['yes', 'y', 'no', 'n']
            )

        try:
            confirm_msg = await self.bot.wait_for("message", check=check_confirm, timeout=10)
        except asyncio.TimeoutError:
            await ctx.send("⌛ Deletion timed out. Cancelled.")
            return

        if confirm_msg.content.lower() not in ['yes', 'y']:
            await ctx.send("❎ Account deletion cancelled.")
            return

        await ctx.send("🔐 Okay, what's your password? (10 seconds to reply)")

        def check_password(m):
            return m.author == ctx.author and m.channel == ctx.channel

        try:
            password_msg = await self.bot.wait_for("message", check=check_password, timeout=10)
        except asyncio.TimeoutError:
            await ctx.send("⌛ Password input timed out. Cancelled.")
            return

        encoded_input_password = base64.b64encode(password_msg.content.encode("utf-8")).decode("utf-8")

        try:
            with get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT [Password] FROM [DMOX].[Account].[Account]
                    WHERE [DiscordId] = ?
                """, (discord_id,))
                row = cursor.fetchone()

                if not row:
                    await ctx.send("❌ Account not found.")
                    return

                stored_password = row.Password

                if stored_password != encoded_input_password:
                    await ctx.send("❌ Incorrect password. Deletion cancelled.")
                    return

                # Delete account
                cursor.execute("""
                    DELETE FROM [DMOX].[Account].[Account]
                    WHERE [DiscordId] = ?
                """, (discord_id,))
                conn.commit()

            await ctx.send("✅ Your account has been permanently deleted.")

        except Exception as e:
            await ctx.send(f"❌ Database error: {str(e)}")

# Required for discord.py v2
async def setup(bot):
    await bot.add_cog(DeleteAccountCog(bot))
