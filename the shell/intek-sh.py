#!/usr/bin/env python3
from os import path, environ, chdir, getcwd, listdir, walk, getpid
import subprocess as s
from path_expansion import *
# from dynamic_command_completion import *
from threading import Thread
from signal_handling import *
from dynamic_command_completion import *


def show_prompt():
    """
    show the prompt and basically cope with user's input.
    """
    print('intek-sh$ ', end='')
    command = input()
    history(command)

    return command.split()


def get_dir(command, current_path):
    """
    change the working shell directory to another one.
    Args:
        command (string): A list contains action and the expected directory
        path which is wanted to move on.
    Raises:
        Exception: raises some errors in case of the expected directory is
        not existing, it is a file or some Permission problems.
    """
    # get the current working directory path.
    dir_path = current_path
    try:
        home_path = environ['HOME']
        # in case of user only input "cd", the shell back to user path.
        if len(command) == 1:
            chdir(home_path)
        # in case of user input a particular path of directory
        elif len(command) > 1:
            if home_path not in command[1]:
                access_dir = dir_path + '/' + command[1]
            else:
                access_dir = command[1]
            if path.isdir(access_dir):
                try:
                    chdir(access_dir)
                except PermissionError:
                    print('intek-sh: cd: ' + command[1] +
                          ':      denied')
            elif path.isfile(access_dir):
                print('intek-sh: cd: '+command[1]+': Not a directory')
            else:
                print('intek-sh: cd: '+command[1] +
                      ': No such file or directory')
    # in case of environ(PATH) is unseted, return error.
    except KeyError:
        print('intek-sh: cd: HOME not set')


def print_environment(command):
    """
    Show detail of one, several of all of the environment.
    Args:
        command (list): a list contains the particular key of environment
        dictionary or nothing
    Raises:
        KeyError: if the key is not apprearan, ignore it and dont do anything
    """
    try:
        # if len of command >=1 , it contains several key of environment
        # dictionary, just print the value of it
        if len(command) >= 1:
            for item in command:
                print(environ[item])
        # if len of the command list is 0, it contains nothing and we just
        if len(command) == 0:
            for value in environ:
                print(value + '=' + environ[value])
    except KeyError:
        pass


def deal_export(command):
    """
    add Key and Value in environment dictionary.
    Args:
        command (list): a list of environment variables
    Raises:
        Exception: if not have in a part of list, show error
    """

    for item in command:
        if '=' in item:
            environ_variable, variable_context = item.split('=')
            environ[environ_variable] = variable_context
        else:
            environ[item] = ''
            print('ValueError: not enough values to unpack')


def delete_environment_variable(command):
    """
    delete one or some environment variable if it is exist.

    Args:
        command (list): list of expected variables

    Raises:
        KeyError: if the variables is not exists previously, dont delete it.

    """
    for item in command:
        try:
            del environ[item]
        except KeyError:
            pass


def run_other_commands(action, command):
    """
    try to run a command.
    Args:
        action (string): the path of command
        command(list): a list contains action and options
    Returns:
        an integer
    Raises:
        Exception: if the file's permissions are limited, raise error.
    """
    try:
        s.run(command)
    except PermissionError:
        print('intek-sh: '+action+': Permission denied')
    except TypeError:
        pass
    return 1


def do_other_commands(command):
    '''
    Run command in executable directory of PATH environmentself.

    Input:
        @command: name of excutable file

    Ouput:
        Return result when run command
    '''
    #  run command if it exists in current directory and excutable directory
    action = command[0]
    count = 0
    # run command if it exists in current directory
    if path.isdir(action):
        print('Intek-sh: ' + command + ': Is a directory')
    else:
        if './' in action:
            if path.exists(action[2:]):
                count = run_other_commands(action, command)
            else:
                print('intek-sh: '+action+': No such file or directory')
        # run command if it exists in excutable directories
        elif 'PATH' in environ:
            for dir_path in environ['PATH'].split(':'):
                command[0] = dir_path + '/' + action
                if path.exists(command[0]):
                    count = run_other_commands(command[0], command)
                    return
            if count == 0:
                print('intek-sh: '+action+': command not found')
        # if the command is not in both current directory and it is not a
        # file in excutable directories then print error.
        else:
            print('intek-sh: '+action+': command not found')


def exit(command):
    """
    exit the program.
    Args:
        command (list): a list contains the exit command and exit code.
    Raises:
        Exception: if not exit code, exit in different form.
    """
    try:
        if len(command) == 1 or int(command[1]):
            print('exit')
    except ValueError:
        print('exit')
        print('intek-sh: exit: '+command[1])


def main():
    global previous_path
    while True:
        previous_path, current_path = get_cwd()
        try:
            handling_signals()
            previous_command = show_prompt()
            command = deal_path_expansion(previous_command, previous_path,
                                          current_path)
            command_list = ['cd', 'printenv', 'export', 'unset', 'exit']
            if command:
                # run change directory command
                if command[0] == 'cd':
                    get_dir(command, current_path)
                # run others commands
                elif command[0] not in command_list:
                    do_other_commands(command)
                # print the environment detail
                elif command[0] == 'printenv':
                    print_environment(command[1:])
                # add others environment variables
                elif command[0] == 'export':
                    deal_export(command[1:])
                # delete somes environment variables
                elif command[0] == 'unset':
                    delete_environment_variable(command[1:])
                    unseted_variable(command[1:])
                # exit the program
                elif command[0] == 'exit':
                    exit(command)
                    break
        except EOFError:
            break
        except KeyboardInterrupt:
            print(" ")


if __name__ == '__main__':
    previous_path = []
    main()
