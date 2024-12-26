import discord
from discord.ext import commands
from discord import app_commands
import os
import sys
from dotenv import load_dotenv
import logs
import embed

# Chargement des variables d'environnement
load_dotenv()

# Liste des variables d'environnement requises
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

# Commandes Slash
@bot.tree.command(name="badge", description="Display KOR badge")
async def badge(interaction: discord.Interaction):
    """Simple command that displays KOR"""
    await interaction.response.send_message("KOR")

# Événements
@bot.event
async def on_ready():
    """Événement déclenché quand le bot est prêt"""
    print(f'{bot.user} est connecté')
    
    # Définir le statut du bot
    await bot.change_presence(activity=discord.Activity(
        type=discord.ActivityType.listening,
        name="Subwoofer Lullaby - C418"
    ))
    
    # Synchroniser les commandes slash
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(f"Failed to sync commands: {e}")
    
    # Initialisation du module de logs
    await logs.setup(bot)

@bot.event
async def on_message(message):
    """Événement déclenché à chaque message"""
    # Ignore les messages du bot
    if message.author.bot:
        return
    
    # Vérifie et corrige les liens sociaux
    await embed.fix_social_links(message)
    
    # Traite les commandes normalement
    await bot.process_commands(message)

# Gestion des erreurs
@bot.event
async def on_command_error(ctx, error):
    """Gestionnaire d'erreurs global pour les commandes"""
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("❌ Commande non trouvée.")
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send("❌ Vous n'avez pas les permissions nécessaires.")
    else:
        print(f"Erreur non gérée : {error}")

# Point d'entrée principal
def main():
    """Fonction principale pour démarrer le bot"""
    token = os.getenv('DISCORD_BOT_TOKEN')
    if not token:
        print("Erreur : Token Discord non trouvé dans le fichier .env")
        sys.exit(1)
    
    try:
        bot.run(token)
    except discord.LoginFailure:
        print("Erreur : Impossible de se connecter. Vérifiez votre token.")
    except Exception as e:
        print(f"Erreur lors du démarrage du bot : {e}")

if __name__ == "__main__":
    main()
