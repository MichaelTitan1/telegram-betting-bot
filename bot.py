import os
import requests
from apscheduler.schedulers.background import BackgroundScheduler
from telegram import Bot, Update
from telegram.ext import Updater, CommandHandler, CallbackContext
from datetime import datetime

# API keys (with the ones you provided)
SPORTS_API_KEY_1 = 'ddac830e88b36908d910d3a6243febe0'
SPORTS_API_KEY_2 = '9446479bb0f51557d3e219ad87d0823c0d3fbeb'
SPORTS_API_KEY_3 = '0d3fbebb6a0f480d882b6cbe6c94935b'
SPORTS_API_KEY_4 = 'SqhwD69YrioLN33CoBd10jQiXA44FFYdpfeKd0SKbRpq18uFPf8G0ZBAdN24'
TELEGRAM_API_TOKEN = '6073976909:AAHjxWe1Yp3T60w4FEUw0qMb4rqJvPztqM4'

# Telegram bot setup
bot = Bot(token=TELEGRAM_API_TOKEN)

# The bot will send messages to your Telegram chat or group after receiving the '/start' command
def start(update: Update, context: CallbackContext):
    update.message.reply_text("Hello! I am your sports betting bot. Type /get_bets to get today's best bets.")

# Fetch the sports betting data from the Sports API
def fetch_bets():
    try:
        url = f"https://api.sportsmonk.com/v1/bets?api_key={SPORTS_API_KEY_1}"
        response = requests.get(url)
        response.raise_for_status()  # Ensure we get a valid response
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None

# Format and send betting predictions to the Telegram chat
def send_bets(update: Update, context: CallbackContext):
    bets = fetch_bets()
    if bets:
        message = "Today's Best Bets:\n\n"
        for bet in bets:
            message += f"{bet['match']}: {bet['prediction']} - {bet['odds']}\n"
        update.message.reply_text(message)
    else:
        update.message.reply_text("Sorry, no bets found for today.")

# Schedule a daily job to fetch and send bets automatically at 6:00 AM (Nigeria time)
def schedule_daily_bets():
    scheduler = BackgroundScheduler(timezone="Africa/Lagos")
    scheduler.add_job(send_bets, 'interval', hours=24, start_date=datetime(2025, 4, 3, 6, 0, 0))
    scheduler.start()

# Create an updater and dispatcher for handling Telegram commands
updater = Updater(TELEGRAM_API_TOKEN, use_context=True)
dp = updater.dispatcher

# Add command handlers for the bot
dp.add_handler(CommandHandler('start', start))
dp.add_handler(CommandHandler('get_bets', send_bets))

# Start the scheduler for automatic bet sending
schedule_daily_bets()

# Start the bot
updater.start_polling()
updater.idle()
