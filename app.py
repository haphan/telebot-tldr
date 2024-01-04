import os

import telebot
from dotenv import load_dotenv
from telebot.types import Message

from crawler import readability_text
from llm import summarize_article, hashtags_tokenization, adsometer
from utils import is_url, create_logger

load_dotenv()

# Replace with your bot token
bot_token = os.getenv('TELEGRAM_BOT_TOKEN')

# Replace with the discussion group ID
discussion_grp_id = os.getenv('TELEGRAM_GROUP_ID')

bot = telebot.TeleBot(bot_token, parse_mode=None)

logger = create_logger()


@bot.message_handler(func=lambda m: m.chat.id == int(discussion_grp_id))
def start(message: Message):
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
    """
    bot.reply_to(message, reply)


if __name__ == "__main__":

    bot.polling()
