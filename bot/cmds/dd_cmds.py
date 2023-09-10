import traceback
from typing import List

import disnake
from disnake.ext import commands
from openbb import obb

from bot.showview import ShowView
from models.api_models import EmbedField

from ..helpers import plot_df

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

            df = response.to_dataframe().T
            df_all = df[df.columns[-1]].to_frame()
            data = df_all[[str(v).replace(".", "", 1).isdigit() for v in df_all[df_all.columns[0]].values]]

            print(data)

            fig = plot_df(
                data,
                fig_size=(620, (52 + (40 * len(data.index)))),
                #col_width=[4, 2.4, 3],
                #tbl_header=imps.PLT_TBL_HEADER,
                #tbl_cells=imps.PLT_TBL_CELLS,
                #font=imps.PLT_TBL_FONT,
                #row_fill_color=imps.PLT_TBL_ROW_COLORS,
                #paper_bgcolor="rgba(0, 0, 0, 0)",
            )
            fig.update_traces(
                cells=(
                    dict(
                        align=["center", "right"],
                        font=dict(color="white", size=12),
                    )
                )
            )
            
            '''
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
            '''

        except Exception as e:
            traceback.print_exc()
            return await ShowView().discord(inter, "income", str(e), error=True)

        # await ShowView().discord(inter, "income", {"embeds": embeds})

        await ShowView().discord(inter, "income", {"title": "Income", "plots": fig})


def setup(bot: commands.Bot):
    bot.add_cog(DueDiligenceCommands(bot))
