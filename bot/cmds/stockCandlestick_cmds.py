import traceback

import disnake
from disnake.ext import commands

from bot.helpers import chart_response
from bot.showview import ShowView


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

        try:
            await inter.response.defer()

            response = chart_response(ticker, "1day", 200)

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

        try:
            await inter.response.defer()

            response = chart_response(ticker, "5min", 4)

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
        try:
            await inter.response.defer()

            response = chart_response(ticker, "15min", 4)

        except Exception as e:
            traceback.print_exc()
            return await ShowView().discord(inter, "c15m", str(e), error=True)

        await ShowView().discord(inter, "c15m", response, no_embed=True)


def setup(bot: commands.Bot):
    bot.add_cog(CandlestickChartsCommands(bot))
