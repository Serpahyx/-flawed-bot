import os
import discord
from discord.ext import commands
from flask import Flask
from threading import Thread

# Set up the bot with the appropriate intents
intents = discord.Intents.default()
intents.message_content = True
intents.reactions = True

bot = commands.Bot(command_prefix="*", intents=intents)

# Replace these with your actual channel IDs for the skull board and sob board
SKULL_BOARD_CHANNEL_ID = 1306026103114039336  # Replace with your skull board channel ID
SOB_BOARD_CHANNEL_ID = 1306026103114039336    # Replace with your sob board channel ID

# Thresholds for reactions
SKULL_REACTION_THRESHOLD = 3
SOB_REACTION_THRESHOLD = 3

# Emojis to trigger skull and sob boards
SKULL_EMOJI = "💀"
SOB_EMOJI = "😭"

# To store message IDs of skull and sob posts
reaction_boards = {}  # format: {original_message_id: {'skull': embed_message_id, 'sob': embed_message_id}}

# Custom status configuration
STATUS_TYPE = "idle"  # Options: 'online', 'offline', 'idle', 'dnd'
ACTIVITY_TYPE = "streaming"  # Options: 'playing', 'streaming', 'listening', 'watching'
ACTIVITY_TEXT = "/flawed on top"  # Text for the status message

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

    # Set the bot's status type
    status = {
        "online": discord.Status.online,
        "offline": discord.Status.offline,
        "idle": discord.Status.idle,
        "dnd": discord.Status.dnd
    }.get(STATUS_TYPE.lower(), discord.Status.online)

    # Set the bot's activity type
    activity = {
        "playing": discord.Game(ACTIVITY_TEXT),
        "streaming": discord.Streaming(name=ACTIVITY_TEXT, url="https://twitch.tv/yourchannel"),  # Update with a valid URL if streaming
        "listening": discord.Activity(type=discord.ActivityType.listening, name=ACTIVITY_TEXT),
        "watching": discord.Activity(type=discord.ActivityType.watching, name=ACTIVITY_TEXT)
    }.get(ACTIVITY_TYPE.lower(), discord.Game(ACTIVITY_TEXT))

    await bot.change_presence(status=status, activity=activity)

@bot.event
async def on_raw_reaction_add(payload):
    try:
        # Get the guild (server) and channel
        guild = bot.get_guild(payload.guild_id)
        channel = bot.get_channel(payload.channel_id)

        # Fetch message, with error handling if it fails
        message = await channel.fetch_message(payload.message_id)

        # Ignore bot messages
        if message.author.bot:
            return

        # Check reactions for Skull and Sob boards
        skull_reaction = discord.utils.get(message.reactions, emoji=SKULL_EMOJI)
        sob_reaction = discord.utils.get(message.reactions, emoji=SOB_EMOJI)

        # Skull Board logic
        if skull_reaction and skull_reaction.count >= SKULL_REACTION_THRESHOLD:
            skull_channel = bot.get_channel(SKULL_BOARD_CHANNEL_ID)
            await update_or_create_embed(
                skull_channel, 
                message, 
                skull_reaction.count, 
                'skull'
            )

        # Sob Board logic
        if sob_reaction and sob_reaction.count >= SOB_REACTION_THRESHOLD:
            sob_channel = bot.get_channel(SOB_BOARD_CHANNEL_ID)
            await update_or_create_embed(
                sob_channel, 
                message, 
                sob_reaction.count, 
                'sob'
            )

    except discord.errors.NotFound:
        print("Error: Message not found.")
    except discord.errors.Forbidden:
        print("Error: Missing permissions to fetch message.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

async def update_or_create_embed(channel, original_message, reaction_count, board_type):
    # Check if this message already has an embed in the board
    embed_message_id = reaction_boards.get(original_message.id, {}).get(board_type)
    color = discord.Color.red() if board_type == 'skull' else discord.Color.blue()
    emoji = SKULL_EMOJI if board_type == 'skull' else SOB_EMOJI

    # If an embed already exists, update it
    if embed_message_id:
        embed_message = await channel.fetch_message(embed_message_id)
        embed = embed_message.embeds[0]
        embed.set_field_at(0, name=f"{emoji} Reactions", value=f"{reaction_count}", inline=False)
        await embed_message.edit(embed=embed)
    else:
        # Otherwise, create a new embed
        embed = discord.Embed(description=original_message.content, color=color)
        embed.set_author(name=original_message.author.display_name, icon_url=original_message.author.avatar.url)
        embed.add_field(name=f"{emoji} Reactions", value=f"{reaction_count}", inline=False)
        embed.add_field(name="Original Message", value=f"[Jump to message]({original_message.jump_url})")
        embed.set_footer(text=f"Message ID: {original_message.id}")

        embed_message = await channel.send(embed=embed)

        # Store the embed message ID for future updates
        if original_message.id not in reaction_boards:
            reaction_boards[original_message.id] = {}
        reaction_boards[original_message.id][board_type] = embed_message.id

# Fake "bam" (ban) command
@bot.command(name="bam")
async def fake_ban(ctx, user: discord.Member, *, reason="for being too awesome!"):
    await ctx.send(f"🔨 BAM! {user.mention} has been fake-banned {reason}! 😂")

# Fake "warm" (warn) command
@bot.command(name="warm")
async def fake_warn(ctx, user: discord.Member, *, reason="for spreading too much joy!"):
    await ctx.send(f"⚠️ WARM! {user.mention} has been issued a fake warning {reason}! 🌞")



# Keep alive


app = Flask('')

@app.route('/')
def home():
    return "Bot is running!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# start
keep_alive()
bot.run("MTMwNjM3OTkzODA5NzY2NDA3MA.GMcEKB.zUkPNMH6lXJVcRfiEQpa5ZY7duzOnYGWx-NYCc")
