import discord
from discord.ext import commands, tasks
import psutil
import time
import os
import platform
from dotenv import load_dotenv

load_dotenv()
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

def get_status_embed():
    uptime = time.time() - psutil.boot_time()
    uptime_str = f"{int(uptime // 86400)}d {int((uptime % 86400) // 3600)}h {int((uptime % 3600) // 60)}m"
    
    embed = discord.Embed(title="Statut de 7KOR", color=discord.Color.random())
    
    fields = [
        ("Uptime", uptime_str),
        ("CPU%", f"{psutil.cpu_percent()}%"),
        ("RAM%", f"{psutil.virtual_memory().percent}%"),
        ("Disk%", f"{psutil.disk_usage('/').percent}%"),
        ("Ping", f"{round(bot.latency * 1000)}ms"),
        ("OS", platform.system())
    ]
    
    for name, value in fields:
        embed.add_field(name=name, value=value, inline=True)
    
    embed.set_author(name=bot.user.name, icon_url=bot.user.avatar.url if bot.user.avatar else None)
    embed.set_footer(text="Update toutes les 30mns")
    embed.timestamp = discord.utils.utcnow()
    embed.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/commons/thumb/3/35/Tux.svg/640px-Tux.svg.png")
    
    return embed

@bot.event
async def on_ready():
    print(f'{bot.user} est connecté')
    hourly_status.start()

@tasks.loop(minutes=30)
async def hourly_status():
    channel_id = int(os.getenv('LOGS_CHANNEL_ID'))
    guild = bot.get_guild(int(os.getenv('GUILD_ID')))
    if guild:
        if channel := guild.get_channel(channel_id):
            await channel.send(embed=get_status_embed())
        else:
            print(f"Canal {channel_id} non trouvé")
    else:
        print(f"Serveur {os.getenv('GUILD_ID')} non trouvé")

@bot.command()
async def status(ctx):
    await ctx.send(embed=get_status_embed())

if token := os.getenv('DISCORD_BOT_TOKEN'):
    bot.run(token)
else:
    print("Erreur : Token non trouvé dans le fichier .env")