# Xero Discord Bot

![Xero Bot](https://example.com/xero_bot_thumbnail.png)

## Overview

The **Xero Discord Bot** is a Python-based Discord bot designed to streamline interactions with the Xero API, offering users an intuitive way to access information about blocked players, challenges, user status, clans, and players on the Xero gaming platform.

## Features

- **Self API Interaction:**
  - Retrieve information about blocked players, challenges, user status, social friends, and social clan using simple Discord commands.
  
- **Player/Clan Info:**
  - Obtain detailed information about specific clans and players by providing their names.
  
- **Help Command:**
  - Quickly access information about available bot commands with the `api_help` command.

## Installation

1. Ensure you have Python installed on your machine.
2. Install the required Python packages:

    ```bash
    pip install discord.py requests
    ```

3. Copy and paste the provided bot code into a Python file (e.g., `xero_bot.py`).
4. Replace the placeholder Xero API access keys in the code with your valid keys.
5. Run the bot:

    ```bash
    python xero_bot.py
    ```

## Usage

1. Invite the bot to your Discord server.
2. Use the provided commands to interact with the Xero API and retrieve valuable gaming information.

## Commands

### Self API Commands

#### `.p block`

Retrieve information about blocked players.

#### `.p challenge`

Retrieve information about challenges.

#### `.p self`

Retrieve information about the user's status.

#### `.p self_social_friends`

Retrieve information about the user's social friends.

#### `.p self_social_clan`

Retrieve information about the user's social clan.

### Player/Clan Info Commands

#### `.p clan <clan_name>`

Retrieve information about a specific clan.

#### `.p player <player_name>`

Retrieve information about a specific player.

### Help Command

#### `.p api_help`

Display a help message containing information about available bot commands.

## Contribution

Contributions are welcome! If you have ideas for improvements or new features, feel free to open an issue or submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).

---

