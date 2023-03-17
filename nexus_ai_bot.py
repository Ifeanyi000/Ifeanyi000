import logging
import openai
import os
from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Set up logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

# Set up API keys
TELEGRAM_API_TOKEN = "5932171600:AAEAk-ZnCMRht1TAv2MG5am0XMs9GENsJuI"
OPENAI_API_KEY = "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"

# Initialize OpenAI GPT-3 API
openai.api_key = OPENAI_API_KEY

def start(update: Update, _: CallbackContext) -> None:
    update.message.reply_text('Hi! I am Nexus AI, your personal AI assistant. How can I help you today?')

def generate_response(prompt):
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=150,
        n=1,
        stop=None,
        temperature=0.5,
    )
    return response.choices[0].text.strip()

def message_handler(update: Update, _: CallbackContext) -> None:
    user_message = update.message.text
    if "?" in user_message:
        prompt = f"{user_message}"
    else:
        prompt = f"User: {user_message}\nAI:"
    generated_response = generate_response(prompt)
    update.message.reply_text(generated_response)

def main() -> None:
    updater = Updater(TELEGRAM_API_TOKEN)

    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, message_handler))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
