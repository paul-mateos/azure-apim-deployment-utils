import os

def byteify(input):
    if isinstance(input, dict):
        return {byteify(key): byteify(value)
                for key, value in input.iteritems()}
    elif isinstance(input, list):
        return [byteify(element) for element in input]
    elif isinstance(input, unicode):
        return input.encode('utf-8')
    else:
        return input
 
def replace_env(input):
    if isinstance(input, dict):
        return {replace_env(key): replace_env(value)
                for key, value in input.iteritems()}
    elif isinstance(input, list):
        return [replace_env(element) for element in input]
    elif isinstance(input, str):
        if input.startswith('$'):
            env_name = input[1:] # strip $
            return os.environ[env_name]
        return input
    else:
        return input
