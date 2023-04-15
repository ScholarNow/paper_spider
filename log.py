import logging
from datetime import datetime

from pytz import timezone


def timetz(*args):
    return datetime.now(tz).timetuple()


tz = timezone('Asia/Shanghai')
logging.Formatter.converter = timetz

logging.basicConfig(
    format="[%(levelname)s]-%(asctime)s - %(filename)s:%(lineno)d - %(message)s",
    datefmt='%Y-%m-%d %H:%M:%S',
    level=logging.INFO,
)
getLogger = logging.getLogger
