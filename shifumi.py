import discord
import random

from discord.ext import commands
from utils.util import srs_only, logtrace
from utils.emojis import shifumi
from utils.db import *


moves = {'pierre': 0, 'feuille': 1, 'papier': 1, 'ciseaux': 2, 'puits': 3}



def get_result(user_move: str, bot_move: str):
    result = 0 # draw = 0; user wins = 1; user loses = 2
    if (user_move == bot_move): # draw
        pass
    elif (user_move != 3 and bot_move != 3): # no well
        result = (1 if (((user_move | 1 << (2)) - (bot_move | 0 << (2))) % 3)\
                else 2)
    else:
        result = (1 if \
                ((user_move == 1 and bot_move == 3)\
                or (user_move == 3 and bot_move != 1)\
                ) else 2)
    return result



class ShifumiCog(commands.Cog):
    """
    Shifumi-with-well game.
    Commands:
      * /shifumi [pierre|feuille|papier|ciseaux|puits]
      * /shifumi score
      * /shifumi leaderboard (TODO)
      * /shifumi help
    """

    def __init__(self, bot):
        self.bot = bot


    def play(self, ctx, arg: str):
        """ Process the game, save into a database and send the score """
        user_move = moves[arg]
        bot_move = random.choice(list(moves.values()))

        result = get_result(user_move=user_move, bot_move=bot_move)

        user_score = result&1
        bot_score = (result&2) >> 1

        """ Save score to database """
        with DbConnection() as db:
            db.execute('SELECT * FROM score WHERE id = (?)', (ctx.author.id,))
            score = db.fetchone()
            if score is None:
                db.execute('INSERT INTO score VALUES (?, ?, ?, ?)',\
                        (ctx.author.id, ctx.author.display_name,\
                        user_score, bot_score))
            else:
                user_score += score[2]
                bot_score += score[3]
                db.execute('''UPDATE score
                SET username = ?,
                user_score = ?,
                bot_score = ?
                WHERE id = ?''', (ctx.author.display_name, user_score,\
                        bot_score, ctx.author.id))

        embed = discord.Embed(colour=discord.Colour.from_rgb(254, 254, 254),
            title="{0} vs {1}".format(ctx.author, ctx.bot.user),
            description="{0} vs {1}".format(\
                shifumi[user_move], shifumi[bot_move]))
        string_result = ("Match nul" if (result == 0) else \
                ("Tu as gagné" if (result == 1) else "Tu as perdu"))
        embed.add_field(name=string_result,\
                value="Score : {0} - {1}".format(user_score, bot_score),\
                inline=False)
        return embed


    def score(self, author, bot):
        """ Get score from database for a specific user. """
        with DbConnection() as db:
            db.execute('SELECT * FROM score WHERE id = (?)', (author.id,))
            score = db.fetchone()
            if score is None:
                db.execute('INSERT INTO score VALUES (?, ?, ?, ?)',\
                        (author.id, author.display_name, 0, 0))
                embed = discord.Embed(\
                        colour=discord.Colour.from_rgb(254, 254, 254),
                        title="Score pour {0} vs {1}".format(author, bot.user),
                        description="0 - 0")
            else:
                embed = discord.Embed(\
                        colour=discord.Colour.from_rgb(254, 254, 254),
                        title="Score pour {0} vs {1}".format(author, bot.user),
                        description="{0} - {1}".format(score[2], score[3]))
            return embed


    def leaderboard(self):
        return


    def _help(self):
        return discord.Embed(colour=discord.Colour.from_rgb(254, 254, 254),
            title="Manuel d'utilisation",
            description="" \
            + "**Jouer**\n" \
            + "/shifumi \"[pierre|feuille|papier|ciseaux|puits]\"\n\n" \
            + "**Afficher son score**\n" \
            + "/shifumi \"score\"\n\n")


    @commands.command(name='shifumi')
    @srs_only()
    async def send_shifumi(self, ctx, *args):
        """ Args parser and dispath method. """
        try:
            if (len(args) != 1):
                await ctx.send(embed=self._help())
            elif (args[0] in moves):
                await ctx.send(content=ctx.author.mention,\
                        embed=self.play(ctx, args[0]))
            elif (args[0] == 'score'):
                await ctx.send(content=ctx.author.mention,\
                        embed=self.score(author=ctx.author, bot=ctx.bot))
            elif (args[0] == 'leaderboard'):
                await ctx.send(embed=self.leaderboard())
            else:
                await ctx.send(embed=self._help())
            return
        except Exception as e:
            await logtrace(ctx, e)

def setup(bot):
    bot.add_cog(ShifumiCog(bot))
