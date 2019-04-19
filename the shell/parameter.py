def deal_parameter(value):
    while '$' in value:
        if '{' and '}' not in value:
            if value[1:] in environ:
                print(environ[value[1:]])
            elif value[1:] in local_variable
                print(local_variable[value])
        elif '{' in value and '}' in value:
            start_point = value.find('{') + 1
            end_point = value.find('}') - 1
            value = value[start_point:end_point]

