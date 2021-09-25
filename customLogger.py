import sys
import logging

# Code from https://stackoverflow.com/a/28636024/3769258
class LevelFormatter(logging.Formatter):
    def __init__(self, fmt=None, datefmt=None, level_fmts={}):
        self._level_formatters = {}
        for level, format in level_fmts.items():
            # Could optionally support level names too
            self._level_formatters[level] = logging.Formatter(fmt=format, datefmt=datefmt)
        # self._fmt will be the default format
        super(LevelFormatter, self).__init__(fmt=fmt, datefmt=datefmt)

    def format(self, record):
        if record.levelno in self._level_formatters:
            return self._level_formatters[record.levelno].format(record)

        return super(LevelFormatter, self).format(record)

def gen_logging(filename, verbose=False, verbose_flag = None):

    root = logging.getLogger(__name__)

    if filename != "":
        log_f = logging.FileHandler(filename + ".log")
    ch = logging.StreamHandler(sys.stdout)

    root.setLevel(logging.INFO)
    ch.setLevel(logging.INFO)

    if verbose:
        if verbose_flag.lower() == 'debug':
            root.setLevel(logging.DEBUG)
            ch.setLevel(logging.DEBUG)
        elif verbose_flag.lower() == 'info':
            root.setLevel(logging.INFO)
            ch.setLevel(logging.INFO)
        elif verbose_flag.lower() == 'warning':
            root.setLevel(logging.WARNING)
            ch.setLevel(logging.WARNING)
        elif verbose_flag.lower() == 'error':
            root.setLevel(logging.ERROR)
            ch.setLevel(logging.ERROR)
        elif verbose_flag.lower() == 'critical':
            root.setLevel(logging.CRITICAL)
            ch.setLevel(logging.CRITICAL)

    formatter = LevelFormatter(fmt="[%(asctime)s] %(levelname)s: %(message)s", level_fmts={logging.INFO: "%(message)s"})

    if filename != "":
        log_f.setFormatter(formatter)
    ch.setFormatter(formatter)

    if filename != "":
        root.addHandler(log_f)
    root.addHandler(ch)

    return root
