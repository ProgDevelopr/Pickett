""" Utilities for Pickett """

from json import load, dump
from os.path import exists

CACHE_PATH = ".\\cache.json"
def load_cache():
    """
    Loads the cache file, creates one if it doesn't exist.
    """
    if not exists(CACHE_PATH):
        with open(CACHE_PATH, "w", encoding="utf-8") as f:
            f.write("{}")
    with open(CACHE_PATH, "r", encoding="utf-8") as f:
        return dict(load(f))

def apply_changes(dict_obj):
    """
    Applies changes to cache.
    
    Args:
        dict_obj (dict): The dict object that represents the cache.
    """
    with open(CACHE_PATH, "w", encoding="utf-8") as f:
        dump(dict_obj, f)

def read_f(file):
    """
    Reads a file.
    
    Args:
        file (str): file name
    """
    with open(file, "r", encoding="utf-8") as f:
        return f.read()

def write_f(file, content):
    """
    Writes to a file.
    
    Args:
        file (str): file name
    """
    with open(file, "w", encoding="utf-8") as f:
        f.write(content)

def pickett_help():
    """ The help utility for pickett """
    print("|- pickett add <KEY> <FILE>\n|- pickett kill <KEY>/all")
    print("|- pickett truncate <KEY>/all\n|- pickett clean <KEY>/all")
    print("|- pickett ow <FILE> <KEY> <Optional: RELEASE>\n|- pickett list\n'- pickett help")
