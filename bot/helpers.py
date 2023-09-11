from math import floor
from typing import List, Optional, Tuple, Union

import numpy as np
import pandas as pd

from utils.pywry_figure import PyWryFigure

PLT_TBL_HEADER = dict(
    height=32,
    fill_color="rgb(30, 30, 30)",
    font_color="white",
    font_size=28,
    line_color="#6e6e6e",
    line_width=1,
)
PLT_TBL_CELLS = dict(
    height=40,
    font_size=28,
    fill_color="rgb(50, 50, 50)",
    font_color="white",
    line_color="#6e6e6e",
    line_width=0,
)
PLT_TBL_FONT = dict(size=28)
PLT_TBL_FONT_COLOR = "white"
PLT_TBL_ROW_COLORS: Optional[Tuple[str, str]] = (
    "#333333",
    "#242424",
)


def numerize(num, round_decimal=2) -> str:
    """Format a long number"""
    if num is None:
        return ""

    if isinstance(num, float):
        magnitude = 0
        while abs(num) >= 1000:
            magnitude += 1
            num /= 1000.0

        string_fmt = f".{round_decimal}f"

        num_str = f"{num:{string_fmt}}"

        return f"{num_str}{' KMBTP'[magnitude]}".strip()
    if isinstance(num, (np.int64, int)):
        num = str(num)
    if num.lstrip("-").isdigit():
        num = int(num)
        num /= 1.0
        magnitude = 0
        while abs(num) >= 1000:
            magnitude += 1
            num /= 1000.0

        string_fmt = f".{round_decimal}f"
        num_str = f"{num:{string_fmt}}"

        return f"{num_str}{' KMBTP'[magnitude]}".strip()
    return num


