import utils
from sys import argv
from os.path import exists

argv = argv[1:]
setting = argv[0]
config = utils.load_config()

try:
    match setting.strip().lower():
        case "add":
            if argv[1] in config:
                if len(config[argv[1]])<3:
                    config[argv[1]].append(utils.read_f(argv[2]))
                    print(f"{argv[1]} already exists, added new release in it.")
                else:
                    print(f"Too many releases for key \"{argv[1]}\"!")
                    option = input("Would you like to remove the oldest release for space? (y/n): ").strip().lower()[0]
                    if option=="y":
                        config[argv[1]].remove(config[argv[1]][0])
                        print("Deleted oldest release...")
                        config[argv[1]].append(utils.read_f(argv[2]))
                        print("Added new release.")
                    else:
                        print("OK, but your release will not be saved!")
            else:
                config[argv[1]]=[utils.read_f(argv[2])]
                print(f"New key was added: {argv[1]}")

        case "kill":
            if argv[1].lower().strip()=="all":
                config = {}
                print("Deleted all keys in cache.")
            else:
                if argv[1] in config:
                    config.pop(argv[1])
                    print(f"Deleted key \"{argv[1]}\".")
                else:
                    print(f"Key \"{argv[1]}\" does not exist.")

        case "ow":
            try:
                key = argv[2]
                file = argv[1]
                release = -1 if len(argv[1:]) != 3 else int(argv[3])-1
                if release==-1 or 2 > release or release > 0:
                    if key in config and exists(file):
                        utils.write_f(file, config[key][release])
                        print("Overwrite was successful.")
                    else:
                        print("An error has occured, please check if file exists or if key is in cache.")
                else: 
                    print("Please enter values between 1-3.")
            except IndexError:
                print("An index error has occured, please check cache.json.")

        case "list":
            if config:
                for k,v in config.items():
                    print(f"{k}:")
                    for j in v:
                        if len(j)>20:
                            print(f"- {j[0:20]}...")
                        else:
                            print(f"- {j}")
            else:
                print("No keys in cache.")

        case "truncate":
            key = argv[1]
            if key=="all":
                for k,_ in config.items():
                    config[k]=[]
                print("Truncated all keys in cache.")
            else:
                if key in config:
                    config[key]=[]
                    print(f"Truncaated key \"{key}\".")
                else:
                    print(f"Key \"{key}\" does not exist.")

        case "clean":
            if config:
                if argv[1]=="all":
                    for k,v in config.items():
                        if len(v)>0:
                            config[k]=[v[-1]]
                            continue
                    print("Cleaning done!")
                else:
                    if argv[1] in config:
                        config[argv[1]]=[config[argv[1]][-1]]
                        print(f"Cleaned key \"{argv[1]}\"!")
                    else:
                        print(f"Key \"{argv[1]}\" does not exist.")
            else:
                print("No keys in cache.")

        case "help":
            print("Commands: ")
            utils.help()

        case _:
            print("Please enter a proper setting: ")
            utils.help()
except IndexError:
    print("An index error has occured. Please make sure to enter arguments correctly.")
utils.change_config(config)