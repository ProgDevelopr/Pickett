""" Utilities for Pickett """

from json import load, dump
from os.path import exists, getsize, expanduser, join

class TreeView:
    """ Organizes data in a tree-like structure. """
    def __init__(self, header):
        self.header = header
        self.branches = []

    def add_branches(self, branch_list: list):
        """
        Adds things to display.
        
        Args:
            branch_list (list): The branches to add.
        """
        for branch in branch_list:
            self.branches.append(branch)

    def view(self, listing=False):
        """ Prints the tree. """

        if not self.branches:
            print(f"* {self.header}: Empty key!\n")
        else:
            print(f"* {self.header}")
            for index, item in enumerate(self.branches):
                condition = len(item)>35 and listing
                sep = f'({index})' if listing else ''

                if index == len(self.branches)-1:
                    print(f"\'-{sep} {f'{item[0:35]}...' if condition else item}\n")
                else:
                    print(f"|-{sep} {f'{item[0:35]}...' if condition else item}")

VALUE_CAP = 3
PICKETT_VER = 2.7
CACHE_PATH = join(expanduser('~'), "cache.json")
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

def cache_size():
    """ Returns the size of the cache in Bytes/Kilobytes """
    if not exists(CACHE_PATH):
        return 0
    byte_size = getsize(CACHE_PATH)
    return f"{byte_size/1024:.3f} kilobytes" if byte_size > 1024 else f"{byte_size} bytes"

def all_keys_used(cache_obj: dict):
    """ 
    Returns the if all keys are used to the fullest. 
    
    Args:
        cache (dict): The cache itself.
    """
    return len(cache_obj.keys())*3 == sum(len(x) for x in cache_obj.values())

def value_warning(cache_obj: dict, tree: TreeView):
    """ 
    Gives a warning if all values are not used fully.
    
    Args:
        cache (dict): The cache itself.
    """
    if len(cache_obj.keys())*3 != sum(len(x) for x in cache_obj.values()):
        tree.add_branches(["Some values are unused!"])

def pickett_help(header: str):
    """ The help utility for pickett """
    tree_obj = TreeView(header)
    tree_obj.add_branches((
        "pickett add <KEY> <Optional: FILE>",
        "pickett kill <KEY>/all",
        "pickett list <Optional: KEY>",
        "pickett truncate <KEY>/all",
        "pickett clean <KEY>/all",
        "pickett ow <FILE> <KEY> <Optional: RELEASE_INDEX>",
        "pickett import <JSON>",
        "pickett export <Optional: NAME>",
        "pickett stats",
        "pickett where",
        "pickett version",
        "pickett help"
    ))
    tree_obj.view()
