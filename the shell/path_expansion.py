from os import environ, getcwd
from re import sub
from pwd import getpwnam


previous_path = None
list_of_path = []
local_variable = {}
unseted_list = []


def cope_with_tilde(command_list, previous_path, current_path):
    """
    cope single and multiple tidle.
    Args:
        command_list (list): list contains command
        previous_path(string): path of previous working directory
        current_path(string): path of current working directory
    Returns:
        list: modified list
    """
    # if the first part of the firt partition of list is ~ then considering
    # it as a sigle tidle and call relevant function.
    if command_list[0][0] is '~' and len(command_list) == 1:
        command_list = cope_single_tidle(command_list, previous_path,
                                         current_path)
        return command_list
    # if len of the command_list is more than 1 and the firt character of then
    # first partition is not ~ then considering it as a multiple tidle and
    # call the relevant function.
    elif len(command_list) > 1 and '~' not in command_list[0]:
        command_list = cope_with_multiple_tidle(command_list, previous_path,
                                                current_path)
        return command_list


def get_cwd():
    """
    This function find the path of previous working directory
    as well and current working directory
    Returns:
        string: a path of previous working directory
        list: a list of working paths
    """
    global previous_path, list_of_path
    # add path of current working directory to a list
    list_of_path.append(getcwd())
    if len(list_of_path) >= 2:
        if list_of_path[-1] != list_of_path[-2]:
            previous_path = list_of_path[-2]
    return previous_path, list_of_path[-1]


def cope_single_tidle(command_list, previous_path, current_path):
    """
    deal with tidle when it in the first char of the first partition of simple
    list
    Args:
        command_list (list): list contains command
        previous_path(string): path of previous working directory
        current_path(string): path of current working directory
    Returns:
        string: modified command or None
    Raises:
        KeyError
    """

    try:
        # if only ~ in the command_list
        if len(command_list[0]) == 1:
            return '/home/' + environ['USER']
        # if only ~GROUP_USER_NAME in the command
        if command_list[0] == ('~' + getpwnam(command_list[0][1:]).pw_name):
            return '/home/' + getpwnam(command_list[0][1:]).pw_name
        if command_list[0] == '~/':
            return '/home/' + environ['USER'] + '/'
        if command_list[0] == '~+':
            return current_path
        if command_list[0] == '~-':
            if previous_path is None:
                print('~-: command not found')
                return
            return previous_path
    except KeyError:
        pass


def cope_with_multiple_tidle(command_list, previous_path, current_path):
    """
    cope with tidle expansion if it is multiple type
    Args:
        command_list (list): list contains command
        previous_path(string): path of previous working directory
        current_path(string): path of current working directory
    Returns:
        string: modified command or None
    Raises:
        KeyError
    """
    # handle each value in the command list and modify them
    for index, value in enumerate(command_list):
        # if the value start with ~/
        if '~/' in value[0:2]:
            command_list[index] = '/home/' + environ['USER'] + value[1:]
        # if the value start with ~-
        elif '~-' in value[0:2]:
            command_list[index] = previous_path
        # if the value start with ~+
        elif '~+' in value[0:2]:
            command_list[index] = current_path
        # if the value start with ~
        elif '~' in value[0]:
            try:
                if len(value) == 1:
                    command_list[index] = '/home/' + environ['USER']
                else:
                    if value[1:] == getpwnam(value[1:]).pw_name:
                        command_list[index] = '/home/' + \
                                              getpwnam(value[1:]).pw_name
            except KeyError:
                pass
        # if the value start with ~+/
        elif '~+/' in value[0:3]:
            command_list[index] = current_path + value[2:]
        # if the value start with ~+
        elif '~-/' in value[0:3]:
            command_list[index] = previous_path + value[2:]
    return command_list


def variable(command_list, previous_path, current_path):
    """
    Put the variable into the dictionary containing local variables.
    Args:
        command_list (list): list contains command
        previous_path(string): path of previous working directory
        current_path(string): path of current working directory
    Returns:
        dictionary: contains the label of local variable and its value
    """

    global local_variable
    for value in command_list:
        if '=' in value and '+' not in value:
            vari = value.split('=')
            local_variable[vari[0]] = deal_path_expansion(vari[1],
                                                          previous_path,
                                                          current_path)
        elif '+=' in value:
            vari = value.split('+=')
            local_variable[vari[0]] += str(vari[1])
    return local_variable


