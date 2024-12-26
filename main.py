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

# Configuration du bot avec tous les intents nécessaires
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

class Bot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix='!', intents=intents)
        
    async def setup_hook(self):
        print("Setting up bot...")
        await self.tree.sync()
        print("Slash commands synced!")

bot = Bot()

@bot.tree.command(name="badge", description="Affiche KOR")
@app_commands.guild_only()
async def badge(interaction: discord.Interaction):
    """Commande qui affiche KOR"""
    try:
        await interaction.response.send_message("KOR")
        print(f"Badge command used by {interaction.user}")
    except Exception as e:
        print(f"Error in badge command: {e}")
        await interaction.response.send_message("Une erreur s'est produite.", ephemeral=True)

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
        print("Starting command sync...")
        await bot.tree.sync()
        print("Commands synced successfully!")
    except Exception as e:
        print(f"Failed to sync commands: {e}")
    
    # Initialisation du module de logs
    await logs.setup(bot)
    
    # Afficher les guilds où le bot est présent
    print("Connected to guilds:")
    for guild in bot.guilds:
        print(f"- {guild.name} (ID: {guild.id})")

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
        print("Starting bot...")
        bot.run(token)
    except discord.LoginFailure:
        print("Erreur : Impossible de se connecter. Vérifiez votre token.")
    except Exception as e:
        print(f"Erreur lors du démarrage du bot : {e}")

if __name__ == "__main__":
    main()
