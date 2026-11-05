import logging
import sys
import os
project_name = "companybot"
class Custom_logger:
    def __init__(self, path = "./logs/"):
        if not os.path.exists(path):
            os.makedirs(path)

        log_format = logging.Formatter(
            fmt = "%(asctime)s [%(levelname)s] (%(name)s -> %(message)s)",
            datefmt = "%Y-%m-%d %H:%M:%S"
        )

        console = logging.StreamHandler(sys.stdout)
        console.setFormatter(log_format)

        filehandler = logging.FileHandler(filename=os.path.join(path+"logfile.log"), encoding = "utf-8")
        filehandler.setFormatter(log_format)

        self.root = logging.getLogger(project_name)
        self.root.setLevel(logging.INFO)
        self.root.addHandler(console)
        self.root.addHandler(filehandler)

    def get_logger(self, loggername: str):
        if not loggername.startswith(project_name):
            return logging.getLogger(f"{project_name}.{loggername}")
        return logging.getLogger(project_name)
    