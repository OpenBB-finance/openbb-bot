import traceback

from openbb import obb

import disnake
from disnake.ext import commands
from datetime import datetime, timedelta

from bot.helpers import chart_response
from bot.showview import ShowView
from models.api_models import MainModel
from utils.pywry_figure import PyWryFigure


class CandlestickChartsCommands(commands.Cog):
    """Candlestick Charting commands."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.slash_command(name="candle")
    async def candle(
        self,
        inter: disnake.AppCmdInter,
        ticker: str,
        interval: str = commands.Param(
            choices=[
                "1day",
                "15min",
                "5min",
            ],
            default="1day",
        ),
        days: int = 200,
        provider: str = commands.Param(
            choices=[
                "fmp",
                "polygon",
                "intrinio"
            ],
            default="fmp",
        ),
    ):
        """Shows a daily candlestick chart for the ticker provided.

        Parameters
        -----------
        ticker: Stock Ticker
        """

        try:
            await inter.response.defer()

            # Pre-processing of parameters
            ticker = ticker.upper()            
            params = {
                "symbol": ticker,
                "provider": provider,
                "start_date":  (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d"),
                "end_date": datetime.now().strftime("%Y-%m-%d"),
                "interval": interval,
                "chart": True,
            }

            # Get the data
            data = obb.stocks.load(**params).chart.content

            # Format for display
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

            response: dict = {"plots": fig.prepare_image()}

        except Exception as e:
            traceback.print_exc()
            return await ShowView().discord(inter, "candle", str(e), error=True)

        await ShowView().discord(inter, "candle", response, no_embed=True)


def setup(bot: commands.Bot):
    bot.add_cog(CandlestickChartsCommands(bot))
