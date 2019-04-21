#!/usr/bin/env python3
from readline import get_current_history_length, get_history_item, insert_text\
    , parse_and_bind, set_pre_input_hook, get_line_buffer
import os
import rlcompleter
# def tab_completion(command_line):
#     pass
#
def checking_environ():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    return dir_path



def history(command):
    # set_pre_input_hook(checking_environ())
    # readline.insert_text('intek-sh: ')
    # readline.get_completer_delims()
    a = get_line_buffer()
    # readline.add_history(command)
    # print(readline.read_history_file(''))

