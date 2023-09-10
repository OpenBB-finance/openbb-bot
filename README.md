# OpenBB Bot - Discord

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

## How to make custom commands for the bot

1. Create a new file or edit a pre-existing file in the commands folder. (The commands folder is located in the bot's root directory.
Example: bot/cmds)

```python
from datetime import datetime, timedelta
import disnake
from disnake.ext import commands
from openbb import obb

from bot.showview import ShowView
from models.api_models import MainModel
from utils.pywry_figure import PyWryFigure


@commands.slash_command(name="command_name")
async def command_name(
    self,
    inter: disnake.AppCmdInter,
    ticker: str,
):
    """Description of the command. (Displayed in slash command description)

    ** We add the parameters here and describe them so they show in slash command help.
    Parameters
    -----------
    ticker: Stock ticker
    """
    ticker = ticker.upper()
    params = {
        "symbol": ticker,
        "provider": "fmp",
        "start_date": datetime_now(days=days),
        "end_date": datetime_now(),
        "interval": interval,
        "chart": True,
    }
    try:

            title = f"{ticker} {interval.replace('1day', 'Daily')}"

            fig = (
                PyWryFigure()
                .update(obb.stocks.load(**params).chart.content)
                .update_layout(
                    title=dict(text=title, x=0.5),
                    margin=dict(l=20, r=20, t=40, b=20),
                    width=900,
                    height=600,
                    xaxis=dict(tick0=0.5, tickangle=0),
                )
            )

            y_min, y_max = fig.data[0].low.min(), fig.data[0].high.max()
            y_range = y_max - y_min
            y_min -= y_range * 0.2
            y_max += y_range * 0.08

            fig.update_layout(yaxis=dict(range=[y_min, y_max], autorange=False))

            response = {"plots": fig.prepare_image()}

        except Exception as e:
            traceback.print_exc()
            return await ShowView().discord(inter, "c15m", str(e), error=True)

        await ShowView().discord(inter, "c15m", response, no_embed=True)
```
