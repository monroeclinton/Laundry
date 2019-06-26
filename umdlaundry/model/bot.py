import json
import asyncio
from discord.ext import commands
from umdlaundry.model.laundry import Laundry
import threading
import time


class Bot:

    """
    load config and create Discord bot
    """
    def __init__(self, username, password):
        with open("config/config.json") as file:
            config = json.load(file)

        self.prefix = config["command_prefix"]
        self.token = config["token"]
        self.laundry_data = []
        self.bot = None

        laundry = Laundry(username, password)
        thread = threading.Thread(target=laundry.run)
        thread.daemon = True
        thread.start()

        self.laundry_data = []

        thread = threading.Thread(target=self.update, args=(laundry,))
        thread.daemon = True
        thread.start()

    @commands.command(pass_context=True)
    async def help(self, ctx):
        recipient = ctx.message.author
        await self.bot.send_message(recipient, self.prefix + "laundry [dorm] [washer/drier] - create alert")
        await self.bot.send_message(recipient, self.prefix + "list - list dorms")

    @commands.command(pass_context=True)
    async def list(self, ctx):
        recipient = ctx.message.author

        if not self.laundry_data:
            await self.bot.send_message(recipient, "Updating... Check back in a minute.")
            return

        await self.bot.send_message(recipient, "List of dorms:")

        # get list of dorms
        dorms = {}

        dorms["string"] = ""
        dorms["array"] = []

        for dorm in self.laundry_data:
            dorms["string"] += dorm["dorm"] + ", "
            dorms["array"].append(dorm["dorm"])

        dorms["string"] = dorms["string"][:-2]

        await self.bot.send_message(recipient, dorms["string"])
        await self.bot.send_message(recipient, "Type the dorm name exactly as listed.")

    @commands.command(pass_context=True)
    async def laundry(self, ctx, dorm, machine):
        dorm = dorm.lower()
        machine = machine.lower()

        recipient = ctx.message.author

        if not self.laundry_data:
            await self.bot.send_message(recipient, "Updating... Check back in a minute.")
            return

        # get list of dorms
        dorms = dict()

        dorms["string"] = ""
        dorms["array"] = []
        dorms["status"] = dict()

        # build list of dorms, add current dorm
        for individual in self.laundry_data:
            if individual["dorm"] == dorm:
                dorms["status"] = individual
            dorms["string"] += individual["dorm"] + ", "
            dorms["array"].append(individual["dorm"])

        dorms["string"] = dorms["string"][:-2]

        # get dorm
        if not dorm in dorms["array"]:
            await self.bot.send_message(recipient, "Invalid dorm. Make sure spelling is correct.")
            return

        # get washer or drier
        if machine != "washer" and machine != "drier":
            await self.bot.send_message(recipient, "Invalid option. Type should be washer or drier.")
            return

        # tell user they weill be alerted
        if dorms["status"]["washer"]["available"] == 0 and machine == "washer":
            await self.bot.send_message(recipient, "You will be alerted when a washer becomes available.")

        if dorms["status"]["drier"]["available"] == 0 and machine == "drier":
            await self.bot.send_message(recipient, "You will be alerted when a drier becomes available.")

        # alert job
        if machine == "washer":
            asyncio.ensure_future(self.washer(recipient, dorm))

        if machine == "drier":
            asyncio.ensure_future(self.drier(recipient, dorm))

    """
    Washer job
    """
    async def washer(self, recipient, dorm_name):
        while True:
            laundry = None
            for dorm in self.laundry_data:
                if dorm["dorm"] == dorm_name:
                    laundry = dorm
            if laundry["washer"]["available"] > 0:
                await self.bot.send_message(recipient, "There is a washer available. There is currently "
                                            + str(laundry["washer"]["available"]) + " out of "
                                            + str(laundry["washer"]["total"]) + " available.")
                return
            await asyncio.sleep(5)

    """
    Drier job
    """
    async def drier(self, recipient, dorm_name):
        while True:
            laundry = None
            for dorm in self.laundry_data:
                if dorm["dorm"] == dorm_name:
                    laundry = dorm
            if laundry["drier"]["available"] > 0:
                await self.bot.send_message(recipient, "There is a drier available. There is currently "
                                            + str(laundry["drier"]["available"]) + " out of "
                                            + str(laundry["drier"]["total"]) + " available.")
                return
            await asyncio.sleep(5)

    """
    Updates laundry variable
    """
    def update(self, laundry):
        while True:
            self.laundry_data = laundry.get()
            time.sleep(5)

    """
    Creates bot, loads commands
    """
    def run(self):
        self.bot = commands.Bot(command_prefix=self.prefix)
        self.bot.remove_command("help")
        self.bot.add_command(self.help)
        self.bot.add_command(self.list)
        self.bot.add_command(self.laundry)

        print("------------------------STATUS------------------------")
        print("               The bot is now running.")
        print("------------------------STATUS------------------------")

        self.bot.run(self.token)