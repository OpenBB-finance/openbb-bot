import traceback
from datetime import datetime, timedelta

import disnake
from disnake.ext import commands
from openbb import obb

from bot.showview import ShowView
from utils.pywry_figure import PyWryFigure


class CandlestickChartsCommands(commands.Cog):
    """Candlestick Charting commands."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.slash_command(name="cd")
    @commands.cooldown(rate=1, per=10, type=commands.BucketType.user)
    async def cd(
        self,
        inter: disnake.AppCmdInter,
        ticker: str,
    ):
        """Shows a daily candlestick chart for the ticker provided.

        Parameters
        -----------
        ticker: Stock Ticker
        """
        params = {
            "symbol": ticker.upper(),
            "start_date": (datetime.now() - timedelta(days=200)).strftime("%Y-%m-%d"),
            "end_date": datetime.now().strftime("%Y-%m-%d"),
            "interval": "1day",
            "chart": True,
        }

        try:
            await inter.response.defer()

            fig: PyWryFigure = PyWryFigure().update(
                obb.stocks.load(**params).chart.content
            )

            fig.update_layout(
                title=dict(text=f"{ticker.upper()} Daily", x=0.5),
                margin=dict(l=20, r=20, t=40, b=20),
                width=900,
                height=600,
                xaxis=dict(tick0=0.5),
            )

        except Exception as e:
            traceback.print_exc()
            await ShowView().discord(inter, "cd", str(e), error=True)
            return
        await ShowView().discord(
            inter, "cd", {"plots": fig.prepare_image()}, no_embed=True
        )


def setup(bot: commands.Bot):
    bot.add_cog(CandlestickChartsCommands(bot))