def has_bad_substitution(value):
    """
    check the command wheather it has bad substitution or not.
    Args:
        value (string): command line
    Returns:
        boolean: True if has bad subprocess and vice versa
    Raises:
        Exception: description
    """

    # if bracket has irregular character inside then True
    try:
        item = ['.', '#', '!', '%', '*', '@', '&', '(', ')', '{', '//', "//",
                '[', ']', '^']
        if any(x in value for x in item):
            return True
        # if bracket is empty then True
        elif value == len(value)*' ':
            return True
        else:
            return False
    except Exception:
        return False


def deal_multiple_parameter(value):
    """
    handle some multiple parameters in command line.

    Args:
        value (string): command line

    Returns:
        string: modified value

    Raises:
        TypeError

    """

    start_point = value.find('{')
    end_point = value.find('}')
    try:
        # consider the case of parameter and call suitable function.
        if value[start_point - 1] == '$':
            # check substitution right here!!
            if has_bad_substitution(value[start_point + 1: end_point]):
                print('intek-sh: ' + value + ': bad substitution')
                return
            partition = deal_parameter('$' + value[start_point + 1:end_point])
            value = value[:start_point - 1] + partition + value[end_point + 1:]
        elif value[start_point - 1] != '$':
            value = value[start_point:]
        # recursive to deal with multiple parameter expansions
        if '$' in value:
            value = deal_parameter(value)
    except TypeError:
        pass
    return value


def find_special_character(value):
    """
    return the index of special character in a command line.
    Args:
        value (string): a command line
    Returns:
        int: the index of the first special char in the value or a len of value
    """
    item = '.#!%*@&(){/\\[]^'
    for index in range(len(value)):
        if value[index] in item:
            return index
    return(len(value))


def deal_single_parameter(value):
    """
    cope with sigle parameter which does not contain the {} bracket.
    Args:
        value (string): command line

    Returns:
        string: modified value

    Raises:
        TypeError
    """
    global local_vaiable
    start_point = value.find('$') + 1
    end_point = start_point + find_special_character(value[start_point:])
    # if it starts with $, find the result in environ and  local variables
    # and return None if nothing found
    if value.startswith('$'):
        if value[start_point:end_point] in environ:
            return environ[value[start_point:end_point]] + value[end_point:]
        elif value[start_point:end_point] in local_variable:
            return local_variable[value[start_point:end_point]] + \
                    value[end_point:]
        else:
            return ''
    # elif $ live in the middle of the command line, using this chains to deal
    else:
        if value[start_point:end_point] in environ:
            return value[:start_point - 1] + \
                   environ[value[start_point:end_point]] + \
                   value[end_point:]
        elif value[start_point:end_point] in local_variable:
            return value[:start_point - 1] + \
                   local_variable[value[start_point:end_point]] + \
                   value[end_point:]
        else:
            return value[:start_point - 1] + value[end_point:]


def deal_parameter(value):
    """
    taking into account wheather it is multiple or simple genre.
    Args:
        value (string): a command line

    Returns:
        function: return relevant function to deal with this particular isusse
    """

    global local_vaiable
    if '{' and '}' not in value:
        return deal_single_parameter(value)
    if '{' in value or '}' in value:
        return deal_multiple_parameter(value)
    return ''


def deal_path_expansion(command_list, previous_path, current_path):
    """
    checking if the list of command contain path expansion.
    Args:
        command_list (list): list contains command
        previous_path(string): path of previous working directory
        current_path(string): path of current working directory
    Returns:
        string: modified command or default command
    """

    for index, value in enumerate(command_list):
        if '=' in value and '=' in command_list[0]:
            variable(command_list, previous_path, current_path)
            return
        elif '~' in value:
            command_list = cope_with_tilde(command_list, previous_path,
                                           current_path)
            return command_list
        elif '$' in value:
            command_list[index] = deal_parameter(value)
    return command_list


def is_in_environent(value):
    global local_variable
    if value in environ:
        return True
    elif value in local_variable:
        return True
    return False


def expanded_features(value, previous_path, current_path):
    global local_variable, unseted_list
    if ':-' in value:
        result = value.split(':-')
        if not is_in_environent(result[0]):
            return result[1]
        elif is_in_environent(result[0]):
            if local_variable[result[0]] is None or environ[result[0]] is None:
                return result[1]
            return local_variable[result[0]]
    elif '-' in value:
        result = value.split('-')
        if not is_in_environent(result[0]):
            if result[0] in unseted_list:
                return result[1]
    elif ':?' in value:
        if not is_in_environent(value.split(':?')[0]):
            result = sub(':?', '=', value)
            variable(result, previous_path, current_path)
    elif '=' in value:
        result = value.split('=')
        if not is_in_environent(result[0]):
            if result[0] in unseted_list:
                pass


def unseted_variable(command):
    global local_variable, unseted_list
    for value in command:
        if value in local_variable:
            del local_variable[value]
            unseted_list.append(value)
