import logging
import random
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from textblob import TextBlob

# Set up logging for the bot
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize the ChatterBot (an AI chatbot engine)
chatbot = ChatBot('SocialBot', storage_adapter='chatterbot.storage.SQLStorageAdapter',
                  database_uri='sqlite:///database.db')

# Train the bot with ChatterBot Corpus
trainer = ChatterBotCorpusTrainer(chatbot)
trainer.train('chatterbot.corpus.english')

# Define slang and human-like responses
slang_responses = [
    "Yaar, that's so bakwas!",
    "Hurr, chill! You're too serious!",
    "Bhai, that's lit!🔥",
    "Cringe much? 😂",
    "Lol, chill yaar, it's not that serious!"
]

# Function to handle the /start command
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Hey! I am your SocialBot. Let\'s chat! Type anything to start.')

# Function to handle incoming messages
def reply(update: Update, context: CallbackContext) -> None:
    user_message = update.message.text

    # Language translation and slang generation
    blob = TextBlob(user_message)
    translated_message = blob.translate(to='en')

    # Get response from ChatterBot
    response = chatbot.get_response(translated_message)

    # If the response is too formal, add some slang
    if response.confidence < 0.6:
        response = random.choice(slang_responses)

    # Reply with a human-like response
    update.message.reply_text(response)

# Function to handle errors
def error(update: Update, context: CallbackContext) -> None:
    logger.warning(f'Update {update} caused error {context.error}')

# Main function to start the bot
def main():
    # Replace with your actual bot token
    TELEGRAM_TOKEN = '7573682690:AAHw2NIetFbKgxbyLpSp5cne3mCur1_jLJw'

    updater = Updater(TELEGRAM_TOKEN)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Add command handler for /start
    dispatcher.add_handler(CommandHandler('start', start))

    # Add message handler for normal text messages
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, reply))

    # Log all errors
    dispatcher.add_error_handler(error)

    # Start the bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()