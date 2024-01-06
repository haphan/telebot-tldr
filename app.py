import asyncio
import os
from contextlib import asynccontextmanager

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI
from telebot.async_telebot import AsyncTeleBot
from telebot.types import Message

from crawler import readability_text
from llm import summarize_article, hashtags_tokenization, adsometer
from utils import is_url, create_logger

load_dotenv()

# Replace with your bot token
bot_token = os.getenv('TELEGRAM_BOT_TOKEN')

# Replace with the discussion group ID
discussion_grp_id = os.getenv('TELEGRAM_GROUP_ID')

bot = AsyncTeleBot(bot_token, parse_mode=None)

logger = create_logger()


@bot.message_handler(func=lambda m: m.chat.id == int(discussion_grp_id))
async def start(message: Message):
    """ Handling message post to chat group"""
    if not is_url(message.text):
        return

    article_url = message.text

    logger.info(f'Processing article: {article_url}')

    article_text = readability_text(article_url)
    summary = summarize_article(article_text)
    tags = hashtags_tokenization(article_text)
    ads = adsometer(article_text)

    reply = f"""
{summary}

Tags: {tags}
Ads-o-meter: {ads}
Tóm tắt bởi Google Gemini Pro
    """
    await bot.reply_to(message, reply)


@asynccontextmanager
async def lifespan(app: FastAPI):
    asyncio.create_task(bot.polling(non_stop=True, timeout=60, interval=2))
    yield


app = FastAPI(lifespan=lifespan)


@app.get('/_healthz')
@app.get('/')
async def heathcheck():
    return 'OK!'


if __name__ == '__main__':
    logger.info('Bot started!')
    uvicorn.run(app)
