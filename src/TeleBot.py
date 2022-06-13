import logging
import random

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

from Server import Server
from config import config as cfg
from src import Emojis
from src.StringFormatter import bold

knowledge: list = ["Knowledge1",
                   "Knowledge2",
                   "Knowledge3"]

all_keywords = {
    "keyword1": ["hint11", "hint12", "hint13", "hint14"],
    "keyword2": ["hint21", "hint22", "hint23", "hint24"],
}

all_reactions = {
    "keyword1": [
        "Some text1 here {emoji}".format(emoji=Emojis.PIZZA)],
    "keyword2": [
        "Some text2 here {emoji}".format(emoji=Emojis.PILL)]
}

logger = logging.getLogger()


class TeleBot:
    telegram_bot_token: str
    server: Server
    keywords: dict[str, list[str]]
    reactions: dict[str, list[str]]

    def __init__(self, server):
        self.load_config()
        self.server = server
        self.keywords = all_keywords
        self.reactions = all_reactions

    def load_config(self):
        self.telegram_bot_token = cfg.config["telegram_bot_token"]
        logger.info("Config loaded...")

    def run(self):
        updater = Updater(token=self.telegram_bot_token, use_context=True)
        dispatcher = updater.dispatcher
        dispatcher.add_handler(CommandHandler('start', self.command_start))
        dispatcher.add_handler(CommandHandler("help", self.command_help))
        dispatcher.add_handler(CommandHandler('knowledge', self.command_knowledge))
        dispatcher.add_handler(CommandHandler('computation', self.command_computation))

        dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, self.interpret_text))

        # Add this handler last to avoid unexpected behaviour.
        dispatcher.add_handler(MessageHandler(Filters.command, self.command_unknown))

        updater.start_polling()

        # Run the bot until you press Ctrl-C or the process receives SIGINT,
        # SIGTERM or SIGABRT. This should be used most of the time, since
        # start_polling() is non-blocking and will stop the bot gracefully.
        updater.idle()

    def command_start(self, update, context):
        context.bot.send_message(chat_id=update.effective_chat.id, text="Start command!")

    def command_help(self, update, _: CallbackContext) -> None:
        update.message.reply_text('Help command!')

    def command_knowledge(self, update, context):
        context.bot.send_message(chat_id=update.effective_chat.id, text=random.choice(knowledge))

    def command_computation(self, update, context):
        response = self.server.compute(context)
        context.bot.send_message(chat_id=update.effective_chat.id, text=response)

    def command_unknown(self, update, context):
        context.bot.send_message(chat_id=update.effective_chat.id, text="Command not implemented yet :(")

    def interpret_text(self, update, context):
        message = update.message.text
        reply = self.find_reply(message)
        if reply:
            context.bot.send_message(chat_id=update.effective_chat.id, parse_mode="MarkdownV2", text=reply)

    def find_reply(self, message):
        for concept, keywords in self.keywords.items():

            match = next((keyword for keyword in keywords if keyword.lower() in message.lower()), None)
            if match:
                available_reactions = self.reactions.get(concept)
                return "Did you say {word}?? {text}".format(word=bold(match), text=random.choice(available_reactions))
