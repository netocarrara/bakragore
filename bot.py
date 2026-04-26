import asyncio
import logging
import os
import tempfile
from typing import Optional

import discord
from discord import FFmpegPCMAudio
from discord.ext import commands
from dotenv import load_dotenv
from gtts import gTTS

load_dotenv()
TOKEN = os.getenv("DISCORD_BOT_TOKEN")
if not TOKEN:
    raise SystemExit("ERRO: defina DISCORD_BOT_TOKEN em .env ou na variável de ambiente.")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s:%(name)s: %(message)s",
)

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)
mechanic_task: Optional[asyncio.Task] = None


def gerar_audio_arquivo(texto: str) -> str:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_file:
        caminho = temp_file.name

    tts = gTTS(text=texto, lang="pt")
    tts.save(caminho)
    return caminho


async def gerar_audio(texto: str) -> str:
    return await asyncio.to_thread(gerar_audio_arquivo, texto)


async def tocar_audio(voice_client: discord.VoiceClient, texto: str) -> None:
    arquivo = await gerar_audio(texto)
    try:
        source = FFmpegPCMAudio(arquivo)
        voice_client.play(source)
        while voice_client.is_playing():
            await asyncio.sleep(0.5)
    finally:
        try:
            os.remove(arquivo)
        except OSError:
            pass


async def join_voice_channel(ctx: commands.Context) -> Optional[discord.VoiceClient]:
    if not ctx.author.voice or not ctx.author.voice.channel:
        await ctx.send("❌ Você não está em um canal de voz.")
        return None

    canal = ctx.author.voice.channel
    if ctx.voice_client:
        if ctx.voice_client.channel.id == canal.id:
            return ctx.voice_client
        return await ctx.voice_client.move_to(canal)

    return await canal.connect()


@bot.event
async def on_ready():
    print(f"Bot conectado como {bot.user}")


@bot.command(name="entrar")
async def entrar(ctx: commands.Context) -> None:
    voice_client = await join_voice_channel(ctx)
    if voice_client:
        await ctx.send("✅ Entrei na call!")


async def _mecanica_loop(ctx: commands.Context) -> None:
    global mechanic_task
    try:
        await ctx.send("🔄 Loop da mecânica iniciado (1:30).")

        while True:
            await asyncio.sleep(90)

            if not ctx.voice_client or not ctx.voice_client.is_connected():
                await ctx.send("❌ Perdi a conexão com o canal de voz.")
                break

            await ctx.send("⚠️ Mecânica em 5 segundos!")
            await tocar_audio(ctx.voice_client, "Mecânica em cinco segundos")

            for n in (3, 2, 1):
                await ctx.send(f"⏳ {n}")
                await tocar_audio(ctx.voice_client, str(n))

            await ctx.send("⚡ Hora da mecânica! ⚡")
            await tocar_audio(ctx.voice_client, "Hora da mecânica!")
    except asyncio.CancelledError:
        await ctx.send("🛑 Loop da mecânica cancelado.")
        raise
    except Exception as error:
        logging.exception("Erro no loop da mecânica")
        await ctx.send("❌ Ocorreu um erro no loop da mecânica.")
    finally:
        mechanic_task = None


@bot.command(name="mecanica")
async def mecanica(ctx: commands.Context) -> None:
    global mechanic_task
    if mechanic_task and not mechanic_task.done():
        await ctx.send("⚠️ O loop já está em execução.")
        return

    voice_client = await join_voice_channel(ctx)
    if not voice_client:
        return

    mechanic_task = bot.loop.create_task(_mecanica_loop(ctx))


@bot.command(name="parar")
async def parar(ctx: commands.Context) -> None:
    global mechanic_task
    if mechanic_task and not mechanic_task.done():
        mechanic_task.cancel()
        try:
            await mechanic_task
        except asyncio.CancelledError:
            pass
        await ctx.send("🛑 Loop da mecânica parado.")
    else:
        await ctx.send("⚠️ O loop já está parado.")

    if ctx.voice_client:
        await ctx.voice_client.disconnect()


@bot.command(name="sair")
async def sair(ctx: commands.Context) -> None:
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.send("👋 Saí do canal de voz.")
    else:
        await ctx.send("⚠️ Eu não estou em um canal de voz.")


if __name__ == "__main__":
    bot.run(TOKEN)
