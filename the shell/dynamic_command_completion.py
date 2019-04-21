#!/usr/bin/env python3
import readline
import rlcompleter
# def tab_completion(command_line):
#     pass
#
#
def history(command):
    # readline.set_completer(show_prompt())
    # readline.set_completer_delims('intek-sh:$ ')
    readline.redisplay()
    a = readline.get_completer_delims()
    readline.parse_and_bind('tab: complete')
    # readline.insert_text(a)
    # readline.add_history(command)
    # print(readline.read_history_file(''))
    # a = readline.get_current_history_length()
    # print(a)
    # print(readline.get_history_item(a))
