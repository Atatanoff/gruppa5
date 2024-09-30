import logging
import logging.handlers


log_file = 'log.log'

class Format(logging.Formatter):
    COLORS = {'DEBUG': '\033[94m', 'INFO': '\033[92m', 'WARNING': '\033[93m',
              'ERROR': '\033[91m', 'CRITICAL': '\033[95m'}
    def format(self, record):
        log_fmt = f"{self.COLORS.get(record.levelname, '')}%(filename)-12s %(lineno)-5d - %(levelname)-8s %(message)s\033[0m"
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)

class FormatFile(Format):
    def format(self, record):
        log_fmt = f"{self.COLORS.get(record.levelname, '')} %(asctime)s - %(filename)-12s %(lineno)-5d - %(levelname)-8s %(message)s \033[0m"
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)

def get_logger():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    file_handler = logging.handlers.RotatingFileHandler(log_file, maxBytes=10485760, backupCount=5)
    file_handler.setLevel(logging.ERROR)
    file_handler.setFormatter(FormatFile())

    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.DEBUG)
    stream_handler.setFormatter(Format())



    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)
    return logger

logger = get_logger()
