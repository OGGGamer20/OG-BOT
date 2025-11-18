import discord
from discord.ext import commands, tasks
import os

TOKEN = os.getenv("BOT_TOKEN")

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# ===== Ticket System =====
@bot.command()
async def ticket(ctx):
    guild = ctx.guild
    overwrites = {
        guild.default_role: discord.PermissionOverwrite(read_messages=False),
        ctx.author: discord.PermissionOverwrite(read_messages=True)
    }
    channel = await guild.create_text_channel(f"ticket-{ctx.author.name}", overwrites=overwrites)
    await ctx.send(f"🎫 Ticket created: {channel.mention}")

# ===== Invite Tracker =====
invites_before = {}

@bot.event
async def on_ready():
    global invites_before
    for guild in bot.guilds:
        invites_before[guild.id] = await guild.invites()
    status_task.start()
    print("Bot is ready!")

@bot.event
async def on_member_join(member):
    invites_after = await member.guild.invites()
    before = invites_before[member.guild.id]
    for invite in invites_after:
        for old in before:
            if invite.code == old.code and invite.uses > old.uses:
                channel = discord.utils.get(member.guild.text_channels, name="general")
                if channel:
                    await channel.send(f"📥 {member.mention} joined using {invite.inviter}'s invite!")
                break
    invites_before[member.guild.id] = invites_after

# ===== Minecraft Status (Dummy Example) =====
@tasks.loop(seconds=30)
async def status_task():
    await bot.change_presence(activity=discord.Game("Managing Server 🚀"))

# ===== Start =====
bot.run(TOKEN)
