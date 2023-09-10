import traceback
from typing import List

import disnake
from disnake.ext import commands
from openbb import obb

from bot.showview import ShowView
from models.api_models import EmbedField


class DueDiligenceCommands(commands.Cog):
    """Due Diligence commands."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.slash_command(name="income")
    async def income(
        self,
        inter: disnake.AppCmdInter,
        ticker: str,
        period: str = commands.Param(
            choices=[
                "annual",
                "quarter",
            ],
            default="annual",
        ),
    ):
        """Shows income statement for the ticker provided.

        Parameters
        -----------
        ticker: Stock Ticker
        period: Period to show income statement for
        """

        try:
            await inter.response.defer()

            response = obb.stocks.fa.income(ticker, period=period)

            data = response.results[0].dict()

            embeds: List[EmbedField] = []

            for i, (key, value) in enumerate(data.items()):
                title = key.replace("_", " ").title()
                if i % 3 == 0:
                    embeds.append(
                        EmbedField(
                            title="_ _",
                            description="_ _",
                            inline=False,
                        )
                    )
                embeds.append(
                    EmbedField(
                        title=title,
                        description=f"{value:,.3f}"
                        if isinstance(value, float)
                        else str(value),
                        inline=True,
                    )
                )

        except Exception as e:
            traceback.print_exc()
            return await ShowView().discord(inter, "income", str(e), error=True)

        await ShowView().discord(inter, "income", {"embeds": embeds})


def setup(bot: commands.Bot):
    bot.add_cog(DueDiligenceCommands(bot))
