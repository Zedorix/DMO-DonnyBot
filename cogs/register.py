import discord
from discord.ext import commands
import datetime
import base64
from db.database import get_connection  # ✅ Import the modular DB connection

class RegisterCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='register')
    async def register(self, ctx, username: str = None, raw_password: str = None):
        if ctx.guild is not None:
            return  # Only allow in DM

        if not username or not raw_password:
            await ctx.send("❌ Usage: `!register Username Password`")
            return

        encoded_password = base64.b64encode(raw_password.encode("utf-8")).decode("utf-8")
        discord_id = str(ctx.author.id)
        email = f"{username}@digimon.com"

        try:
            with get_connection() as conn:  # ✅ Use the modular DB connection
                cursor = conn.cursor()

                # Check Discord ID
                cursor.execute("""
                    SELECT 1 FROM [DMOX].[Account].[Account]
                    WHERE [DiscordId] = ?
                """, (discord_id,))
                if cursor.fetchone():
                    await ctx.send("⚠️ You already have an account registered with this Discord ID.")
                    return

                # Check Username
                cursor.execute("""
                    SELECT 1 FROM [DMOX].[Account].[Account]
                    WHERE [Username] = ?
                """, (username,))
                if cursor.fetchone():
                    await ctx.send("⚠️ That username is already taken.")
                    return

                # Insert account
                now = datetime.datetime.now()
                cursor.execute("""
                    INSERT INTO [DMOX].[Account].[Account]
                        ([Username], [Password], [Email], [AccessLevel], [CreateDate],
                         [Premium], [Silk], [ReceiveWelcome], [DiscordId])
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    username, encoded_password, email,
                    0, now,
                    0, 0, 1,
                    discord_id
                ))
                conn.commit()

            await ctx.send(f"✅ Account created!\nUsername: `{username}`\nEmail: `{email}`")

        except Exception as e:
            await ctx.send(f"❌ Database error: {str(e)}")
            
async def setup(bot):
    await bot.add_cog(RegisterCog(bot))
