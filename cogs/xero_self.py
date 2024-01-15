import discord
from discord.ext import commands
import requests

class XeroAPI:
    BASE_URL = "https://xero.gg/api"

    @classmethod
    def set_keys(cls, api_access_key_id, api_secret_access_key):
        cls.HEADERS = {
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

class SelfAPI(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="block")
    async def block_command(self, ctx):
        await ctx.send("Please enter your Xero API access key:")
        api_access_key_id = await self.bot.wait_for('message', check=lambda m: m.author == ctx.author)
        api_access_key_id = api_access_key_id.content

        await ctx.send("Please enter your Xero API secret access key:")
        api_secret_access_key = await self.bot.wait_for('message', check=lambda m: m.author == ctx.author)
        api_secret_access_key = api_secret_access_key.content

        XeroAPI.set_keys(api_access_key_id, api_secret_access_key)

        block_info = XeroAPI.make_request("block")

        if block_info and block_info.get("success"):
            blocks = block_info.get("blocks", [])
            await self.send_blocks_embed(ctx, blocks)
        else:
            await ctx.send("Error retrieving blocked players information.")

    async def send_blocks_embed(self, ctx, blocks):
        embed = discord.Embed(title="Blocked Players", color=0xadd8e6)  # Baby blue color code

        for block in blocks:
            embed.add_field(
                name=block['name'],
                value=f"XP: {block['progression']['xp']} | Level: {block['progression']['level']['value']}",
                inline=False
            )

        await ctx.send(embed=embed)
        
    @commands.command(name="challenge")
    async def challenge_command(self, ctx):
        await ctx.send("Please enter your Xero API access key:")
        api_access_key_id = await self.bot.wait_for('message', check=lambda m: m.author == ctx.author)
        api_access_key_id = api_access_key_id.content

        await ctx.send("Please enter your Xero API secret access key:")
        api_secret_access_key = await self.bot.wait_for('message', check=lambda m: m.author == ctx.author)
        api_secret_access_key = api_secret_access_key.content

        XeroAPI.set_keys(api_access_key_id, api_secret_access_key)

        challenge_info = XeroAPI.make_request("challenge")

        if challenge_info and 'challenges' in challenge_info:
            challenges = challenge_info['challenges']
            await self.send_challenges_embed(ctx, challenges)
        else:
            await ctx.send("Error retrieving challenges information.")

    async def send_challenges_embed(self, ctx, challenges):
        embed = discord.Embed(title="Challenges", color=0xadd8e6)  # Baby blue color code

        for challenge in challenges:
            embed.add_field(
                name=challenge['name'],
                value=f"Start Date: {challenge['startDate']} | End Date: {challenge['endDate']}",
                inline=False
            )

        await ctx.send(embed=embed)
        
    @commands.command(name="self")
    async def self_status_command(self, ctx):
        await ctx.send("Please enter your Xero API access key:")
        api_access_key_id = await self.bot.wait_for('message', check=lambda m: m.author == ctx.author)
        api_access_key_id = api_access_key_id.content

        await ctx.send("Please enter your Xero API secret access key:")
        api_secret_access_key = await self.bot.wait_for('message', check=lambda m: m.author == ctx.author)
        api_secret_access_key = api_secret_access_key.content

        XeroAPI.set_keys(api_access_key_id, api_secret_access_key)

        self_info = XeroAPI.make_request("self/status")

        if self_info and 'success' in self_info and self_info['success']:
            await self.send_self_info_embed(ctx, self_info)
        else:
            await ctx.send("Error retrieving self information.")

    async def send_self_info_embed(self, ctx, self_info):
        info = self_info['info']
        currency = self_info['currency']
        web_status = self_info['web']
        game_status = self_info['game']

        embed = discord.Embed(title=f"Status for {info['name']}", color=0xadd8e6)  # Baby blue color code

        # User Information
        embed.set_thumbnail(url=info['avatar']['image'])
        embed.add_field(name="Clan", value=f"Name: {info['clan']['name']}", inline=True)
        embed.add_field(name="Level", value=f"Value: {info['progression']['level']['value']}", inline=True)
        embed.add_field(name="XP", value=f"{info['progression']['xp']} XP", inline=True)
        embed.add_field(name="Premium", value=f"Enabled: {info['premium']['enabled']}", inline=True)
        embed.add_field(name="Premium Expiry", value=f"Expiry Time: {info['premium']['expiryTime']}", inline=True)

        # Currency Information
        embed.add_field(name="Currency", value=f"Pen: {currency['pen']} | ZP: {currency['zp']} | Gems: {currency['gems']}", inline=False)

        # Web Status
        embed.add_field(name="Web Status", value=f"Online: {web_status['online']}", inline=False)

        # Game Status
        embed.add_field(name="Game Status", value=f"Online: {game_status['online']}", inline=True)

        await ctx.send(embed=embed)
        
    @commands.command(name="self_social_friends")
    async def self_social_friends_command(self, ctx):
        await ctx.send("Please enter your Xero API access key:")
        api_access_key_id = await self.bot.wait_for('message', check=lambda m: m.author == ctx.author)
        api_access_key_id = api_access_key_id.content

        await ctx.send("Please enter your Xero API secret access key:")
        api_secret_access_key = await self.bot.wait_for('message', check=lambda m: m.author == ctx.author)
        api_secret_access_key = api_secret_access_key.content

        XeroAPI.set_keys(api_access_key_id, api_secret_access_key)

        friends_info = XeroAPI.make_request("self/social/friends")

        if friends_info and 'success' in friends_info and friends_info['success']:
            await self.send_social_friends_paginated(ctx, friends_info)
        else:
            await ctx.send("Error retrieving social friends information.")

    async def send_social_friends_paginated(self, ctx, friends_info):
        players = friends_info['players']
        chunked_players = [players[i:i + 25] for i in range(0, len(players), 25)]

        for chunk in chunked_players:
            embeds = self.create_social_friends_embed(chunk)
            for embed in embeds:
                await ctx.send(embed=embed)

    def create_social_friends_embed(self, players):
        embeds = []
        for player in players:
            name = player['name']
            progression = player['progression']
            web_status = player['web']
            game_status = player['game']

            embed = discord.Embed(title=f"Social Friends - {name}", color=0xadd8e6)  # Baby blue color code
            embed.add_field(name="XP", value=f"{progression['xp']} | Level: {progression['level']['value']}", inline=False)
            embed.add_field(name="Web Status", value=f"Online: {web_status['online']}", inline=True)
            embed.add_field(name="Game Status", value=f"Online: {game_status['online']}", inline=True)

            if game_status['online']:
                server_name = game_status['server']['name'] if game_status['server'] else "N/A"
                channel_name = game_status['channel']['name'] if game_status['channel'] else "N/A"
                room_id = game_status['room']['id'] if game_status['room'] else "N/A"

                embed.add_field(name="Server", value=server_name, inline=True)
                embed.add_field(name="Channel", value=channel_name, inline=True)
                embed.add_field(name="Room ID", value=room_id, inline=True)

            embeds.append(embed)

        return embeds

    @commands.command(name="self_social_clan")
    async def self_social_clan_command(self, ctx):
        await ctx.send("Please enter your Xero API access key:")
        api_access_key_id = await self.bot.wait_for('message', check=lambda m: m.author == ctx.author)
        api_access_key_id = api_access_key_id.content

        await ctx.send("Please enter your Xero API secret access key:")
        api_secret_access_key = await self.bot.wait_for('message', check=lambda m: m.author == ctx.author)
        api_secret_access_key = api_secret_access_key.content

        XeroAPI.set_keys(api_access_key_id, api_secret_access_key)

        clan_info = XeroAPI.make_request("self/social/clan")

        if clan_info and 'success' in clan_info and clan_info['success']:
            await self.send_social_clan_info_paginated(ctx, clan_info)
        else:
            await ctx.send("Error retrieving social clan information.")

    async def send_social_clan_info_paginated(self, ctx, clan_info):
        players = clan_info['players']
        chunked_players = [players[i:i + 25] for i in range(0, len(players), 25)]

        for chunk in chunked_players:
            embeds = self.create_social_clan_info_embed(chunk)
            for embed in embeds:
                await ctx.send(embed=embed)

    def create_social_clan_info_embed(self, players):
        embeds = []
        for player in players:
            name = player['name']
            progression = player['progression']
            web_status = player['web']
            game_status = player['game']

            embed = discord.Embed(title=f"Social Clan Info - {name}", color=0xadd8e6)  # Baby blue color code
            embed.add_field(name="XP", value=f"{progression['xp']} | Level: {progression['level']['value']}", inline=False)
            embed.add_field(name="Web Status", value=f"Online: {web_status['online']}", inline=True)
            embed.add_field(name="Game Status", value=f"Online: {game_status['online']}", inline=True)

            if game_status['online']:
                server_name = game_status['server']['name'] if game_status['server'] else "N/A"
                channel_name = game_status['channel']['name'] if game_status['channel'] else "N/A"
                room_id = game_status['room']['id'] if game_status['room'] else "N/A"

                embed.add_field(name="Server", value=server_name, inline=True)
                embed.add_field(name="Channel", value=channel_name, inline=True)
                embed.add_field(name="Room ID", value=room_id, inline=True)

            embeds.append(embed)

        return embeds


async def setup(bot):
    await bot.add_cog(SelfAPI(bot))
