import uuid
from datetime import datetime, timedelta

# from bot.config import redis_conn

# from utils.supported_classes import SUPPORTED_TICKERS


def datetime_now(previous: bool = False) -> datetime:
    """Returns datetime.now() as eastern timezone, if previous is True, returns
        previous day

    Parameters
    ----------
    previous : bool, optional
        If True, returns previous day, else returns current day. The default is
        False.
    """
    output = datetime.now().astimezone()
    if previous:
        output -= timedelta(days=1)
    return output


def dt_replace(hour: int, minute: int, second: int) -> datetime:
    """Returns datetime.now() as eastern timezone, but with the given hour,
        minute, and second

    Parameters
    ----------
    hour: `int`
        Hour to set
    minute: `int`
        Minute to set
    second: `int`
        Second to set
    """
    output = datetime.now().astimezone()
    output = output.replace(hour=hour, minute=minute, second=second)

    return output


# def redis_cache(
#     redis_key: str,
#     data=None,
#     expire=60,
#     redis_client=redis_conn,
# ):
#     """Check if key is in redis cache, if not, add it and return data

#     Parameters
#     ----------
#     redis_key : str
#         Key to check in redis cache
#     data : object, optional
#         Data to add to redis cache. The default is None.
#     expire : int, optional
#         Expiration time in seconds. The default is redis_cache_seconds().
#     redis_client : redis.Redis, optional
#         Redis client. The default is imps.redis_conn.

#     Returns
#     -------
#     object
#         Data from redis cache if it exists, else data
#     """

#     if redis_client.get(redis_key):
#         return ujson.loads(redis_client.get(redis_key))

#     if data is None:
#         return False

#     redis_client.set(redis_key, ujson.dumps(data), ex=int(expire) if expire else None)

#     return data


def uuid_get() -> str:
    """Returns a UUID

    Returns
    -------
    str
        UUID Ex. e48c4851a42711ec8e11fb53fa4c20e5
    """
    rand = str(uuid.uuid4()).replace("-", "")
    return rand
