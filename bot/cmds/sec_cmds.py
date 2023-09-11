import traceback

from openbb import obb

import disnake
from disnake.ext import commands
from datetime import datetime, timedelta

from bot.showview import ShowView
from utils.pywry_figure import PyWryFigure


class SECCommands(commands.Cog):
    """SEC commands."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.slash_command(name="sec")
    async def sec(
        self,
        inter: disnake.AppCmdInter,
        ticker: str,
        type: str = commands.Param(
            choices=[
              '1', '1-A', '1-E', '10-K'
            ],
            default="10-K",
        ),
    ):
        """Shows a daily candlestick chart for the ticker provided.

        Parameters
        -----------
        ticker: Stock Ticker
        type: SEC filing type
          '1',
            '1-A',
            '1-E',
            '1-K',
            '1-N',
            '1-SA',
            '1-U',
            '1-Z', '10', '10-D', '10-K',
            '10-M', '10-Q', '11-K', '12b-25', '13F', '13H',
            '144', '15', '15F', '17-H', '18', '18-K', '19b-4',
            '19b-4(e)', '19b-7', '2-E', '20-F', '24F-2', '25',
            '3', '4', '40-F', '5', '6-K', '7-M', '8-A', '8-K',
            '8-M', '9-M', 'ABS-15G', 'ABS-EE', 'ABS DD-15E', 'ADV',
            'ADV-E', 'ADV-H', 'ADV-NR', 'ADV-W', 'ATS', 'ATS-N', 'ATS-R',
            'BD', 'BD-N', 'BDW', 'C', 'CA-1', 'CB', 'CFPORTAL', 'CRS', 'CUSTODY',
            'D', 'F-1', 'F-10', 'F-3', 'F-4', 'F-6', 'F-7', 'F-8', 'F-80', 'F-N',
            'F-X', 'ID', 'MA', 'MA-I', 'MA-NR', 'MA-W', 'MSD', 'MSDW', 'N-14', 'N-17D-1',
            'N-17f-1', 'N-17f-2', 'N-18f-1', 'N-1A', 'N-2', 'N-23c-3', 'N-27D-1', 'N-3',
            'N-4', 'N-5', 'N-54A', 'N-54C', 'N-6', 'N-6EI-1', 'N-6F', 'N-8A', 'N-8B-2',
            'N-8B-4', 'N-8F', 'N-CEN'
            
        """

        try:
            await inter.response.defer()

            # Hardcoded parameters
            provider = "fmp" # can also be 'polygon' or 'intrinio'

            # Pre-processing of parameters
            ticker = ticker.upper()

            params = {
                "symbol": ticker,
                "type": type,
            }

            # Get the data
            data = obb.stocks.dd.sec(symbol="AAPL", type="10-K").to_dataframe()[["filling_date", "final_link"]]

            # Format for display
            #response: dict = {"plots": fig.prepare_image()}
            response: dict = {}

        except Exception as e:
            traceback.print_exc()
            return await ShowView().discord(inter, "sec", str(e), error=True)

        await ShowView().discord(inter, "sec", response, no_embed=True)


def setup(bot: commands.Bot):
    bot.add_cog(SECCommands(bot))
