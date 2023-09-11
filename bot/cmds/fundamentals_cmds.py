import traceback

import disnake
from disnake.ext import commands
from openbb import obb

from bot.showview import ShowView

from ..run_bot import OBB_Bot


class FundamentalsCommands(commands.Cog):
    """Fundamentals commands."""

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

            ticker = ticker.upper()

            df = (
                obb.stocks.fa.income(ticker, period=period)
                .to_dataframe()
                .drop(["cik", "calendar_year"], axis=1)
            )
            df.columns = df.columns.str.replace("_", " ").str.title()

            df = df.tail(1).T
            df.columns = [d.strftime("%Y-%m-%d") for d in df.columns]
            df_update = df[
                [str(v).replace(".", "", 1).isdigit() for v in df[df.columns[0]].values]
            ]
            # Filter out rows
            df_update2 = df_update[~df_update.index.str.contains("Ratio")]
            data = df_update2[~df_update2.index.str.contains("Average")]

            # Define a dictionary of replacements
            replacement_dict = {
                "Research And Development Expenses": "R&D Expenses",
                "General And Administrative Expenses": "G&A Expenses",
                "Selling And Marketing Expenses": "S&M Expenses",
                "Selling General And Administrative Expenses": "SG&A Expenses",
                "Eps": "EPS",
                "Eps Diluted": "EPS Diluted",
                "Ebitda": "EBITDA",
            }

            # Apply the replacements using a list comprehension
            data.index = [replacement_dict.get(i, i) for i in data.index]

            font_color = list()
            for val in data[data.columns[0]].values:
                sval = str(val).split(".")[0]
                if "-" in sval:
                    sval = sval.replace("-", "")
                    if len(sval) > 9:
                        font_color.append("rgb(248,113,113)")
                    elif len(sval) > 6:
                        font_color.append("rgb(220,38,38)")
                    elif len(sval) > 3:
                        font_color.append("rgb(185,28,28)")
                    else:
                        font_color.append("white")
                elif len(sval) > 9:
                    font_color.append("rgb(74,222,128)")
                elif len(sval) > 6:
                    font_color.append("rgb(22,163,74)")
                elif len(sval) > 3:
                    font_color.append("rgb(21,128,61)")
                else:
                    font_color.append("white")

            fig = self.plot_df(
                data,
                fig_size=(650, (30 + (45 * len(data.index)))),
                print_index=True,
                col_width=[8, 5],
                nums_format=[data.columns[0]],
                cell_align=["left", "right"],
                cell_font_color=[["white"] * len(data), font_color],
            )

        except Exception as e:
            traceback.print_exc()
            return await ShowView().discord(inter, "income", str(e), error=True)

        await ShowView().discord(
            inter, "income", {"title": f"{ticker} Income", "plots": fig.prepare_table()}
        )

def setup(bot: "OBB_Bot"):
    bot.add_cog(FundamentalsCommands(bot))
