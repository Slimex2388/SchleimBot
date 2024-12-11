import discord
from discord.ext import commands, tasks
import googleapiclient.discovery
import googleapiclient.errors
import os
import time

# Setze den YouTube API Key und den Discord Bot Token
YOUTUBE_API_KEY = "DEIN_YOUTUBE_API_KEY"
CHANNEL_ID = "DEIN_YOUTUBE_CHANNEL_ID"
DISCORD_TOKEN = "DEIN_DISCORD_BOT_TOKEN"
GUILD_ID = "DEIN_GUILD_ID"  # Optional: für den spezifischen Server

# Discord Bot Setup
intents = discord.Intents.default()
intents.messages = True  # Aktiviert den Empfang von Nachrichten
bot = commands.Bot(command_prefix="!", intents=intents)

# Channel ID für den Discord Channel, in den Nachrichten gesendet werden sollen
CHANNEL_ID_DISCORD = 123456789012345678  # Beispiel Channel-ID (ersetze durch deine eigene)

# YouTube API Setup
def youtube_api():
    """Erstellt den YouTube API Client"""
    youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=YOUTUBE_API_KEY)
    return youtube

# Überprüfe auf neue Videos
def get_latest_video():
    """Hole das neueste Video des Kanals"""
    youtube = youtube_api()
    request = youtube.search().list(
        part="snippet",
        channelId=CHANNEL_ID,
        order="date",
        maxResults=1
    )
    response = request.execute()
    return response["items"][0]["snippet"]["resourceId"]["videoId"]

# Discord Bot Command: /troll
@bot.command()
async def troll(ctx):
    """Spammt den YouTube Kanal 10 mal und abonniert den Kanal"""
    for _ in range(10):
        await ctx.send(f"Schaut euch meinen YouTube-Kanal an: https://www.youtube.com/channel/{CHANNEL_ID}")
        time.sleep(1)  # Eine Sekunde warten, um Spam zu kontrollieren
    await ctx.send("Ich habe den Kanal 10-mal gepostet. Jetzt abonniere ich...")

    # Hier könntest du eine echte Subscription-Logik einbauen,
    # aber da der Bot keine YouTube-API nutzt, wird diese Zeile nur ein "Abonnieren"-Text senden.
    await ctx.send(f"Ich habe jetzt den Kanal abonniert: https://www.youtube.com/channel/{CHANNEL_ID}")

# Task, um regelmäßig nach neuen Videos zu prüfen und Benachrichtigungen zu senden
@tasks.loop(minutes=10)
async def check_new_video():
    """Überprüft alle 10 Minuten auf ein neues Video und sendet eine Nachricht im Discord Channel"""
    latest_video_id = get_latest_video()
    latest_video_url = f"https://www.youtube.com/watch?v={latest_video_id}"

    channel = bot.get_channel(CHANNEL_ID_DISCORD)
    await channel.send(f"Neues Video von meinem Kanal: {latest_video_url}")

# Starten der Periodischen Aufgabe
@bot.event
async def on_ready():
    """Wird aufgerufen, wenn der Bot startet und sich erfolgreich verbindet"""
    print(f"Bot ist eingeloggt als {bot.user}")
    check_new_video.start()

# Bot starten
bot.run(DISCORD_TOKEN)
