""" Project settings environment module. """
import ast
import os
import random


def get_secret_key(base_dir):
    """ Read key from file or create a new one. """
    key_file = os.path.join(base_dir, 'var', 'secret_key')
    if os.path.isfile(key_file):
        with open(key_file) as key_fd:
            key = key_fd.read().strip()
    else:
        key = ''.join(random.choice(
            'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
        ) for _ in range(50))
        with open(key_file, 'w') as key_fd:
            key_fd.write(key)
    return key


def get_settings(base_dir, settings_file):
    """ Eval the settings file and return it. """
    path = os.path.join(base_dir, 'var', settings_file)
    with open(path) as settings_fd:
        return ast.literal_eval(settings_fd.read())
    return None
