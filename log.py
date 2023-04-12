import logging

logging.basicConfig(
    format="[%(levelname)s]-%(asctime)s - %(filename)s:%(lineno)d - %(message)s",
    datefmt='%Y-%m-%d %H:%M:%S',
    level=logging.INFO,
)
getLogger = logging.getLogger
