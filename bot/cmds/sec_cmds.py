import traceback

from openbb import obb

import pandas as pd
import disnake
from disnake.ext import commands
from datetime import datetime, timedelta
from typing import List, Optional

from bot.showview import ShowView
from models.api_models import EmbedField
from utils.pywry_figure import PyWryFigure


async def sec_form_autocomplete(inter, form: str):
    """Autocomplete for SEC forms"""
    tlow = form.upper()
    sec_forms = [
        '1', '1-A', '1-E', '1-K', '1-N', '1-SA', '1-U', '1-Z', '10',
        '10-D', '10-K', '10-M', '10-Q', '11-K', '12b-25', '13F', '13H',
        '144', '15', '15F', '17-H', '18', '18-K', '19b-4', '19b-4(e)',
        '19b-7', '2-E', '20-F', '24F-2', '25', '3', '4', '40-F', '5',
        '6-K', '7-M', '8-A', '8-K', '8-M', '9-M', 'ABS-15G', 'ABS-EE',
        'ABS DD-15E', 'ADV', 'ADV-E', 'ADV-H', 'ADV-NR', 'ADV-W', 'ATS',
        'ATS-N', 'ATS-R', 'BD', 'BD-N', 'BDW', 'C', 'CA-1', 'CB',
        'CFPORTAL', 'CRS', 'CUSTODY', 'D', 'F-1', 'F-10', 'F-3', 'F-4',
        'F-6', 'F-7', 'F-8', 'F-80', 'F-N', 'F-X', 'ID', 'MA', 'MA-I',
        'MA-NR', 'MA-W', 'MSD', 'MSDW', 'N-14', 'N-17D-1', 'N-17f-1',
        'N-17f-2', 'N-18f-1', 'N-1A', 'N-2', 'N-23c-3', 'N-27D-1', 'N-3',
        'N-4', 'N-5', 'N-54A', 'N-54C', 'N-6', 'N-6EI-1', 'N-6F', 'N-8A',
        'N-8B-2', 'N-8B-4', 'N-8F', 'N-CEN'
    ]
    return [
        form for form in sec_forms if form.startswith(tlow)
    ][:24]

class SECCommands(commands.Cog):
    """SEC commands."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.slash_command(name="sec")
    async def sec(
        self,
        inter: disnake.AppCmdInter,
        ticker: str,
        sec_form: str = commands.Param(
            default="10-K", # We need to fix SDK so we can use None here
            autocomplete=sec_form_autocomplete,
        ),
    ):
        """Retrieves last SEC link for the ticker provided.
        
        Parameters
        -----------
        ticker: Stock Ticker
        sec_form: SEC filing type.
        """

        try:
            await inter.response.defer()

            # Pre-processing of parameters
            ticker = ticker.upper()
            
            # Get the data
            params = {
                "symbol": ticker,
                "type": sec_form,
            }
            
            data = obb.stocks.dd.sec(**params).to_dataframe().head(5)
            
            embeds: List[EmbedField] = []
            embeds.append(
                EmbedField(
                    title=f"{ticker}",
                )
            )

            for _, row in data.iterrows():
                filling_date = pd.to_datetime(row["filling_date"]).strftime("%Y-%m-%d")
                final_link = row["final_link"]
                sec_type = row["type"]

                embeds.append(
                    EmbedField(
                        title=f"{sec_type} filled on {filling_date}",
                        description=f"[Filling document]({final_link})",
                    )
                )

            # Format for display
            #response: dict = {"plots": fig.prepare_image()}
            response: dict = {
                "embeds": embeds,
            }

        except Exception as e:
            traceback.print_exc()
            return await ShowView().discord(inter, "sec", str(e), error=True)

        await ShowView().discord(inter, "sec", response, no_embed=True)


def setup(bot: commands.Bot):
    bot.add_cog(SECCommands(bot))
