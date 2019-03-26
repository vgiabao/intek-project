#!/usr/bin/env python3
from os import path, environ, chdir, getcwd, listdir, walk
import subprocess as s


def show_prompt():
    print('intek-sh$ ', end='')
    command = input()
    return command.split()


def take_cwd():
    current_working_dir = getcwd()
    return current_working_dir


def get_dir(command):
    dir_path = take_cwd()
    home_path = '/' + dir_path.split('/')[1] + '/' + dir_path.split('/')[2]
    if len(command) == 1:
        chdir(home_path)
    elif len(command) > 1:
        access_dir = dir_path + '/' + command[1]
        if path.isdir(access_dir):
            try:
                chdir(access_dir)
            except PermissionError:
                print('bash: cd: ' + command[1] + ': Permission denied')
        elif path.isfile(access_dir):
            print('bash: cd: '+command[1]+': Not a directory')
        else:
            print('bash: cd: '+command[1]+': No such file or directory')


def do_other_commands(command):
    '''
    Run command in executable directory of PATH environmentself.

    Input:
        @command: name of excutable file

    Ouput:
        Return result when run command
    '''
    # get executable directory list and run command if it eixst in executable
    #   _directory
    action = command[0]
    count = 0
    for dir_path in environ['PATH'].split(':'):
        command[0] = dir_path + '/' + action
        if path.exists(command[0]):
            p = s.Popen(command)
            p.wait()
            count += 1
            return
    if count == 0:
        print(action+': command not found')
    return


def cope_environment(command):
    try:
        if len(command) >= 1:
            for item in command:
                print(environ[item])
        if len(command) == 0:
            print(environ)
    except KeyError:
        pass


def deal_export(command):
    for item in command:
        environ_variable, variable_context = item.split('=')
        environ[environ_variable] = variable_context


def delete_environment_variable(command):
    for item in command:
        del environ[item]


def main():
    while True:
        command = show_prompt()
        if command:
            command_list = ['cd', 'printenv', 'export', 'unset', 'exit']
            #
            if command[0] == 'cd':
                get_dir(command)
            #
            elif command[0] not in command_list:
                do_other_commands(command)
            #
            elif command[0] == 'printenv':
                cope_environment(command[1:])
            elif command[0] == 'export':
                deal_export(command[1:])
            elif command[0] == 'unset':
                delete_environment_variable(command[1:])
            elif command[0] == 'exit':
                if len(command) >= 1:
                    print('exit')
                    break
        else:
            pass


if __name__ == '__main__':
    main()
