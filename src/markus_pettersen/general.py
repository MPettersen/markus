import os
import re
import sys
import string
import logging
import secrets
import requests

from typing import Any, Union
from base64 import b64encode, b64decode
from datetime import datetime, timedelta
from collections.abc import Iterable, Iterator


DATE_FORMAT = "%Y-%m-%dT%H:%M:%S.%f"
# Setup root logger
LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO").upper()
logging.basicConfig(
    stream=sys.stdout,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=LOG_LEVEL,
)
LOG = logging.getLogger(__name__)


def check_env(env_key: str, default: str = ""):
    env = os.environ.get(env_key, default)
    if env == "":
        raise Exception(f"Missing environment variable: {env_key}")
    return env


def password_generator(length: int = 12):
    alphabet = string.ascii_letters + string.digits
    password = ''.join(secrets.choice(alphabet) for _ in range(length))
    return password


def encode(s: str):
    return b64encode(s.encode('utf-8')).decode('utf-8')


def decode(s: str):
    return b64decode(s).decode('utf-8')


def camel_to_snake(s: str, upper: bool = True) -> str:
    """
    Convert from camel to snake case.

    Args:
        s (str): A string
        upper (bool): Convert to upper case. Defaults to true

    Returns:
        The snake case version of the input string
    """
    s = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', s)
    if upper:
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s).upper()
    else:
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s).lower()


def batch_list(iterable: Iterable[Any], batch_size: int = 1) -> Iterator[Union[Iterable[Any], Any]]:
    """
    Batch an iterable.

    Args:
        iterable (Iterable): An iterable to be batched
        batch_size (int): The batch size. Defauts to 1

    Yields:
        Iterator[Iterable[Any] | Any]: A subset of the iterable
    """
    length = len(iterable)
    for ndx in range(0, length, batch_size):
        yield iterable[ndx:min(ndx + batch_size, length)]


def get_utc_timestamp(s: str, **kwargs) -> int:
    """
    Get utc timestamp

    Args:
        s (str): A string representation of a date
        delta (int): Number of days to be added to the date. Defaults to 0

    Returns:
        The timestamp of the provided date adjusted for the delta value
    """
    return int(datetime.timestamp(datetime.strptime(s, DATE_FORMAT) + timedelta(**kwargs)) * 1000) if isinstance(s, str) else s


def paginate(url: str, headers: dict, data: list, skip: int = 0, take: int = 100):
    # TODO: Change pageIndex/pageSize to be configurable
    new = requests.get(f"{url}?pageIndex={skip}&pageSize={take}", headers=headers).json()
    if len(new) == 0:
        return data
    else:
        data.extend(new)
        return paginate(url, headers, data, skip + 1)
