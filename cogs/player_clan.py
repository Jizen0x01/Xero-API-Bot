import discord
from discord.ext import commands
import requests

api_access_key_id = "YOUR_XERO_API_ACCESS_KEY_ID"
api_secret_access_key = "YOUR_XERO_API_SECRET_ACCESS_KEY"

class XeroAPI:
    BASE_URL = "https://xero.gg/api"
    HEADERS = {
        "x-api-access-key-id": api_access_key_id,
        "x-api-secret-access-key": api_secret_access_key
    }

    @classmethod
    def make_request(cls, endpoint, params=None):
        url = f"{cls.BASE_URL}/{endpoint}"
        response = requests.get(url, headers=cls.HEADERS, params=params)

        if response.status_code == 200:
            return response.json()
        else:
            return None

class XeroCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="clan")
    async def xero_player_command(self, ctx, *player_names):
        if not player_names:
            await ctx.send("Please provide at least one clan name.")
            return

        # Retrieve clan information for each player
        for player_name in player_names:
            clan_info = XeroAPI.make_request(f"clan/{player_name}")

            if clan_info and clan_info.get("success"):
                clan_data = clan_info.get("clan", {})
                await self.send_clan_embed(ctx, clan_data)
            else:
                await ctx.send(f"Error retrieving clan information for {player_name}.")

    @commands.command(name="player")
    async def player_command(self, ctx, player_name):
        player_info = XeroAPI.make_request(f"player/{player_name}")

        if player_info and player_info.get("success"):
            player_data = player_info.get("player", {})
            embed = self.create_player_embed(player_data)
            await ctx.send(embed=embed)
        else:
            await ctx.send(f"Error retrieving information for {player_name}.")

    async def send_clan_embed(self, ctx, clan_data):
        members = clan_data.get("members", [])
        chunked_members = [members[i:i + 25] for i in range(0, len(members), 25)]

        for chunk in chunked_members:
            embed = self.create_clan_embed(clan_data, chunk)
            await ctx.send(embed=embed)

    def create_clan_embed(self, clan_data, members_chunk):
        rank_names = {
        1: "Master",
        3: "Staff",
        4: "Regular",
        6: "Bad Manner"
        }

        # Check if the 'id' key exists in clan_data, use it if present, otherwise use 'name'
        clan_id = clan_data.get('id', clan_data.get('name', 'N/A'))
    
        clan_url = f"[Clan URL](https://xero.gg/clan/{clan_id})"
        embed = discord.Embed(title=f"Clan: {clan_data.get('name', 'N/A')}", description=clan_url, color=0xadd8e6)  # Baby blue color code
        embed.set_thumbnail(url=clan_data.get("image", ""))

        for member in members_chunk:
            rank_value = member['rank']
            rank_name = rank_names.get(rank_value, f"Unknown Rank {rank_value}")

            player_name = member['name']
            player_link = f"[{player_name}](https://xero.gg/player/{player_name})"

            embed.add_field(
                name=f"{player_link} ({rank_name})",
                value=f"Level: {member['progression']['level']['value']} | XP: {member['progression']['xp']}",
                inline=False
            )

        return embed


    def create_player_embed(self, player_data):
        player_url = f"[Player URL](https://xero.gg/player/{player_data['name']})"
        embed = discord.Embed(title=f"Player: {player_data['name']}", description=player_url, color=0xadd8e6)  # Baby blue color code

        # Add clan information
        clan_data = player_data.get("clan")
        if clan_data:
            embed.add_field(name="Clan", value=f"Name: {clan_data.get('name', 'N/A')}", inline=False)
        else:
            embed.add_field(name="Clan", value="N/A", inline=False)

        # Add avatar information
        avatar_data = player_data.get("avatar", {})
        embed.set_thumbnail(url=avatar_data.get("image", ""))

        # Add progression information
        progression_data = player_data.get("progression", {})
        level_data = progression_data.get("level", {})
        progress_data = level_data.get("progress", {})
        embed.add_field(name="XP", value=f"{progression_data.get('xp', 'N/A')}", inline=True)
        embed.add_field(name="Level", value=f"{level_data.get('value', 'N/A')}", inline=True)
        embed.add_field(name="Progress", value=f"{progress_data.get('percentage', 'N/A')}%", inline=True)

        return embed

async def setup(bot):
    await bot.add_cog(XeroCog(bot))

