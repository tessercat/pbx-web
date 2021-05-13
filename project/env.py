""" Project settings environment module. """
import ast
import logging
import os
import random


def get_settings(base_dir):
    """ Read settings and return it. """
    settings_file = os.path.join(base_dir, 'var', 'settings.py')
    with open(settings_file) as settings_fd:
        return ast.literal_eval(settings_fd.read())
    return {}


def get_secret_key(base_dir):
    """ Read the secret key from file or create a new one. """
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