# pylint: disable=R0913
def plot_df(
    df: Union[pd.Series, pd.DataFrame],
    print_index: bool = False,
    multi_index: bool = False,
    title: Optional[dict] = None,
    tbl_header_visible: bool = True,
    tbl_header: Optional[dict] = PLT_TBL_HEADER,
    tbl_cells: Optional[dict] = PLT_TBL_CELLS,
    row_fill_color: Optional[Tuple[str, str]] = PLT_TBL_ROW_COLORS,
    col_width: Optional[Union[int, float, List[Union[int, float]]]] = None,
    fig_size: Optional[Tuple[int, int]] = None,
    cell_align: Optional[List[str]] = None,
    cell_font_color: Optional[List[str]] = None,
    cells_format: Optional[List[str]] = None,
    nums_format: Optional[List[str]] = None,
    **layout_kwargs,
) -> PyWryFigure:
    """Plots a pd.Series or pd.DataFrame.

    Parameters
    ----------
    df : Union[pd.Series, pd.DataFrame]
        Series or dataframe to be plotted.
    print_index : bool, default False
        If `True`, prints the dataframe's index. `df.index.name` will become the index
        column header.
    title : dict, default None
        A dict possibly containing `plotly` key/value pairs:
        https://plotly.com/python/reference/layout/#layout-title

        More relevant key/value pairs:

        - font_color : color
        - font_family : str
        - font_size : number greater than or equal to 1
        - text : str
        - x : number between or equal to 0 and 1, default 0.5

        Sets the x position with respect to `xref` in normalized coordinates
        from "0" (left) to "1" (right).
        - xanchor : enumerated, one of ("auto", "left", "center", "right"),
        default "auto"

        Sets the title's horizontal alignment with respect to its x position.
        "left" means that the title starts at x, "right" means that the title ends
        at x and "center" means that the title's center is at x. "auto" divides
        `xref` by three and calculates the `xanchor` value automatically based on
        the value of `x`.
    tbl_header_visible : bool, default True,
        If `False`, table header will be invisible. Takes precedence over `tbl_header`
        argument.
    tbl_header, tbl_cells : dict, default None
        A dict possibly containing `plotly` key/value pairs:
        https://plotly.com/python/reference/table/#table-header
        https://plotly.com/python/reference/table/#table-cells

        More relevant key/value pairs:

        - align : enumerated or array of enumerateds,
            one of ("left", "center", "right"), default "center"
        - fill_color : color, default "white"
        - font_color : color or array of colors
        - font_family : str or array of str
        - font_size : number or array of numbers greater than or equal to 1
        - height : number, default 28
        - line_width : number or array of numbers, default 1
    row_fill_color : Tuple[str, str], default None
        Tuple of colors that will be used to alternate row colors. Takes precedence
        over `tbl_cells["fill_color"]`.
    col_width : number or array of numbers, default None
        The width of columns expressed as a ratio. Columns fill the available width
        in proportion of their specified column widths.
    fig_size : Tuple[int, int], default None
        Tuple specifying the `width` and `height` of the figure.
    cell_align : List[str], default None
        List of strings specifying the alignment of each cell.
    cell_font_color : List[str], default None
        List of strings specifying the font color of each cell.
    cells_format : List[str], default None
        List of strings specifying which columns should be formatted.
            -Add '%' in the string to be formatted as a percentage. ex. f"{x:.2f}%"
            -Add '$' in the string to be formatted as a currency. ex. f"${x:.2f}"
            -Add '#' in the string to be formatted as a number with commas. ex. f"{x:,.0f}"
            -otherwise x will be formatted as f"{x:,.2f}".
    nums_format : List[str], default None
        List of strings specifying which columns should be formatted with magnitudes.
            -Add '$' in the string to be formatted as a currency. ex. f"${x:.2f} M"
    **layout_kwargs
        Plotly accepts a large number of layout-related keyword arguments.
        A detailed descriptions is available at
        https://plotly.com/python-api-reference/generated/plotly.graph_objects.Layout.html.

    Returns
    -------
    PyWryFigure
        Returns a figure object.

    """
    df = df.copy()

    def _alternate_row_colors() -> Optional[List[str]]:
        color_list = None
        # alternate row colors
        row_count = len(df)
        if row_fill_color is not None:
            # determine how many rows in `df` and then create a list with alternating
            # row colors
            row_odd_count = floor(row_count / 2) + row_count % 2
            row_even_count = floor(row_count / 2)
            odd_list = [row_fill_color[0]] * row_odd_count
            even_list = [row_fill_color[1]] * row_even_count
            color_list = [x for y in zip(odd_list, even_list) for x in y]
            if row_odd_count > row_even_count:
                color_list.append(row_fill_color[0])

        return color_list

    def _alternate_cell_alignments() -> Optional[List[str]]:
        align_list = ["center"]
        if cell_align is not None:
            align_list = list(cell_align)

        return align_list

    if nums_format is not None:
        for col in nums_format:
            if "$" in col:
                newcol = col.replace("$", "")
                df[newcol] = df[newcol].apply(lambda x: f"${numerize(x)}")
            elif "*" in col:
                newcol = col.replace("*", "")
                df[newcol] = df[newcol].apply(lambda x: f"<b>{numerize(x)}</b>")
            elif "ETH" in col:
                newcol = col.replace("ETH", "")
                df[newcol] = df[newcol].apply(lambda x: f"{numerize(x)} ETH")
            else:
                df[col] = df[col].apply(lambda x: f"{numerize(x)}")

    if cells_format is not None:
        for col in cells_format:
            if "%" in col:
                newcol = col.replace("%", "")
                df[newcol] = df[newcol].apply(lambda x: f"{x:.2f}%")
                df[newcol] = df[newcol].str.replace("nan%", "", regex=False)
            elif "$" in col:
                newcol = col.replace("$", "")
                df[newcol] = df[newcol].apply(lambda x: f"${x:,.2f}")
                df[newcol] = df[newcol].str.replace("$nan", "", regex=False)
            elif "#" in col:
                newcol = col.replace("#", "")
                df[newcol] = df[newcol].apply(lambda x: f"{x:,.0f}")
                df[newcol] = df[newcol].str.replace("nan", "", regex=False)
            else:
                df[col] = df[col].apply(lambda x: f"{x:,.2f}")
                df[col] = df[col].str.replace("nan", "", regex=False)

    def _tbl_values():
        if print_index and not multi_index:
            header_values = [
                f"<b>{x}<b>"
                for x in [
                    df.index.name if df.index.name is not None else "",
                    *df.columns,
                ]
            ]
            cell_values = [df.index, *[df[col] for col in df]]
        elif multi_index:
            header_values = df.columns.tolist()
            cell_values = df.T.values
        else:
            header_values = [f"<b>{x}<b>" for x in df.columns.to_list()]
            cell_values = [df[col] for col in df]

        return header_values, cell_values

    row_color_list = _alternate_row_colors()
    header_vals, cell_vals = _tbl_values()

    if not tbl_header:
        tbl_header = dict()
    tbl_header.update(values=header_vals)

    if not tbl_header_visible:
        tbl_header.update(
            fill_color="white", font_color="white", line_color="white", height=1
        )

    if not tbl_cells:
        tbl_cells = dict()
    tbl_cells.update(
        values=cell_vals,
        fill_color=[row_color_list] * len(df)
        if row_color_list
        else tbl_cells.get("fill_color"),
    )

    fig = PyWryFigure().add_table(header=tbl_header, cells=tbl_cells)

    fig.data[0]["columnwidth"] = col_width if col_width else None

    if not title:
        title = dict()
    title.update(
        x=0.01 if title.get("x") is None else title.get("x"),
        xanchor="left" if title.get("xanchor") is None else title.get("xanchor"),
    )

    fig.update_layout(
        title=title,
        font=layout_kwargs.pop("font", dict(size=28)),
        margin=dict(autoexpand=False, b=20, l=5, r=5, t=5),
        width=fig_size[0] + (fig_size[0] * 0.30)  # type: ignore
        if fig_size[0] > 450  # type: ignore
        else fig_size[0] + 320
        if fig_size
        else None,
        height=fig_size[1] + 250 if fig_size else None,
        autosize=False if col_width else None,
        paper_bgcolor=layout_kwargs.pop("paper_bgcolor", "rgba(0, 0, 0, 0)"),
        **layout_kwargs,
        xaxis=dict(
            rangeslider=dict(visible=False),
        ),
        dragmode="pan",
    )

    cell_align_list = _alternate_cell_alignments()

    fig.update_traces(
        cells=(
            dict(
                align=cell_align_list,
                font=dict(
                    color="white" if cell_font_color is None else cell_font_color
                ),
            )
        )
    )

    return fig
