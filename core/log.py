import os
import time

class Log:

    def __init__(self):
        self.__format = "%Y-%m-%d %H:%M:%S"


    def write(self, classification, happening,  log_str):
        with open("IP.log", "a") as logger:
            logger.write(f"[{time.strftime(self.__format, time.localtime())}] <{classification}>/<{happening}>: {log_str}\n")

