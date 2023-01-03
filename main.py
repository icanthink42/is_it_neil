import random

import discord

bot = discord.Bot()

guilds = [349402004549795840]

neil_id = 343545158140428289

games = {}


not_neils = {518911004164227075: None, 940441319057276958: None}


@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")
    global neil
    neil = await bot.fetch_user(neil_id)


@bot.event
async def on_message(message):
    if message.author == bot.user or not isinstance(
        message.channel, discord.channel.DMChannel
    ):
        return
    if message.author.id == neil_id and message.reference != None:
        reply_message = await message.author.fetch_message(message.reference.message_id)
        try:
            other_id = int(
                reply_message.content.split(":")[0]
                .replace("<", "")
                .replace(">", "")
                .replace("@", "")
            )
            if other_id not in games:
                await message.reply("*You are not in a game with that person anymore!*")
                return
            other_user = await bot.fetch_user(other_id)
            await other_user.send(message.content)
        except:
            await message.reply(
                "*Hey shitass. Reply to a message sent by another user!*"
            )
            return
    elif message.author.id == neil_id and message.reference == None:
        await message.reply(
            "*Reply to a message with the text you wish to send so the bot knows who you are talking to.*"
        )
    elif message.author.id not in games and (
        message.author.id not in not_neils
        or (message.author.id in not_neils and not_neils[message.author.id] is None)
    ):
        await message.reply("Run /play to start a game!")
    elif message.author.id not in games and message.author.id in not_neils:
        other_user = await bot.fetch_user(not_neils[message.author.id])
        await other_user.send(message.content)
    else:
        game = games[message.author.id]
        if game["to_neil"]:
            await neil.send(f"<@{message.author.id}>: {message.content}")
        else:
            other_user = await bot.fetch_user(game["chatting_to"])
            await other_user.send(message.content)


@bot.slash_command(guild_ids=guilds)
async def is_neil(ctx):
    if ctx.author.id not in games:
        await ctx.respond("I mean cool but ur not in a game rn.", ephemeral=True)
        return
    game = games[ctx.author.id]
    if game["to_neil"]:
        await neil.send(
            f"**<@{ctx.author.id}> guessed that you where Neil correctly! L+Ratio!**"
        )
        await ctx.respond(
            f"<@{ctx.author.id}> guessed correctly that they where talking to Neil!"
        )
    else:
        other_user = await bot.fetch_user(games[ctx.author.id]["chatting_to"])
        await other_user.send(
            f"**You successfully tricked <@{ctx.author.id}> into thinking they where talking to Neil!**"
        )
        await ctx.respond(
            f"<@{other_user.id}> successfully tricked <@{ctx.author.id}> into thinking they were Neil!"
        )
        not_neils[other_user.id] = None
    del games[ctx.author.id]


@bot.slash_command(guild_ids=guilds)
async def not_neil(ctx):
    if ctx.author.id not in games:
        await ctx.respond("I mean cool but ur not in a game rn.", ephemeral=True)
        return
    game = games[ctx.author.id]
    if not game["to_neil"]:
        other_user = await bot.fetch_user(games[ctx.author.id]["chatting_to"])
        await other_user.send(
            f"**<@{ctx.author.id}> guessed that you where not Neil correctly! L+Ratio!**"
        )
        await ctx.respond(
            f"<@{ctx.author.id}> guessed correctly that they where not talking to Neil!"
        )
        not_neils[other_user.id] = None
    else:
        await neil.send(
            f"**You successfully tricked <@{ctx.author.id}> into thinking they where not talking to Neil!**"
        )
        await ctx.respond(
            f"Neil successfully tricked <@{ctx.author.id}> into thinking they were not talking to Neil!"
        )
    del games[ctx.author.id]


@bot.slash_command(guild_ids=guilds)
async def play(ctx):
    if ctx.author.id == neil_id:
        await ctx.respond("You are ~~Neil!~~ Niel!", ephemeral=True)
        return
    if ctx.author.id in games:
        await ctx.respond("You are already in a game!", ephemeral=True)
        return
    for _ in range(100):
        chatting_to = random.choice(list(not_neils.keys()))
        if (
            not_neils[chatting_to] is None
            and chatting_to not in games
            and chatting_to != ctx.author.id
        ):
            break
    else:
        await ctx.respond(
            "There are not enough people avalible to play the part of fake Neil!",
            ephemeral=True,
        )
        return
    to_neil = random.choice([True, False])
    games[ctx.author.id] = {
        "chatting_to": chatting_to,
        "to_neil": to_neil,
    }
    await ctx.author.send(
        "**Game started! When you're ready to guess go back to cola and run /is_neil or /not_neil**"
    )
    if to_neil:
        await neil.send(
            f"**<@{ctx.author.id}>:{ctx.author.name} has begun a game. Make them belive they arn't talking to Neil!**"
        )
    else:
        other = await bot.fetch_user(chatting_to)
        not_neils[chatting_to] = ctx.author.id
        await other.send(
            f"**{ctx.author.name} has started a game! Make them belive they are talking to Neil!**"
        )
    await ctx.respond("Started Game...", ephemeral=True)


f = open("token")
token = f.read().strip()
f.close()
bot.run(token)
