import discord
from discord.ext import commands, tasks
import psutil
import time
from dotenv import load_dotenv
import os
import platform

load_dotenv()
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

async def get_status_embed():
    uptime = time.time() - psutil.boot_time()
    uptime_str = f"{int(uptime // 86400)}d {int((uptime % 86400) // 3600)}h {int((uptime % 3600) // 60)}m"
    cpu_usage = psutil.cpu_percent()
    ram_usage = psutil.virtual_memory().percent
    disk_usage = psutil.disk_usage('/').percent
    ping = round(bot.latency * 1000)
   
    embed = discord.Embed(
        title="Statut de 7KOR",
        description="Informations",
        color=discord.Color.random()
    )
   
    embed.add_field(name="Uptime", value=uptime_str, inline=True)
    embed.add_field(name="CPU%", value=f"{cpu_usage}%", inline=True)
    embed.add_field(name="RAM%", value=f"{ram_usage}%", inline=True)
    embed.add_field(name="Disk%", value=f"{disk_usage}%", inline=True)
    embed.add_field(name="Ping", value=f"{ping}ms", inline=True)
    embed.add_field(name="OS", value=platform.system(), inline=True)
   
    embed.set_author(name=bot.user.name, icon_url=bot.user.avatar.url if bot.user.avatar else discord.Embed.Empty)
   
    embed.set_footer(text="Update toutes les 30mns")
   
    embed.timestamp = discord.utils.utcnow()
   
    embed.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/commons/thumb/3/35/Tux.svg/640px-Tux.svg.png")
    
    return embed

@bot.event
async def on_ready():
    print(f'{bot.user} est connecte')
    hourly_status.start()

@tasks.loop(minutes=30)
async def hourly_status():
    channel_id = int(os.getenv('LOGS_CHANNEL_ID'))
    guild_id = int(os.getenv('GUILD_ID'))
    
    guild = bot.get_guild(guild_id)
    if guild:
        channel = guild.get_channel(channel_id)
        if channel:
            embed = await get_status_embed()
            await channel.send(embed=embed)
        else:
            print(f"Pas trouve {channel_id}")
    else:
        print(f"Pas trouve{guild_id}")

@bot.command()
async def status(ctx):
    embed = await get_status_embed()
    await ctx.send(embed=embed)

# Get the token from the environment variable
token = os.getenv('DISCORD_BOT_TOKEN')
# Check if the token is available
if token is None:
    print("Erreur fichier .env")
else:
    bot.run(token)