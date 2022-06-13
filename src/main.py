import logging

from TeleBot import TeleBot
from Server import Server


def main():
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    server = Server()
    bot = TeleBot(server)
    bot.run()


if __name__ == "__main__":
    main()
