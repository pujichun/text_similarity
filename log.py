import logging


def get_logger():
    logger = logging.getLogger()
    fmt = logging.Formatter("%(asctime)s-%(filename)s-[line:%(lineno)d]-%(levelname)s:%(message)s")
    fh = logging.FileHandler("similarly.log")
    sh = logging.StreamHandler()
    fh.setFormatter(fmt)
    sh.setFormatter(fmt)
    logger.addHandler(fh)
    logger.addHandler(sh)
    logger.setLevel("INFO")
    return logger
