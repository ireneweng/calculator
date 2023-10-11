import logging


def create_logger():
    logging.basicConfig(
        filename="calculator_log.txt",
        level=logging.DEBUG,
        format="[%(asctime)s] %(filename)-20s:%(lineno)d %(levelname)s - %(message)s",
        datefmt="%H:%M:%S",
    )

    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        "%(filename)-20s:%(lineno)d %(levelname)s - %(message)s",
    )
    console.setFormatter(formatter)
    logging.getLogger("").addHandler(console)

    logger = logging.getLogger(__name__)
    return logger
