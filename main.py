import discord
from discord.ext import commands
import os
import sys
from dotenv import load_dotenv
import logs

# Chargement des variables d'environnement
load_dotenv()

# Vérification des variables d'environnement requises
required_env_vars = [
    'DISCORD_BOT_TOKEN', 
    'LOGS_CHANNEL_ID', 
    'GUILD_ID', 
    'AUTHORIZED_KOR', 
    'AUTHORIZED_LEE'
]

# Vérification des variables d'environnement
missing_vars = [var for var in required_env_vars if not os.getenv(var)]
if missing_vars:
    print(f"Erreur : Variables d'environnement manquantes : {', '.join(missing_vars)}")
    sys.exit(1)

# Configuration du bot
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    """Événement déclenché quand le bot est prêt"""
    print(f'{bot.user} est connecté')
    await bot.change_presence(activity=discord.Activity(
        type=discord.ActivityType.watching,
        name="7KOR mourir..."
    ))
    
    # Initialisation du module de logs une fois que le bot est prêt
    await logs.setup(bot)

if __name__ == "__main__":
    token = os.getenv('DISCORD_BOT_TOKEN')
    if token:
        bot.run(token)
    else:
        print("Erreur : Token Discord non trouvé dans le fichier .env")