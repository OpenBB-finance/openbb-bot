import traceback
from datetime import datetime, timedelta

import disnake
from disnake.ext import commands
from openbb import obb

from bot.showview import ShowView
from utils.pywry_figure import PyWryFigure


def candlestick_chart(params: dict, title: str) -> PyWryFigure:
    fig: PyWryFigure = PyWryFigure().update(obb.stocks.load(**params).chart.content)

    fig.update_layout(
        title=dict(text=title, x=0.5),
        margin=dict(l=20, r=20, t=40, b=20),
        width=900,
        height=600,
        xaxis=dict(tick0=0.5, tickangle=0),
    )

    return fig


class CandlestickChartsCommands(commands.Cog):
    """Candlestick Charting commands."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.slash_command(name="cd")
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

            fig = candlestick_chart(params, f"{ticker.upper()} Daily")
            response = {"plots": fig.prepare_image()}

        except Exception as e:
            traceback.print_exc()
            return await ShowView().discord(inter, "cd", str(e), error=True)

        await ShowView().discord(inter, "cd", response, no_embed=True)

    @commands.slash_command(name="cc")
    async def cc(
        self,
        inter: disnake.AppCmdInter,
        ticker: str,
    ):
        """Shows a 5 minute candlestick chart for the ticker provided.

        Parameters
        -----------
        ticker: Stock Ticker
        """
        params = {
            "symbol": ticker.upper(),
            "start_date": (datetime.now() - timedelta(days=2)).strftime("%Y-%m-%d"),
            "end_date": datetime.now().strftime("%Y-%m-%d"),
            "interval": "5min",
            "chart": True,
        }

        try:
            await inter.response.defer()

            fig = candlestick_chart(params, f"{ticker.upper()} 5min")
            response = {"plots": fig.prepare_image()}

        except Exception as e:
            traceback.print_exc()
            return await ShowView().discord(inter, "cc", str(e), error=True)

        await ShowView().discord(inter, "cc", response, no_embed=True)

    @commands.slash_command(name="c15m")
    async def c15m(
        self,
        inter: disnake.AppCmdInter,
        ticker: str,
    ):
        """Shows a 15 minute candlestick chart for the ticker provided.

        Parameters
        -----------
        ticker: Stock Ticker
        """
        params = {
            "symbol": ticker.upper(),
            "start_date": (datetime.now() - timedelta(days=2)).strftime("%Y-%m-%d"),
            "end_date": datetime.now().strftime("%Y-%m-%d"),
            "interval": "15min",
            "chart": True,
        }

        try:
            await inter.response.defer()

            fig = candlestick_chart(params, f"{ticker.upper()} 15min")
            response = {"plots": fig.prepare_image()}

        except Exception as e:
            traceback.print_exc()
            return await ShowView().discord(inter, "c15m", str(e), error=True)

        await ShowView().discord(inter, "c15m", response, no_embed=True)


def setup(bot: commands.Bot):
    bot.add_cog(CandlestickChartsCommands(bot))
