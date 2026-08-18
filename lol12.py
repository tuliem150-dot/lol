import os
import discord
from discord.ext import commands
from openai import OpenAI
from dotenv import load_dotenv

# Tải các biến môi trường từ file .env
load_dotenv()

# Lấy Key & Token từ file .env ra
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

MODEL_NAME = "google/gemma-2-27b-it"

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY
)

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'Bot đã hoạt động với tên: {bot.user}')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    async with message.channel.typing():
        try:
            response = client.chat.completions.create(
                model=MODEL_NAME,
                messages=[
                    {"role": "system", "content": "Bạn là một trợ lý AI thân thiện trên Discord."},
                    {"role": "user", "content": message.content}
                ]
            )
            
            reply_text = response.choices[0].message.content

            if len(reply_text) > 2000:
                for i in range(0, len(reply_text), 1900):
                    await message.reply(reply_text[i:i+1900])
            else:
                await message.reply(reply_text)

        except Exception as e:
            await message.reply(f"Đã có lỗi xảy ra: {e}")

    await bot.process_commands(message)

bot.run(DISCORD_TOKEN)