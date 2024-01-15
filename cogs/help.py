import discord
from discord.ext import commands


class HelpCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="api_help")
    async def help_command(self, ctx):
        embed = discord.Embed(title="Xero API Bot Commands", color=0xadd8e6)  # Baby blue color code
        embed.set_thumbnail(url="https://xero.gg/assets/img/2020/logo/logo_hover.png")  # Replace with your bot's thumbnail URL

        embed.add_field(
            name="Self API Calls Commands Using Access Keys",
            value=(
                "`.p block`: Retrieve information about blocked players.\n"
                "`.p challenge`: Retrieve information about challenges.\n"
                "`.p self`: Retrieve information about the user's status.\n"
                "`.p self_social_friends`: Retrieve information about the user's social friends.\n"
                "`.p self_social_clan`: Retrieve information about the user's social clan."
            ),
            inline=False
        )

        embed.add_field(
            name="Player/Clan Info Commands",
            value=(
                "`.p clan <clan_name>`: Retrieve information about a specific clan.\n"
                "`.p player <player_name>`: Retrieve information about a specific player."
            ),
            inline=False
        )

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(HelpCog(bot))
