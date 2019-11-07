import sys


LOG_DEBUG = 0
LOG_INFO = 1
LOG_WARNING = 2
LOG_ERROR = 3

LOG_PREFIX = {
    LOG_DEBUG: "\x1B[0m[D]\x1B[0m",
    LOG_INFO: "\x1B[36m[I]\x1B[0m",
    LOG_WARNING: "\x1B[33m[W]\x1B[0m",
    LOG_ERROR: "\x1B[31m[E]\x1B[0m",
}
LOG_STR_MAPPING = {
    'debug': LOG_DEBUG,
    'info': LOG_INFO,
    'warn': LOG_WARNING,
    'warning': LOG_WARNING,
    'error': LOG_ERROR,
    'critical': LOG_ERROR,
}


log_level = LOG_WARNING


def validate_log_level(level):
    try:
        level = int(level)
        if 0 <= level <= LOG_ERROR:
            return level
    except Exception:
        pass

    if isinstance(level, str):
        try:
            return LOG_STR_MAPPING[level.lower()]
        except KeyError:
            raise ValueError(f"Invalid log level {level!r}") from None


def set_log_level(level):
    global log_level
    log_level = validate_log_level(level)


def log(level, *args):
    if not isinstance(level, int):
        try:
            level = LOG_STR_MAPPING[level.lower()]
        except KeyError:
            raise ValueError(f"Unexpected logging level {level!r}") from None
    if level < log_level:
        return  # Discard unwanted logs
    s = "{} {}".format(LOG_PREFIX[level], " ".join(map(str, args)))
    print(s, file=sys.stderr)
