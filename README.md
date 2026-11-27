# Game-Discord-Clans-Bot

A Discord bot that brings clans to your game. Players team up with their friends, apply to create a clan, and get their own dedicated space inside the game's Discord server, all managed through simple commands.

## Overview

Playing with your team is better when your community is built around it. This bot lets players form clans directly in your Discord server. Once a clan is approved, it gets its own role and channel, plus access to areas of the server that regular members can't see.

Staff stay in control. Every clan application goes through a review, clan names are checked before they reach the server, and every action can be logged to a dedicated channel.

## Features

- **Clan creation:** players apply to start a clan with a unique tag, then invite their friends to join
- **Staff approval:** staff accept or deny each clan application before the clan goes live
- **Dedicated clan role and channel:** every approved clan gets its own role and its own channel
- **Exclusive areas:** clan members unlock access to certain new places in the server
- **Leadership roles:** clan leaders can promote members to co leader, remove members, transfer ownership and disband the clan
- **Invite system:** leaders and co leaders invite players, who can accept or decline
- **Name protection:** clan tags are limited to letters and numbers (no emojis or special characters), must be unique, and are run through a language filter to block inappropriate names
- **Clan profiles:** clans can set a Discord invite, YouTube link, logo, banner and colour, and anyone can look up a clan's info
- **Event win tracking:** staff can add and remove Roams, KOTH and Maze wins for a clan
- **Staff tools:** force disband, invite, remove or transfer any clan
- **Logging:** clan activity can be sent to a logs channel
- **Persistent storage:** all clan data is stored in MongoDB

## How It Works

1. A player runs `!clancreate <tag>`
2. The tag is validated (letters and numbers only, not already taken, player not already in a clan)
3. The application is sent to staff, who accept or deny it
4. If accepted, the clan's role and channel are created and the applicant becomes the clan leader
5. The leader invites friends with `!claninvite @member`, and can promote co leaders with `!clanpromote @member`
6. Clan members get access to the server's clan areas

## Commands

The default prefix is `!` and can be changed in `config.json`.

### General

| Command | Aliases | Description |
| --- | --- | --- |
| `!help` | `clanhelp` | Show the help menu |
| `!aliases` | | Show the aliases for every command |
| `!clancreate <tag>` | `cc` | Apply to create a clan |
| `!clanleave` | | Leave your current clan (leaders can't leave their own clan) |
| `!claninfo [tag]` | `info` | View a clan's info, or your own clan if no tag is given |

### Clan leaders and co leaders

| Command | Aliases | Description |
| --- | --- | --- |
| `!claninvite @member` | `ci` | Invite a member to your clan |
| `!clanremove @member` | `clankick`, `ck`, `cr` | Remove a member from your clan |

### Clan leaders only

| Command | Aliases | Description |
| --- | --- | --- |
| `!clanpromote @member` | `promote` | Promote a member to co leader |
| `!clandemote @member` | `demote` | Demote a co leader back to member |
| `!changeleader @member` | `cl` | Transfer clan ownership to another member |
| `!changename <newname>` | | Change your clan's name |
| `!clandisband` | `cd` | Disband your clan (asks for confirmation) |
| `!clansetdiscord <link>` | `csd` | Set your clan's Discord invite |
| `!clansetyoutube <link>` | `csy` | Set your clan's YouTube link |
| `!clansetlogo <image link>` | `csl` | Set your clan's logo |
| `!clansetbanner <image link>` | `csb` | Set your clan's banner |
| `!clansetcolor <#hex>` | `csc` | Set your clan's colour |

### Staff

| Command | Aliases | Description |
| --- | --- | --- |
| `!forcedisband <tag>` | `fd` | Force a clan to disband |
| `!forceinvite <tag> @member` | `fi` | Force invite a member to a clan |
| `!forceremove <tag> @member` | `fr` | Force remove a member from a clan |
| `!forcetransfer <tag> @newleader` | `ft` | Force transfer a clan to another user |
| `!addroamwin <tag>` | | Add a Roams win to a clan |
| `!addkothwin <tag>` | | Add a KOTH win to a clan |
| `!addmazewin <tag>` | | Add a Maze win to a clan |
| `!removeroamwin <tag>` | | Remove a Roams win from a clan |
| `!removekothwin <tag>` | | Remove a KOTH win from a clan |
| `!removemazewin <tag>` | | Remove a Maze win from a clan |

## Getting Started

### Prerequisites

- Python 3.10 or 3.11 (the pinned dependencies are older versions)
- A MongoDB database, such as a free [MongoDB Atlas](https://www.mongodb.com/atlas) cluster
- A bot application from the [Discord Developer Portal](https://discord.com/developers/applications) with the **Server Members**, **Message Content** and **Presence** privileged intents enabled
- A Discord server with the following set up:
  - A clan leader role, a co leader role and one or more staff roles
  - A category for clan channels
  - Channels for clan requests, clan logs and clan commands

The bot needs permission to manage roles and channels. Make sure the bot's own role sits above the clan, leader and co leader roles in your server's role list, otherwise it can't assign them.

### Installation

```bash
git clone https://github.com/[your-username]/[repo-name].git
cd [repo-name]
pip install -r requirements.txt
```

### Configuration

Copy the example config and fill in your own values:

```bash
cp config.example.json config.json
```

| Key | Description |
| --- | --- |
| `Bot Token` | Your Discord bot token |
| `Bot Prefix` | Prefix for commands, for example `!` |
| `MongoDB Connection String` | Connection string for your MongoDB database |
| `MongoDB Database Name` | Name of the database the bot should use |
| `Guild ID` | ID of your Discord server |
| `Embed Colour` | Hex colour used for the bot's embeds |
| `ClanCategoryID` | ID of the category for clan channels |
| `Roles` > `Clan Leader Role` | ID of the clan leader role |
| `Roles` > `Co-Leader Role` | ID of the co leader role |
| `Roles` > `Staff Roles` | List of role IDs that count as staff |
| `Channels` > `Accept Clan Request ChannelID` | Channel where clan applications are sent to staff |
| `Channels` > `Clan Logs ChannelID` | Channel where clan activity is logged |
| `Channels` > `Clan Commands ChannelID` | Channel for clan commands |

**Never commit `config.json` or share your bot token or database password.** It is already listed in `.gitignore`. If a token ever leaks, reset it straight away in the Developer Portal.

### Running the Bot

```bash
python bot.py
```

## Project Structure

```
.
├── bot.py                 # Bot setup, database connection and error handling
├── config.json            # Your settings (not committed)
├── config.example.json    # Template for config.json
├── requirements.txt
├── cogs/                  # Command modules, loaded automatically
│   ├── claninfo.py
│   ├── clanCreate.py
│   ├── clanDisband.py
│   ├── clanInvite.py
│   ├── clanLeave.py
│   ├── clanRemove.py
│   ├── help.py
│   ├── promoteDemote.py
│   └── staffCommands.py
└── utils/                 # Shared helpers
    ├── clanUtilities.py
    └── miscUtilities.py
```

## Contributing

Suggestions and improvements are welcome. Open an issue to report a bug or request a feature, or submit a pull request if you would like to contribute a fix.
