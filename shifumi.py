import discord
import random

moves = {'pierre': 0, 'paper': 1, 'feuille': 1, 'ciseaux': 2, 'puit': 3}
emojis = {0: "\N{Raised Fist}", 1: "\N{Raised Hand}", 2: "\N{Victory Hand}", 3: "\N{OK Hand Sign}"}

async def parse(ctx, *args):
    if (len(args) != 1):
        await ctx.send(embed=help())
        return
    if (args[0] == 'leaderboard'):
        await ctx.send(embed=leaderboard())
        return
    if (args[0] == 'score'):
        await ctx.send(embed=score(ctx))
        return
    if (args[0] in moves):
        await ctx.send(embed=play(ctx, args))
        return
    else:
        await ctx.send(embed=help())
        return

def play(ctx, *args):
    bot = random.choice(list(moves.values()))
    user = moves[args[0]]
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
            title="{0} vs {1}".format(ctx.author, ctx.bot),
            description="{0} vs {1}".format(emojis[user], emojis[bot]))

    if (result == 0):
        embed.add_field(name="Match nul", value="", inline=False)
    elif (result == 1):
        embed.add_field(name="Tu as gagné", value="", inline=False)
    elif (result == 2):
        embed.add_field(name="Tu as perdu", value="", inline=False)
    else:
        return
    return embed

async def leaderboard():
    return

async def score(ctx):
    return

async def help():
    return discord.Embed(colour=discord.Colour.from_rgb(254, 254, 254),
            title="Manuel d'utilisation",
            description="" \
            + "**Jouer**\n" \
            + "/shifumi \"[pierre|feuille|papier|ciseaux|puit]\"\n" \
            + "**Afficher son score**\n\n" \
            + "/shifumi \"score\"" \
            + "**Afficher le leaderboard**\n\n" \
            + "/shifumi \"leaderboard\"")
