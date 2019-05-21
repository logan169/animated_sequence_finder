# -*- coding: utf-8 -*-


from functools import wraps
import os


def check_folder_path_exists(func):
    """
    Decorator that evaluate if the folder exist
    Raise an Exception otherwise
    """

    @wraps(func)
    def func_wrapper(*args, **kwargs):
        folder_path = args[0]
        if os.path.isdir(folder_path):
            return func(*args, **kwargs)
        raise Exception(
            "Error: folder {} doesn't exists".format(folder_path))

    return func_wrapper
