# embed.py
import discord
import re

async def fix_social_links(message):
    try:
        # Patterns pour détecter les liens
        twitter_pattern = r'https?://(?:www\.)?(?:twitter\.com|x\.com)/([a-zA-Z0-9_]+/status/[0-9]+)'
        instagram_pattern = r'https?://(?:www\.)?instagram\.com/(?:p|reel)/([a-zA-Z0-9_-]+)'
        tiktok_pattern = r'https?://(?:www\.)?tiktok\.com/(@[^/]+/video/[0-9]+)'

        # Fonction pour remplacer les liens
        content = message.content
        
        # Fix Twitter/X
        if re.search(twitter_pattern, content):
            content = re.sub(twitter_pattern, r'https://vxtwitter.com/\1', content)
        
        # Fix Instagram
        if re.search(instagram_pattern, content):
            content = re.sub(instagram_pattern, r'https://ddinstagram.com/p/\1', content)
        
        # Fix TikTok
        if re.search(tiktok_pattern, content):
            content = re.sub(tiktok_pattern, r'https://vxtiktok.com/\1', content)

        # Si le contenu a été modifié, envoyer le nouveau message
        if content != message.content:
            await message.delete()
            await message.channel.send(content)
            
    except Exception as e:
        print(f"Erreur dans fix_social_link: {e}")