""" Main Program - Pickett """

from sys import argv, exit as ext
from os.path import exists
from json import load, dump, JSONDecodeError
import utils

argv = argv[1:]
cache = utils.load_cache()
if len(argv)==0:
    utils.pickett_help(f"Pickett {utils.PICKETT_VER}")
    ext(0)

setting = argv[0]
try:
    match setting.strip().lower():
        case "add":
            key = argv[1]
            if len(argv)==2:
                cache[key]=[]
                print(f"Added new empty key: \"{key}\".")
            else:
                if key in cache:
                    if len(cache[key])<utils.VALUE_CAP:
                        cache[key].append(utils.read_f(argv[2]))
                        print(f"Added new release to \"{key}\".")
                    else:
                        print(f"Too many releases for key \"{key}\"!")
                        option = input("Would you like to remove the oldest release? (y/n): ")
                        if option.strip().lower()[0]=="y":
                            cache[key].remove(cache[key][0])
                            print("Deleting oldest release...")
                            cache[key].append(utils.read_f(argv[2]))
                            print("Added new release.")
                        else:
                            print("OK, but your release will not be saved!")
                else:
                    cache[key]=[utils.read_f(argv[2])]
                    print(f"New key was added: \"{key}\"")

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
                        print(f"Key \"{key}\" does not exist!")
            else:
                print("No keys found in cache!")

        case "ow":
            if cache:
                file = argv[1]
                key = argv[2]
                release = -1
                if len(argv) == 4: # Because argv includes setting
                    release = int(argv[3])

                if utils.VALUE_CAP > release > -2:
                    if not key in cache:
                        print(f"Key \"{key}\" does not exist!")
                        ext(1)
                    if not exists(file):
                        print(f"File \"{file}\" does not exist!")
                        ext(1)
                    utils.write_f(file, cache[key][release])
                    print(f"Overwrite to \"{file}\" was successful.")
                else:
                    print(f"Please enter values between 0-{utils.VALUE_CAP-1}. (self-included)")
            else:
                print("No keys found in cache!")

        case "list":
            if cache:
                if len(argv)==1:
                    for k,v in cache.items(): # k = keys, v = arrays
                        if v == []:
                            print(f"* {k}: Empty key\n")
                        else:
                            tree_obj = utils.TreeView(str(k))
                            tree_obj.add_branches([str(x).replace("\n","\\n") for x in v])
                            tree_obj.view(listing = True)
                else:
                    key = argv[1]
                    if not key in cache:
                        print(f"Key \"{key}\" does not exist!")
                        ext(1)
                    if cache[key] == []:
                        print(f"* {key}: Empty key\n")
                    else:
                        tree_obj = utils.TreeView(str(key))
                        tree_obj.add_branches([str(x).replace("\n","\\n") for x in cache[key]])
                        tree_obj.view(listing = True)
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
                        print(f"Key \"{key}\" does not exist!")
            else:
                print("No keys found in cache!")

        case "clean":
            if cache:
                key = argv[1]
                if argv[1]=="all":
                    for k,v in cache.items():
                        if len(v)>0:
                            cache[k]=[v[-1]]
                            continue
                    print("Cleaned all keys in cache.")
                else:
                    if argv[1] in cache:
                        cache[argv[1]]=[cache[argv[1]][-1]]
                        print(f"Cleaned key \"{argv[1]}\".")
                    else:
                        print(f"Key \"{argv[1]}\" does not exist!")
            else:
                print("No keys found in cache!")

        case "stats":
            tree_obj = utils.TreeView("config.json")
            tree_obj.add_branches([
                f"{utils.cache_size()}",
                f"{len(cache.keys())} keys",
                f"{sum(len(x) for x in cache.values())} values"
            ])
            utils.value_warning(cache, tree_obj)
            tree_obj.view()

        case "import":
            if len(argv)<2:
                print("Please enter file name.")
                ext(1)
            NEW_CACHE = argv[1] if argv[1].endswith(".json") else argv[1]+".json"
            if not exists(NEW_CACHE):
                print(f"{NEW_CACHE} does not exist.")
                ext(1)
            with open(NEW_CACHE, mode="r", encoding="utf-8") as f:
                try:
                    cache = dict(load(f))
                except JSONDecodeError:
                    print(f"\"{NEW_CACHE}\" is not a JSON file!")
                    ext(1)
            print(f"New cache imported from \"{NEW_CACHE}\".")

        case "export":
            EXPORT_NAME = "cache.json"
            if len(argv)>1:
                EXPORT_NAME = argv[1] if argv[1].endswith(".json") else argv[1]+".json"
            with open(EXPORT_NAME, mode="w", encoding="utf-8") as f:
                dump(cache, f)
            print(f"Exported cache.json as \"{EXPORT_NAME}\".")

        case "where":
            print(f"Cache path: {utils.CACHE_PATH}")

        case "version":
            print(f"Pickett {utils.PICKETT_VER}")

        case "help":
            utils.pickett_help("Commands: ")

        case _:
            utils.pickett_help("Please enter a proper setting: ")
    utils.apply_changes(cache)
except IndexError:
    print("An index error has occurred! Please make sure index exists in cache.")
    ext(1)
except ValueError:
    print("Please enter proper arguments.")
    ext(1)
except Exception as e:
    print(e)
    ext(1)
