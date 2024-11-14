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

# Your existing bot code...

app = Flask('')

@app.route('/')
def home():
    return "Bot is running!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# Start Flask in a thread
keep_alive()

# Run the bot
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.event
async def on_raw_reaction_add(payload):
    # Your existing on_raw_reaction_add code...

@bot.command(name="bam")
async def fake_ban(ctx, user: discord.Member, *, reason="for being too awesome!"):
    await ctx.send(f"🔨 BAM! {user.mention} has been fake-banned {reason}! 😂")

@bot.command(name="warm")
async def fake_warn(ctx, user: discord.Member, *, reason="for spreading too much joy!"):
    await ctx.send(f"⚠️ WARM! {user.mention} has been issued a fake warning {reason}! 🌞")

if __name__ == "__main__":
    keep_alive()
    bot.run(os.environ['TOKEN'])
