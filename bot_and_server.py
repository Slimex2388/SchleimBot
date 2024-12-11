import discord
import asyncio

# Discord-Bot-Token (ersetze mit deinem Token)
TOKEN = "DEIN_DISCORD_BOT_TOKEN"

# Channel-ID, in den der Bot die Nachrichten senden soll (ersetze mit deiner Channel-ID)
CHANNEL_ID = 123456789012345678

# Discord-Bot-Client
intents = discord.Intents.default()
intents.messages = True  # Erlaubt dem Bot, Nachrichten zu lesen und zu senden
client = discord.Client(intents=intents)

async def send_console_messages():
    await client.wait_until_ready()
    channel = client.get_channel(CHANNEL_ID)

    if not channel:
        print(f"Fehler: Channel mit der ID {CHANNEL_ID} wurde nicht gefunden.")
        return

    print("Schreibe eine Nachricht in die Konsole, die der Bot im Chat senden soll:")
    while True:
        message = input("> ")  # Liest Nachricht aus der Konsole
        if message.lower() in ["exit", "quit"]:  # Beenden mit "exit" oder "quit"
            print("Bot wird gestoppt...")
            await client.close()
            break
        await channel.send(message)  # Nachricht in Discord senden

@client.event
async def on_ready():
    print(f"Bot ist bereit und eingeloggt als {client.user}!")

# Hintergrund-Task starten
client.loop.create_task(send_console_messages())

# Bot starten
client.run(TOKEN)
