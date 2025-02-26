from django import template
import re

register = template.Library()

@register.filter
def youtube_embed(url):
    """ Преобразует YouTube URL в формат для iframe """
    if not url:
        return ""
    match = re.search(r"(?:https?:\/\/)?(?:www\.)?(?:youtube\.com\/(?:watch\?v=|embed\/)|youtu\.be\/)([\w-]+)", url)
    if match:
        video_id = match.group(1)
        return f"https://www.youtube.com/embed/{video_id}"
    return url  # Если URL не соответствует YouTube, оставить его как есть
