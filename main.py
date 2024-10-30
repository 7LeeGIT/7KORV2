import discord
from discord.ext import tasks
from datetime import datetime, time
import pytz
import os

class CountdownManager:
    def __init__(self, bot):
        self.bot = bot
        self.target_date = datetime(2024, 12, 22)
        self.channel_id = int(os.getenv('COUNTDOWN_CHANNEL_ID'))
        self.daily_time = time(hour=7, minute=7)
        self.timezone = pytz.timezone('Europe/Paris')
        
    def get_days_remaining(self):
        now = datetime.now(self.timezone)
        delta = self.target_date - now.replace(tzinfo=None)
        return max(0, delta.days)

    @tasks.loop(time=time(hour=7, minute=7))
    async def daily_countdown(self):
        channel = self.bot.get_channel(self.channel_id)
        if not channel:
            return

        days_left = self.get_days_remaining()
        
        if days_left == 0:
            message = "🎉 **JOUR J** 🎉\n<@_kor> Le grand jour est arrivé !"
        else:
            message = f"⏰ **Countdown**\nPlus que {days_left} jours avant le 22 décembre 2024 !"
            
        await channel.send(message)

    @daily_countdown.before_loop
    async def before_countdown(self):
        await self.bot.wait_until_ready()

async def setup(bot):
    countdown_manager = CountdownManager(bot)
    countdown_manager.daily_countdown.start()