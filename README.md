# OpenBB Bot - Discord Edition

The [OpenBB Bot](http://my.openbb.co/app/bot) is a chatting bot that retrieves financial data on Discord and Telegram.

If you want to use our hosted version which is 100% free, go to http://my.openbb.co/app/bot.

Otherwise, the remainder of this document will explain how you can self-host our Discord bot.

We have open source our framework so that users are able to build their own Discord bots. We are relying on the [OpenBB Platform](HTTP://my.openbb.co/app.sdk) and [Disnake](https://github.com/DisnakeDev/disnake).

## Add your own OpenBB Bot to your server of interest

1. Go to https://discord.com/developers/applications
2. Click on "New Application"
3. Select a name for the application and agree to the ToS
4. Add an image so that you can easily recognize the bot on Discord, and save changes
5. On the "Settings" sidebar, go to "OAuth2"
6. Copy the ClientID on that page
7. Go to https://discord.com/oauth2/authorize?client_id=<CLIENTID>&scope=bot and replace `<CLIENTID>` by the one you copied in the previous step
8. Make sure you select the Server you are interested in having the bot in
9. On the "Settings" sidebar, go to "Bot"
10. Click on "Reset Token" and copy the Token ID - this will be necessary when running the bot.

## Configure your own OpenBB Bot

1. Update and rename the `.env.example` file to `.env`
2. In this `.env` file set `DISCORD_BOT_TOKEN` with the Token ID previously copied
3. If you don't have an OpenBB Hub account, go to http://my.openbb.co 
5. Once you do go the [OpenBB SDK - PAT (personal access token) page](http://my.openbb.co/app/sdk/pat) and copy the PAT
6. In the `.env` file set `OPENBB_HUB_PAT` with the PAT previously copied

One of the reasons you rely on the OpenBB Hub PAT is that it manages all of your API keys on your behalf once you want to access data using OpenBB. So make sure you have your API keys set in http://my.openbb.co/sdk/api-keys.

## Run your own OpenBB Bot

1. Install the requirements

```bash
poetry install
```

2. Run your own OpenBB Bot

```bash
uvicorn main:app --reload
```

## How to make your own custom commands for the OpenBB Bot

Create a new file or edit a pre-existing file in the folder: `bot/cmds`.
  
Let's assume that we create a new file called `stockCandlestick_cmds.py`. We will go step-by-step over what this file should contain:

1. Import all necessary python libraries

```python
import traceback

from openbb import obb

import disnake
from disnake.ext import commands
from datetime import datetime, timedelta

from bot.showview import ShowView
from utils.pywry_figure import PyWryFigure
```

2. Create a new class associated with the file which may hold multiple commands

```python
class CandlestickChartsCommands(commands.Cog):
    """Candlestick Charting commands."""
```

3. Within that class, initialize the class as follows

```python
def __init__(self, bot: commands.Bot):
        self.bot = bot
```

4. Within that class create a command. An example with several comments to explain the structure follows

```python
# Ensure that the name and the method name is the same
# this will be what the user utilizes to invoke the command from Discord
@commands.slash_command(name="candle")
async def candle(
    self,  # inherits from the class
    inter: disnake.AppCmdInter,  # comes from disnake and is used to run the command
    # custom commands
    ticker: str,  # user can type anything but this parameter is required
    interval: str = commands.Param(  # user can only select between '1day', '15min' and '5min'
        choices=[
            "1day",
            "15min",
            "5min",
        ],
        default="1day",  # if the user doesn't select any, by default '1day' is set
    ),
    days: int = 200,  # user has to select an integer, by default 200 is selected
):
    """Shows a daily candlestick chart for the ticker provided.

    Parameters
    -----------
    ticker: Stock Ticker
    interval: Select whether to show 1day, 15min, or 5min intervals
    days: Number of days in the past to show
    """

    # Ensure the docstring above is added
    # so that the users know what each command and parameter corresponds to.

    try:
        # Ensures the data can be retrieved with disnake
        await inter.response.defer()

        # Handle hardcoded parameters, e.g. data provider coming from OpenBB
        provider = "fmp" # can also be 'polygon' or 'intrinio'

        # Pre-processing of parameters, in case it needs to be processed before calling OpenBB
        ticker = ticker.upper()
        params = {
            "symbol": ticker,
            "provider": provider,
            "start_date":  (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d"),
            "end_date": datetime.now().strftime("%Y-%m-%d"),
            "interval": interval,
            "chart": True,
        }

        # Get the data from OpenBB
        data = obb.stocks.load(**params).chart.content

        # Format this data to be displayed on Discord
        title = f"{ticker} {interval.replace('1day', 'Daily')}"

        fig = (
            PyWryFigure()
            .update(data)
            .update_layout(
                margin=dict(l=80, r=10, t=40, b=20),
                paper_bgcolor="#111111",
                plot_bgcolor="rgba(0,0,0,0)",
                height=762,
                width=1430,
                title=dict(text=title, x=0.5),
                xaxis=dict(tick0=0.5, tickangle=0),
            )
        )

        y_min, y_max = min(fig.data[0].low), max(fig.data[0].high)
        y_range = y_max - y_min
        y_min -= y_range * 0.2
        y_max += y_range * 0.08

        fig.update_layout(yaxis=dict(range=[y_min, y_max], autorange=False))

        # The response must be a Dictionary with key "plots", "embeds" or "images_list"
        response: dict = {"plots": fig.prepare_image()}

    except Exception as e:
        # In case there's an exception we want the error to be printed in the user's console
        traceback.print_exc()
        # This returns the error as a string to the Discord so that the user can see what happened
        # this is extremely useful when debugging
        return await ShowView().discord(inter, "candle", str(e), error=True)

    This handles the command rendering on Discord
    await ShowView().discord(inter, "candle", response, no_embed=True)
```

5. Within that class, create as many methods as you wish

6. Finally, create a `setup` function that adds this class to the OpenBB Bot instance

```python
def setup(bot: commands.Bot):
    bot.add_cog(CandlestickChartsCommands(bot))
```
