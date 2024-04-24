import logging


logging.basicConfig(
    filename=f".\logs\log.log",
    filemode='a',
    format='%(asctime)s - %(levelname)s : %(message)s',
    datefmt='%m/%d/%Y %I:%M:%S %p',
    level=logging.INFO
)