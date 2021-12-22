#-*- coding: utf-8 -*-
import logging
import logging.handlers
from com.iotcube.util.config import Config

"""
colargulog - Python3 Logging with Colored Arguments and new string formatting style
Written by david.ohana@ibm.com
License: Apache-2.0
"""
class ColorCodes:
    grey = "\x1b[24;21m"
    green = "\x1b[24;32m"
    yellow = "\x1b[33;1m"
    red = "\x1b[31;1m"
    bold_red = "\x1b[31;1m"
    blue = "\x1b[24;34m"
    light_blue = "\x1b[1;36m"
    purple = "\x1b[24;35m"
    reset = "\x1b[0;m"
class ColorizedArgsFormatter(logging.Formatter):
    arg_colors = [ColorCodes.purple, ColorCodes.light_blue]
    level_fields = ["levelname", "levelno"]
    level_to_color = {
        logging.DEBUG: ColorCodes.green,
        logging.INFO: ColorCodes.blue,
        logging.WARNING: ColorCodes.yellow,
        logging.ERROR: ColorCodes.red,
        logging.CRITICAL: ColorCodes.bold_red,
    }

    def __init__(self, fmt: str):
        super().__init__()
        self.level_to_formatter = {}

        def add_color_format(level: int):
            color = ColorizedArgsFormatter.level_to_color[level]
            _format = fmt
            for fld in ColorizedArgsFormatter.level_fields:
                search = "(%\(" + fld + "\).*?s)"
                # _format = re.sub(search, "\\1\x1b[24m", _format)
                _format = f"{color}{_format}{ColorCodes.reset}"
                # _format = re.sub(search, f"{color}\\1{ColorCodes.reset}", _format)
            formatter = logging.Formatter(_format)
            self.level_to_formatter[level] = formatter

        add_color_format(logging.DEBUG)
        add_color_format(logging.INFO)
        add_color_format(logging.WARNING)
        add_color_format(logging.ERROR)
        add_color_format(logging.CRITICAL)

    @staticmethod
    def rewrite_record(record: logging.LogRecord):
        if not BraceFormatStyleFormatter.is_brace_format_style(record):
            return

        msg = record.msg
        msg = msg.replace("{", "_{{")
        msg = msg.replace("}", "_}}")
        placeholder_count = 0
        # add ANSI escape code for next alternating color before each formatting parameter
        # and reset color after it.
        while True:
            if "_{{" not in msg:
                break
            color_index = placeholder_count % len(ColorizedArgsFormatter.arg_colors)
            color = ColorizedArgsFormatter.arg_colors[color_index]
            msg = msg.replace("_{{", color + "{", 1)
            msg = msg.replace("_}}", "}" + ColorCodes.reset, 1)
            placeholder_count += 1

        record.msg = msg.format(*record.args)
        record.args = []

    def format(self, record):
        orig_msg = record.msg
        orig_args = record.args
        formatter = self.level_to_formatter.get(record.levelno)
        self.rewrite_record(record)
        formatted = formatter.format(record)

        # restore log record to original state for other handlers
        record.msg = orig_msg
        record.args = orig_args
        return formatted


class BraceFormatStyleFormatter(logging.Formatter):
    def __init__(self, fmt: str):
        super().__init__()
        self.formatter = logging.Formatter(fmt)

    @staticmethod
    def is_brace_format_style(record: logging.LogRecord):
        if len(record.args) == 0:
            return False

        msg = record.msg
        if '%' in msg:
            return False

        count_of_start_param = msg.count("{")
        count_of_end_param = msg.count("}")

        if count_of_start_param != count_of_end_param:
            return False

        if count_of_start_param != len(record.args):
            return False

        return True

    @staticmethod
    def rewrite_record(record: logging.LogRecord):
        if not BraceFormatStyleFormatter.is_brace_format_style(record):
            return

        record.msg = record.msg.format(*record.args)
        record.args = []

    def format(self, record):
        orig_msg = record.msg
        orig_args = record.args
        self.rewrite_record(record)
        formatted = self.formatter.format(record)

        # restore log record to original state for other handlers
        record.msg = orig_msg
        record.args = orig_args
        return formatted

class Logger(object):
    logger = None

    def __new__(cls):
        if not hasattr(cls,'instance'):
            config = Config()
            appName = config.getConfig('COMMON', 'appname')
            logRootPath = config.getConfig('LOG', 'logpath')

            cls.logger = logging.getLogger()
            cls.logger.setLevel(logging.DEBUG)
            format = '%(asctime)s %(levelname)s %(process)s %(filename)s:%(lineno)d %(message)s'

            coloredFormatter = ColorizedArgsFormatter(format)
            bracedFormatter = BraceFormatStyleFormatter(format)
            
            timedRotatingFileHandler = logging.handlers.TimedRotatingFileHandler(
               f'{logRootPath}/{appName}.log', when='D', encoding='utf-8')
            timedRotatingFileHandler.setFormatter(bracedFormatter)
            timedRotatingFileHandler.setLevel(logging.DEBUG)
            cls.logger.addHandler(timedRotatingFileHandler)
            streamHandler = logging.StreamHandler()
            streamHandler.setFormatter(coloredFormatter)
            streamHandler.setLevel(logging.DEBUG)
            cls.logger.addHandler(streamHandler)
            cls.instance = super(Logger, cls).__new__(cls)
        return cls.instance
    
    def getLogger(cls):
        return cls.logger
