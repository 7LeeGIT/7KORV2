import discord
from discord.ext import commands, tasks
import psutil
import time
import os
import platform
import sys

class ControlButtons(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        """Vérifie si l'utilisateur a la permission d'utiliser les boutons"""
        try:
            authorized_kor = int(os.getenv('AUTHORIZED_KOR'))
            authorized_lee = int(os.getenv('AUTHORIZED_LEE'))
        except (ValueError, TypeError):
            print("Erreur : IDs d'utilisateurs invalides dans les variables d'environnement")
            return False
        
        if interaction.user.id not in [authorized_kor, authorized_lee]:
            await interaction.response.send_message(
                "❌ Vous n'avez pas la permission d'utiliser ces contrôles.", 
                ephemeral=True
            )
            return False
        return True

    @discord.ui.button(label="🔄 Redémarrer", style=discord.ButtonStyle.primary, custom_id="restart_bot")
    async def restart_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(
            f"🔄 Redémarrage du bot initié par {interaction.user.display_name}...", 
            ephemeral=True
        )
        os.execv(sys.executable, ['python'] + sys.argv)

class StatusManager:
    def __init__(self, bot):
        self.bot = bot
        self.last_status_message = None

    def get_status_embed(self):
        """Crée l'embed avec les informations de statut"""
        uptime = time.time() - psutil.boot_time()
        uptime_str = f"{int(uptime // 86400)}j {int((uptime % 86400) // 3600)}h {int((uptime % 3600) // 60)}m"
        
        process = psutil.Process()
        bot_uptime = time.time() - process.create_time()
        bot_uptime_str = f"{int(bot_uptime // 86400)}j {int((bot_uptime % 86400) // 3600)}h {int((bot_uptime % 3600) // 60)}m"
        
        embed = discord.Embed(title="📊 Statut de 7KOR", color=discord.Color.random())
        
        main_stats = [
            ("⏰ Uptime Système", uptime_str),
            ("🤖 Uptime Bot", bot_uptime_str),
            ("📡 Ping", f"{round(self.bot.latency * 1000)}ms"),
            ("💻 CPU Usage", f"{psutil.cpu_percent()}%"),
            ("📝 RAM Usage", f"{psutil.virtual_memory().percent}%"),
            ("🖥️ OS de KOR", f"{platform.system()} {platform.release()}")
        ]
        
        for name, value in main_stats:
            embed.add_field(name=name, value=value, inline=True)
        
        embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar.url if self.bot.user.avatar else None)
        embed.set_footer(text="Mise à jour toutes les 45 minutes")
        embed.timestamp = discord.utils.utcnow()
        embed.set_thumbnail(url="https://media.discordapp.net/attachments/1040759817385562182/1298551346194284547/Fils.gif?ex=6719f9ae&is=6718a82e&hm=4fb322fd39a3d1c24ac4142f86dbd60cb22619215743f7d08cc4615fd36c7666&=&width=670&height=670")
        
        return embed

    @tasks.loop(minutes=45)
    async def update_status(self):
        """Met à jour le message de statut toutes les 45 minutes"""
        try:
            channel_id = int(os.getenv('LOGS_CHANNEL_ID'))
            guild = self.bot.get_guild(int(os.getenv('GUILD_ID')))
            
            if guild:
                if channel := guild.get_channel(channel_id):
                    # Suppression du dernier message s'il existe
                    try:
                        if self.last_status_message:
                            await self.last_status_message.delete()
                    except discord.NotFound:
                        pass  # Le message a déjà été supprimé
                    except discord.HTTPException as e:
                        print(f"Erreur lors de la suppression du message : {e}")
                    
                    # Envoi du nouveau message
                    self.last_status_message = await channel.send(
                        embed=self.get_status_embed(),
                        view=ControlButtons()
                    )
                else:
                    print(f"Canal {channel_id} non trouvé")
            else:
                print(f"Serveur {os.getenv('GUILD_ID')} non trouvé")
        except Exception as e:
            print(f"Erreur lors de la mise à jour du statut : {e}")

    @update_status.before_loop
    async def before_update_status(self):
        """Attend que le bot soit prêt avant de démarrer la tâche"""
        await self.bot.wait_until_ready()

async def setup(bot):
    """Initialise le module de logs"""
    status_manager = StatusManager(bot)
    status_manager.update_status.start()  # La tâche démarrera et enverra son premier message
    bot.add_view(ControlButtons())