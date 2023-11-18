import sys
import functools
import inspect

from loguru import logger

LOG_LEVEL = "INFO"
FILE_LEVEL = "DEBUG"


__doc__ = """
Provides logging ease of use for debugging. By default outputs to
- stderr at level INFO
- log.log at level DEBUG

## import with full
from libs.log import *

## outputs 'message', along with log level, time, origin, and line number
trace("message")
debug("message")
info("message")
success("message")
warning("message")
error("message")
critical("message")

## adds function entry and exit points, with arguments and result
@track
sum(a, b):
    return a + b

## by default track outputs at DEBUG, and errors to ERROR
@track(level=info, failure=warning)
prod(a, b):
    return a * b
"""

# Removes default logging handler and adds ones with custom formatting for the
# command line and the log.log file
logger.remove()
logger.add("log.log", format="{elapsed} | {level:<8} | {module:>16}:{function:<16} ({line:>4}) - {message}", level=FILE_LEVEL, backtrace=False)
logger.success("")
logger.success("=== NEW RUN ===")
logger.add(sys.stderr, colorize=True, format="<green>{elapsed}</green> | <level>{level:<8}</level> | {module:>16}:{function:<16} ({line:>4}) - <level>{message}</level>", level=LOG_LEVEL, backtrace=False)


# allows calling the logger's functions directly if imported
trace = logger.trace
debug = logger.debug
info = logger.info
success = logger.success
warning = logger.warning
error = logger.error
critical = logger.critical


def _annotate(v):
    if isinstance(v, str):
        v = '"' + v + '"'
    return f"{v}<{str(type(v))[8:-2]}>"


def track(_func=None, *, level=debug, failure=error):
    """Logs function calls with arguments and returns.

    @track
    sum(a, b):
        return a + b
    sum(2, b=3)
        
    -> (to log output/file) sum(2, b=3) -> 5
    """

    if not callable(level):
        raise TypeError("level must be a function")
    if not callable(failure):
        raise TypeError("failure must be a function")

    ## please do not copy any of this. This is horrific... but it works?
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):

            ## format the function's arguments for printing
            sargs = ", ".join(f"{_annotate(a)}" for a in args)
            skwargs = ", ".join(f"{k}={_annotate(v)}" for k,v in kwargs.items())
            fullargs = sargs + skwargs if skwargs else sargs

            # ## find the variable list and defaults
            # vars, _, _, default = inspect.getargspec(func)
            # if default is not None:
            #     d = dict(zip(vars[-len(default):], default))
            # else:
            #     d = {}
            # # d.update(dict(zip(vars, args)))
            # defaults = ", ".join(f"{k}{'=' + _annotate(d[k]) if k in d else ''}" for k in vars)

            try:
                ## run the function, then print
                # level(f"""{func.__name__}({defaults})""")
                level(f"""{func.__name__}({fullargs}) -> (running...)""")
                r = func(*args, **kwargs)
                # level(f"""{func.__name__}({defaults})""")
                level(f"""{func.__name__}({fullargs}) -> {_annotate(r)}""")
                return r
            
            except Exception as e:
                ## print the function arguments on failure
                # failure(f"""{func.__name__}({defaults})""")
                failure(f"""{func.__name__}({fullargs}) -> EXCEPTION""")
                logger.exception(e)
                raise

        return wrapper
    
    if _func is None:
        return decorator
    return decorator(_func)
