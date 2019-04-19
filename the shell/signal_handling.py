#!/usr/bin/env python3
import signal


def handling_signals():
    signal.signal(signal.SIGQUIT, signal.SIG_IGN )
    signal.signal(signal.SIGTERM, signal.SIG_IGN)
    return