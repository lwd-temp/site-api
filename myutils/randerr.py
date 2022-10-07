# randerr.py
# Raise Random Exceptions
import random


def randerr():
    # Get a list of all the exception types
    errlist = [BaseException, SystemExit, KeyboardInterrupt, GeneratorExit,
               Exception, StopIteration, ArithmeticError, FloatingPointError,
               OverflowError, ZeroDivisionError, AssertionError, AttributeError,
               BufferError, EOFError, ImportError, LookupError, IndexError,
               KeyError, MemoryError, NameError, UnboundLocalError, OSError,
               BlockingIOError, ChildProcessError, ConnectionError,
               BrokenPipeError, ConnectionAbortedError, ConnectionRefusedError,
               ConnectionResetError, FileExistsError, FileNotFoundError,
               InterruptedError, IsADirectoryError, NotADirectoryError,
               PermissionError, ProcessLookupError, TimeoutError, ReferenceError,
               RuntimeError, NotImplementedError, RecursionError, SyntaxError,
               IndentationError, TabError, SystemError, TypeError, ValueError,
               UnicodeError, UnicodeDecodeError, UnicodeEncodeError,
               UnicodeTranslateError, Warning, DeprecationWarning,
               PendingDeprecationWarning, RuntimeWarning, SyntaxWarning,
               UserWarning, FutureWarning, ImportWarning, UnicodeWarning,
               BytesWarning, ResourceWarning]
    # Get a random exception type
    err = random.choice(errlist)
    # Raise the exception
    raise err
