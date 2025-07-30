import logging
import os

def setup_logger(name, log_file='parser.log', level=logging.INFO):
    os.makedirs("logs", exist_ok=True)

    logger = logging.getLogger(name)
    logger.setLevel(level)

    hendler = logging.FileHandler(f"logs/{__name__}.log", encoding='utf-8')
    formatter = logging.Formatter("%(name)s %(asctime)s %(levelname)s %(message)s")

    hendler.setFormatter(formatter)
    logger.addHandler(hendler)
    
    return logger
