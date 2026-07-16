from json import load, dump
from os import getlogin
from os.path import exists

CONFIG = f".\\cache.json"
def load_config():
    if not exists(CONFIG):
        with open(CONFIG, "w") as f:
            f.write("{}")
    with open(CONFIG,"r") as f:
        return dict(load(f))

def change_config(conf_obj):
    with open(CONFIG,"w") as f:
        dump(conf_obj, f)

def read_f(file):
    with open(file, "r") as f:
        return f.read()

def write_f(file, content):
    with open(file, "w") as f:
        f.write(content)

def help():
    print("pickett add <KEY> <FILE>\npickett kill <KEY>/all")
    print("pickett truncate <KEY>/all\npickett clean <KEY>/all")
    print("pickett ow <FILE> <KEY> <Optional: RELEASE>\npickett list\npickett help")