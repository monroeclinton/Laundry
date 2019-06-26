from umdlaundry.model.bot import Bot


def main(username, password):
    bot = Bot(username, password)
    bot.run()
