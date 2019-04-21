#!/usr/bin/env python3
import signal


def handling_signals():
    """
    handle some effects causing interrupt program.
    Raises:
        KeyboardInterrupt: raises some errors in case of the expected directory is
        not existing, it is a file or some Permission problems.
    """
    # handling ctrl + C
    signal.signal(signal.SIGINT, call_sigint)
    # ignore ctrl + Q
    signal.signal(signal.SIGQUIT, signal.SIG_IGN)
    # ignore ctrl + \
    signal.signal(signal.SIGTERM, signal.SIG_IGN)
    # ignore Ctrl + Z
    signal.signal(signal.SIGTSTP, signal.SIG_IGN)


def call_sigint(signal, frame):
    raise KeyboardInterrupt


