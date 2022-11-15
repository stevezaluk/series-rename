import os
# S([0-9]\S)E\s\(([0-9]\S)\)
from core.rename import Rename
from argparse import ArgumentParser

def usage():
    print("series-rename - A bulk renaming tool for tv series")
    print("     -i [path] : Show info on a path or file")
    print("     -p [path] : Choose the path you would like to walk")
    print("     -c [config.env] : Choose a config file")
    print("     --no-seasons : Dont check for season folders")
    print("     --show-name 'NAME' : Choose a show name to embed in the file name")
    print("     --match-db [imdb|tvdb|plex] : Match episode titles and add them to the end of the file name.")
    print("     --episode-regex [regex] : Add an episode regex to the validation pool")
    print("     --season-regex [regex] : Add a regex to the validation pool")
    print("     --dry-run : Do everything except rename files")

parser = ArgumentParser()

parser.add_argument("-i", "--info", action="store")
parser.add_argument("-p", "--path", action="store")
parser.add_argument("-c", "--config", action="store")

parser.add_argument("--no-seasons", action="store_true")
parser.add_argument("--show-name", action="store")
parser.add_argument("--match-db", action="store")
parser.add_argument("--episode-regex", action="store")
parser.add_argument("--season-regex", action="store")
parser.add_argument("--dry-run", action="store_true")

if __name__ == "__main__":
    args = parser.parse_args()

    config_path = "config.json"
    if args.config:
        config_path = args.config
    
    rename = Rename(config_path)

    if args.show_name:
        rename.show_name = args.show_name

    if args.no_seasons:
        rename.no_seasons = True

    if args.episode_regex:
        pass

    if args.season_regex:
        pass

    if args.dry_run:
        rename.dry_run = True

    if args.info:
        rename.info(args.info)

    if args.path:
        print("[info] Compiling {l} regular expressions".format(l=len(rename.episode_regex) + len(rename.season_regex)))
        rename.compile_regex()
        print("[info] Walk: ", args.path)
        seasons, renamed = rename.walk(args.path)
        print("Renamed: {ec} episodes in {sc} seasons".format(sc=len(seasons), ec=len(renamed)))

