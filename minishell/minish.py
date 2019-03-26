#!/usr/bin/env python3
from os import path, environ, chdir, getcwd, listdir


def show_prompt():
    print('intek-sh$ ', end='')
    command = input()
    return command


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


def do_other_commands(action, variable):
    for dir_path in environ['PATH'].split(':'):
        a = path.listdir(dir_path)
        print(a)
        # if command[0] in dir:
        #     run_file = dir + '/' + command[0]
        #     import run_file
    return


def main():
    while True:
        command_list = ['cd', 'pwd', 'printenv', 'export', 'unset', 'exit']
        command = show_prompt()
        atom = command.split()
        print(atom)
        action = atom[0]
        variable = atom[1]
        if action == 'cd':
            get_dir(command.split())
        elif action == 'cwd':
            print(take_cwd())
        elif action not in command_list:
            do_other_commands(command)
        elif action == 'exit':
            break



if __name__ == '__main__':
    main()
