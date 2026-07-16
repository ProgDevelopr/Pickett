""" Main Program - Pickett """

from sys import argv
from os.path import exists
import utils

argv = argv[1:]
setting = argv[0]
cache = utils.load_cache()

try:
    match setting.strip().lower():
        case "add":
            key = argv[1]
            if len(argv)==2:
                cache[key]=[]
                print(f"Added new empty key: \"{key}\".")
            else:
                if key in cache:
                    if len(cache[key])<3:
                        cache[key].append(utils.read_f(argv[2]))
                        print(f"Added new release to {key}.")
                    else:
                        print(f"Too many releases for key \"{key}\"!")
                        option = input("Would you like to remove the oldest release? (y/n): ")
                        if option.strip().lower()[0]=="y":
                            cache[key].remove(cache[key][0])
                            print("Deleted oldest release...")
                            cache[key].append(utils.read_f(argv[2]))
                            print("Added new release.")
                        else:
                            print("OK, but your release will not be saved!")
                else:
                    cache[key]=[utils.read_f(argv[2])]
                    print(f"New key was added: {key}")

        case "kill":
            if cache:
                key = argv[1]
                if key.lower().strip()=="all":
                    cache = {}
                    print("Deleted all keys in cache.")
                else:
                    if key in cache:
                        cache.pop(key)
                        print(f"Deleted key \"{key}\".")
                    else:
                        print(f"Key \"{key}\" does not exist.")
            else:
                print("No keys found in cache.")

        case "ow":
            if cache:
                try:
                    file = argv[1]
                    key = argv[2]
                    release = -1
                    if len(argv) == 4: # Because argv includes setting
                        release = int(argv[3])

                    if 3 > release > -2:
                        if not key in cache:
                            print(f"Key \"{key}\" does not exist.")
                        if not exists(file):
                            print(f"File \"{file}\" does not exist.")
                        if exists(file) and key in cache:
                            utils.write_f(file, cache[key][release])
                            print("Overwrite was successful.")
                    else:
                        print("Please enter values between 0-2. (self-included)")
                except IndexError:
                    print("An index error has occured, please check cache.json.")

        case "list":
            if cache:
                for k,v in cache.items(): # k = keys, v = arrays
                    if v == []:
                        print(f"* {k}: Empty key")
                    else:
                        print(f"* {k}:")
                        for i,j in enumerate(v): # i = indices, j = values in v
                            if i==len(v)-1:
                                if len(j)>20:
                                    print(f"'-({i}) {j[0:20]}...")
                                else:
                                    print(f"'-({i}) {j}")
                            else:
                                if len(j)>20:
                                    print(f"|-({i}) {j[0:20]}...")
                                else:
                                    print(f"|-({i}) {j}")
                    print()

            else:
                print("No keys found in cache.")

        case "truncate":
            if cache:
                key = argv[1]
                if key=="all":
                    for k,_ in cache.items():
                        cache[k]=[]
                    print("Truncated all keys in cache.")
                else:
                    if key in cache:
                        cache[key]=[]
                        print(f"Truncated key \"{key}\".")
                    else:
                        print(f"Key \"{key}\" does not exist.")
            else:
                print("No keys found in cache.")

        case "clean":
            if cache:
                key = argv[1]
                if argv[1]=="all":
                    for k,v in cache.items():
                        if len(v)>0:
                            cache[k]=[v[-1]]
                            continue
                    print("Cleaning done!")
                else:
                    if argv[1] in cache:
                        cache[argv[1]]=[cache[argv[1]][-1]]
                        print(f"Cleaned key \"{argv[1]}\"!")
                    else:
                        print(f"Key \"{argv[1]}\" does not exist.")
            else:
                print("No keys found in cache.")

        case "help":
            print("* Commands: ")
            utils.pickett_help()

        case _:
            print("* Please enter a proper setting: ")
            utils.pickett_help()
    utils.apply_changes(cache)
except IndexError:
    print("An index error has occurred. Please make sure index exists in cache.")
except ValueError:
    print("Please enter proper arguments.")
except Exception as e:
    print(e)
