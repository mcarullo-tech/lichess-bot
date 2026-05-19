<div align="center">

  ![lichess-bot](https://github.com/lichess-bot-devs/lichess-bot-images/blob/main/lichess-bot-icon-400.png)

  <h1>lichess-bot</h1>

  A bridge between [lichess.org](https://lichess.org) and bots.
  <br>
  <strong>[Explore lichess-bot docs »](https://github.com/lichess-bot-devs/lichess-bot/wiki)</strong>
  <br>
  <br>
  [![Python Build](https://github.com/lichess-bot-devs/lichess-bot/actions/workflows/python-build.yml/badge.svg)](https://github.com/lichess-bot-devs/lichess-bot/actions/workflows/python-build.yml)
  [![Python Test](https://github.com/lichess-bot-devs/lichess-bot/actions/workflows/python-test.yml/badge.svg)](https://github.com/lichess-bot-devs/lichess-bot/actions/workflows/python-test.yml)
  [![Mypy](https://github.com/lichess-bot-devs/lichess-bot/actions/workflows/mypy.yml/badge.svg)](https://github.com/lichess-bot-devs/lichess-bot/actions/workflows/mypy.yml)

</div>

## Overview

This repository is a fork of [lichess-bot](https://github.com/lichess-bot-devs/lichess-bot) by lichess-bot-devs. It preserves the original bridge between the [Lichess Bot API](https://lichess.org/api#tag/Bot) and chess engines, and adds a custom homemade bot implementation in `homemade.py`.

With lichess-bot, you can create and operate a bot on lichess. Your bot will be able to play against humans and bots alike, and you will be able to view games live on lichess.

See also the lichess-bot [documentation](https://github.com/lichess-bot-devs/lichess-bot/wiki) for further usage help.

## This fork includes: MattysBot

This fork ships with a homemade engine named `MattysBot` in `homemade.py`.

### What `MattysBot` does
- Implements a depth-3 minimax search over legal moves.
- Uses alpha-beta pruning to reduce the search space.
- Evaluates positions with material values plus piece-square tables.
- Uses separate king tables for middle-game and endgame evaluation.
- Detects endgame positions with a simple rule:
  - no queens on the board, or
  - no rooks and at most two minor pieces.
- Selects the best move for White by maximizing the score, and the best move for Black by minimizing it.
- Falls back to a random legal move if no best move is found.
- Prints the chosen move and evaluation to the console for debugging.

### How `MattysBot` scores a position
- Pawns: 100
- Knights: 320
- Bishops: 330
- Rooks: 500
- Queens: 900
- King: 20000

Every piece also gets a positional bonus from piece-square tables.
A positive score favors White, and a negative score favors Black.

## Features
Supports:
- Every variant and time control
- UCI, XBoard, and Homemade engines
- Matchmaking (challenging other bots)
- Offering draws and resigning
- Participating in tournaments
- Accepting move takeback requests from opponents
- Saving games as PGN
- Local & Online opening books
- Local & Online endgame tablebases

Can run on:
- Python 3.10 and later
- Windows, Linux and MacOS
- Docker

## Play MattysBot

To play the homemade bot included in this fork:

1. Copy `config.yml.default` to `config.yml`.
2. Set the engine protocol to `homemade`.
3. Set the engine name to `MattysBot`.

Example `config.yml` engine section:

```yaml
engine:
  protocol: "homemade"
  name: "MattysBot"
  dir: "./"
  debug: false
```

4. Configure the rest of the bot as usual, including your Lichess OAuth token, time controls, and challenge preferences.
5. Run the bot from the repository root:

```bash
python lichess-bot.py
```

6. Challenge the bot on lichess or wait for it to accept incoming games according to your `challenge` settings.

> Note: To play on Lichess, you must use a bot account and a valid OAuth token. Follow the upstream documentation to upgrade your account and create the token.

## Steps
1. [Install lichess-bot](https://github.com/lichess-bot-devs/lichess-bot/wiki/How-to-Install)
2. [Create a lichess OAuth token](https://github.com/lichess-bot-devs/lichess-bot/wiki/How-to-create-a-Lichess-OAuth-token)
3. [Setup the engine](https://github.com/lichess-bot-devs/lichess-bot/wiki/Setup-the-engine)
4. [Configure lichess-bot](https://github.com/lichess-bot-devs/lichess-bot/wiki/Configure-lichess-bot)
5. [Upgrade to a BOT account](https://github.com/lichess-bot-devs/lichess-bot/wiki/Upgrade-to-a-BOT-account)
6. [Run lichess-bot](https://github.com/lichess-bot-devs/lichess-bot/wiki/How-to-Run-lichess%E2%80%90bot)

## Advanced options
- [Create a homemade engine](https://github.com/lichess-bot-devs/lichess-bot/wiki/Create-a-homemade-engine)
- [Add extra customizations](https://github.com/lichess-bot-devs/lichess-bot/wiki/Extra-customizations)

<br />

## Acknowledgements
Thanks to the Lichess team, especially T. Alexander Lystad and Thibault Duplessis for working with the LeelaChessZero team to get this API up. Thanks to [Niklas Fiekas](https://github.com/niklasf) and his [python-chess](https://github.com/niklasf/python-chess) code which allows engine communication seamlessly.

## License
lichess-bot is licensed under the AGPLv3 (or any later version at your option). Check out the [LICENSE file](https://github.com/lichess-bot-devs/lichess-bot/blob/master/LICENSE) for the full text.

## Citation
If this software has been used for research purposes, please cite it using the "Cite this repository" menu on the right sidebar. For more information, check the [CITATION file](https://github.com/lichess-bot-devs/lichess-bot/blob/master/CITATION.cff).
