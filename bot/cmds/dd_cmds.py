import traceback

import disnake
from disnake.ext import commands
from openbb import obb

from bot.showview import ShowView

from ..run_bot import OBB_Bot


class DueDiligenceCommands(commands.Cog):
    """Due Diligence commands."""

    def __init__(self, bot: "OBB_Bot"):
        self.bot = bot
        self.plot_df = bot.plot_df

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

            df = (
                obb.stocks.fa.income(ticker, period=period)
                .to_dataframe()
                .drop(["cik", "calendar_year"], axis=1)
            )
            df.columns = df.columns.str.replace("_", " ").str.title()

            df = df.tail(1).T
            df.columns = [d.strftime("%Y-%m-%d") for d in df.columns]
            data = df[
                [str(v).replace(".", "", 1).isdigit() for v in df[df.columns[0]].values]
            ]

            fig = self.plot_df(
                data,
                fig_size=(650, (30 + (40 * len(data.index)))),
                print_index=True,
                col_width=[7, 5],
                nums_format=[data.columns[0]],
                cell_align=["left", "right"],
            )

        except Exception as e:
            traceback.print_exc()
            return await ShowView().discord(inter, "income", str(e), error=True)

        await ShowView().discord(
            inter, "income", {"title": "Income", "plots": fig.prepare_table()}
        )


def setup(bot: "OBB_Bot"):
    bot.add_cog(DueDiligenceCommands(bot))
