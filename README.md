# Bots

OpennBB Bots Framework using OpenBB SDK and [Disnake](
    https://github.com/DisnakeDev/disnake
)

## How to run the bot

1. Update and rename the `.env.example` file to .env

2. Install the requirements

```bash
poetry install
```


3. Run the bot

```bash
uvicorn bot.main:app --reload
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
    """Description of the command. (This shows up in the help command)

    ** We add the parameters here and describe them so they show in slash command help.
    Parameters
    -----------
    ticker: The ticker of the stock you want to get the option chain for.
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
