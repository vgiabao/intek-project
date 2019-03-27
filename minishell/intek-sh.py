#!/usr/bin/env python3
from os import path, environ, chdir, getcwd, listdir, walk
import subprocess as s


def show_prompt():
    """show the prompt to read input from users.

    Returns: list of commands and options
    """
    print('intek-sh$ ', end='')
    command = input()
    return command.split()


def take_cwd():
    """
    Get the path of current working directory.

    Returns:
    the exactly path of current working directory
    """
    current_working_dir = getcwd()
    return current_working_dir


def change_dir(command):
    """
    change current working directory.

    Inputs:
        @command : the name of excutable file

    """
    dir_path = take_cwd()
    try:
        home_path = '/' + environ['HOME']
        if len(command) == 1:
            chdir(home_path)
        elif len(command) > 1:
            access_dir = dir_path + '/' + command[1]
            if path.isdir(access_dir):
                try:
                    chdir(access_dir)
                except PermissionError:
                    print('intek-sh: cd: ' + command[1] + ': Permission denied')
            elif path.isfile(access_dir):
                print('intek-sh: cd: '+command[1]+': Not a directory')
            else:
                print('intek-sh: cd: '+command[1]+': No such file or directory')
    except KeyError:
        print('intek-sh: cd: HOME not set')


def do_other_commands(command):
    '''
    Run command in executable directory of PATH environmentself.

    Input:
        @command: name of excutable file

    Ouput:
        Return result when run command
    '''
    action = command[0]
    count = 0
    # get executable directory list and run command if it eixst in executable
    #   _directory
    if './' in action:
        if path.exists(action[2:]):
            try:
                p = s.Popen(command)
                p.wait()
                count += 1
            except PermissionError:
                print('intek-sh: '+action+': Permission denied')
        else:
            print('bash: '+action+': No such file or directory')
    elif 'PATH' in environ:
        for dir_path in environ['PATH'].split(':'):
            command[0] = dir_path + '/' + action
            if path.exists(command[0]):
                try:
                    p = s.Popen(command)
                    p.wait()
                    count += 1
                    return
                except PermissionError:
                    print(command[0]+': Permission denied')
        if count == 0:
            print('intek-sh: '+action+': command not found')
    else:
        print('intek-sh: '+action+': command not found')


def print_environment(command):
    try:
        if len(command) >= 1:
            for item in command:
                print(environ[item])
        if len(command) == 0:
            for value in environ:
                print(value + '=' + environ[value])
    except KeyError:
        pass


def deal_export(command):
    for item in command:
        if '=' in item:
            environ_variable, variable_context = item.split('=')
            environ[environ_variable] = variable_context
        else:
            environ[item] = ''
            print('ValueError: not enough values to unpack')


def delete_environment_variable(command):
    for item in command:
        try:
            del environ[item]
        except KeyError:
            pass


def main():
    while True:
        try:
            command = show_prompt()
            if command:
                command_list = ['cd', 'printenv', 'export', 'unset', 'exit']
                #
                if command[0] == 'cd':
                    change_dir(command)
                #
                elif command[0] not in command_list:
                    do_other_commands(command)
                #
                elif command[0] == 'printenv':
                    print_environment(command[1:])
                elif command[0] == 'export':
                    deal_export(command[1:])
                elif command[0] == 'unset':
                    delete_environment_variable(command[1:])
                elif command[0] == 'exit':
                    try:
                        if len(command) == 1 or int(command[1]):
                            print('exit')
                    except ValueError:
                        print('exit')
                        print('intek-sh: exit: '+command[1])
                    break
        except EOFError:
            break


if __name__ == '__main__':
    main()
