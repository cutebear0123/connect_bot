token='a token from https://discord.com/developers/applications'



import discord, json, aiohttp, asyncio
from discord.ext import commands
from discord.commands import Option

bot = commands.Bot()


class Safe:
    def __init__(self):
        self.colddown = []
        self.whitelist = []

    @property
    def blacklist(self):
        with open("blacklist.json", "r") as f:
            return json.load(f)


safe = Safe()


@bot.event
async def on_ready():
    print("Logged in as")
    print(bot.user.name)
    print(bot.user.id)
    print("------")
    while True:
        for i in safe.colddown:
            safe.colddown.remove(i)
        await asyncio.sleep(0.8)


@bot.slash_command()
async def connect(ctx):
    with open("conn.json", "r") as f:
        data = json.load(f)
    if str(ctx.channel.id) in data:
        await ctx.respond("you have been connect")
    else:
        webhook = await ctx.channel.create_webhook(name="連接者")
        data[ctx.channel.id] = webhook.url
        with open("conn.json", "w") as f:
            json.dump(data, f)
        await ctx.respond("you connect")


@bot.slash_command()
async def disconnect(ctx):
    with open("conn.json", "r") as f:
        data = json.load(f)
    if str(ctx.channel.id) in data:
        await ctx.respond("you disconnect")
        del data[str(ctx.channel.id)]
        with open("conn.json", "w") as f:
            json.dump(data, f)
    else:
        await ctx.respond("you are not connect")


@bot.event
async def on_message(message):
    if message.webhook_id:
        return
    if message.author.bot:
        if message.author.id in safe.whitelist:
            pass
        else:
            return

    else:
        with open("conn.json", "r") as f:
            data = json.load(f)
        if str(message.channel.id) in data:
            # if message.attachments!=
            if message.channel.id in safe.colddown:
                return
            if message.author.id in safe.blacklist:
                return

            else:
                safe.colddown.append(message.channel.id)
            for i in data:
                if message.channel.id != int(i):
                    async with aiohttp.ClientSession() as session:
                        async with session.post(
                            data[i],
                            json={
                                "content": message.content,
                                "username": f"{message.author.name} from {message.guild.name}",
                                "avatar_url": message.author.avatar.url,
                            },
                        ) as resp:
                            pass

bot.run(token)
