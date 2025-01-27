import discord
import re

async def fix_social_links(message):
    try:
        # Patterns pour détecter les liens
        twitter_pattern = r'https?://(?:www\.)?(?:twitter\.com|x\.com)/([a-zA-Z0-9_]+/status/[0-9]+)'
        instagram_pattern = r'https?://(?:www\.)?instagram\.com/(?:p|reel)/([a-zA-Z0-9_-]+)'
        tiktok_pattern = r'https?://(?:www\.|vm\.)?tiktok\.com/(?:@[^/]+/video/[0-9]+|[A-Za-z0-9]+/?)'
        reddit_pattern = r'https?://(?:www\.)?reddit\.com(/r/[^/]+/comments/[a-zA-Z0-9]+/[^/?]+(?:\?[^/\s]*)?)'

        content = message.content

        # Fix Twitter/X
        if re.search(twitter_pattern, content):
            content = re.sub(twitter_pattern, r'https://vxtwitter.com/\1', content)

        # Fix Instagram
        if re.search(instagram_pattern, content):
            content = re.sub(instagram_pattern, r'https://ddinstagram.com/p/\1', content)

        # Fix TikTok
        if re.search(tiktok_pattern, content):
            tiktok_matches = re.finditer(tiktok_pattern, content)
            for match in tiktok_matches:
                original_url = match.group(0)
                fixed_url = original_url.replace('tiktok.com', 'tnktok.com')
                content = content.replace(original_url, fixed_url)

        # Fix Reddit
        if re.search(reddit_pattern, content):
            content = re.sub(reddit_pattern, r'https://www.rxddit.com\1', content)

        if content != message.content:
            await message.delete()
            formatted_message = f"Envoyé par {message.author.mention} :\n{content}"
            await message.channel.send(formatted_message)

    except Exception as e:
        print(f"Erreur dans fix_social_links: {e}")