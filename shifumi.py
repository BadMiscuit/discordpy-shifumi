import discord
import random
from db import *

moves = {'pierre': 0, 'papier': 1, 'feuille': 1, 'ciseaux': 2, 'puits': 3}
emojis = {0: "\N{Raised Fist}", 1: "\N{Raised Hand}", 2: "\N{Victory Hand}", 3: "\N{OK Hand Sign}"}

async def send_shifumi(ctx, *args):
    try:
        if (len(args) != 1):
            await ctx.send(embed=shifumi_help())
            return
        if (args[0] == 'leaderboard'):
            await ctx.send(embed=leaderboard())
            return
        if (args[0] == 'score'):
            await ctx.send(content=ctx.author.mention, embed=score(ctx))
            return
        if (args[0] in moves):
            await ctx.send(content=ctx.author.mention, embed=play(ctx, args))
            return
        else:
            await ctx.send(embed=shifumi_help())
            return
    except Exception as e:
        print(str(e))
        await ctx.send(embed=shifumi_help())

def play(ctx, *args):
    bot = random.choice(list(moves.values()))
    user = moves[args[0][0]]
    result = 0 # 0 draw ; 1 user wins ; 2 user loses
    if (bot == user):
        pass
    elif (bot != 3 and user != 3):
        if (((user | 1 << (2)) - (bot | 0 << (2))) % 3):
            result = 1
        else:
            result = 2
    else:
        if (bot == 3):
            if (user == 1):
                result = 1
            else:
                result = 2
        elif (user == 3):
            if (bot == 1):
                result = 2
            else:
                result = 1
    embed = discord.Embed(colour=discord.Colour.from_rgb(254, 254, 254),
            title="{0} vs {1}".format(ctx.author, ctx.bot.user),
            description="{0} vs {1}".format(emojis[user], emojis[bot]))

    user_score = result&1
    bot_score = (result&2) >> 1
    with DbConnection() as db:
        db.execute('SELECT * FROM score WHERE id = (?)', (ctx.author.id,))
        score = db.fetchone()
        if score is None:
            db.execute('INSERT INTO score VALUES (?, ?, ?, ?)', (ctx.author.id, ctx.author.display_name, user_score, bot_score))
        else:
            user_score += score[2]
            bot_score += score[3]
            db.execute('''UPDATE score
                    SET username = ?,
                    user_score = ?,
                    bot_score = ?
                    WHERE id = ?''', (ctx.author.display_name, user_score, bot_score, ctx.author.id))

    if (result == 0):
        embed.add_field(name="Match nul", value="Score : {0} - {1}".format(user_score, bot_score), inline=False)
    elif (result == 1):
        embed.add_field(name="Tu as gagné", value="Score : {0} - {1}".format(user_score, bot_score), inline=False)
    elif (result == 2):
        embed.add_field(name="Tu as perdu", value="Score : {0} - {1}".format(user_score, bot_score), inline=False)
    else:
        return
    return embed

async def leaderboard():
    return

def score(ctx):
    with DbConnection() as db:
        db.execute('SELECT * FROM score WHERE id = (?)', (ctx.author.id,))
        score = db.fetchone()
        if score is None:
            db.execute('INSERT INTO score VALUES (?, ?, ?, ?)', (ctx.author.id, ctx.author.display_name, 0, 0))
            embed = discord.Embed(colour=discord.Colour.from_rgb(254, 254, 254),
                    title="Score pour {0} vs {1}".format(ctx.author, ctx.bot.user),
                    description="0 - 0")
        else:
            embed = discord.Embed(colour=discord.Colour.from_rgb(254, 254, 254),
                    title="Score pour {0} vs {1}".format(ctx.author, ctx.bot.user),
                    description="{0} - {1}".format(score[2], score[3]))
        return embed

async def leaderboard():
    return

def shifumi_help():
    return discord.Embed(colour=discord.Colour.from_rgb(254, 254, 254),
            title="Manuel d'utilisation",
            description="" \
            + "**Jouer**\n" \
            + "/shifumi \"[pierre|feuille|papier|ciseaux|puits]\"\n\n" \
            + "**Afficher son score**\n" \
            + "/shifumi \"score\"\n\n")

            #+ "**Afficher le leaderboard**\n" \
            #+ "/shifumi \"leaderboard\"")
