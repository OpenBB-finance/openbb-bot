from datetime import datetime, timedelta

from openbb import obb

from models.api_models import MainModel
from utils.pywry_figure import PyWryFigure


def datetime_now(days: int = 0) -> str:
    """
    Get the current datetime in the format of YYYY-MM-DD.

    Parameters
    -----------
    days: int
        Number of days to subtract from the current datetime.

    Returns
    -------
    str
        The current datetime in the format of YYYY-MM-DD.
    """

    return (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")


def chart_response(ticker: str, interval: str, days: int = 0) -> MainModel:
    """
    Get a candlestick chart for the ticker provided.

    Parameters
    -----------
    ticker: str
        The ticker to get the chart for.
    interval: str
        The interval to get the chart for.
    days: int
        The number of days to look back. Default is 0.

    Returns
    -------
    PyWryFigure
        The candlestick chart for the ticker provided.
    """
    ticker = ticker.upper()

    params = {
        "symbol": ticker,
        "provider": "fmp",
        "start_date": datetime_now(days=days),
        "end_date": datetime_now(),
        "interval": interval,
        "chart": True,
    }

    title = f"{ticker} {interval.replace('1day', 'Daily')}"

    fig = (
        PyWryFigure()
        .update(obb.stocks.load(**params).chart.content)
        .update_layout(
            title=dict(text=title, x=0.5),
            margin=dict(l=20, r=20, t=40, b=20),
            width=900,
            height=600,
            xaxis=dict(tick0=0.5, tickangle=0),
        )
    )

    y_min, y_max = min(fig.data[0].low), max(fig.data[0].high)
    y_range = y_max - y_min
    y_min -= y_range * 0.2
    y_max += y_range * 0.08

    fig.update_layout(yaxis=dict(range=[y_min, y_max], autorange=False))

    return {"plots": fig.prepare_image()}
