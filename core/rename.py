import os, sys

from asgard_sdk.models.local import LocalPath

from dotenv import dotenv_values
from json import loads
from re import compile
from colorama import Fore, Style

RED=Fore.RED
GREEN=Fore.GREEN
BLUE=Fore.BLUE
NC=Style.RESET_ALL

def validate_path(path: str) -> None:
    if path.startswith("~"):
        path = path.replace("~", os.getenv("HOME"))
    
    if os.path.exists is False:
        print("[{R}error{NC}] Failed to find path: ".format(R=RED, NC=NC), path)
        sys.exit(1)

class Rename:
    def __init__(self, config_path: str):
        self.config_path = config_path
        self.config_map = None
        
        self.show_name = ""
        self.season_regex = []
        self.episode_regex = []
        self.dry_run = False
        self.no_seasons = False

        validate_path(self.config_path)
        self.parse_config()

    def parse_config(self):
        # self.config_map = dotenv_values(self.config_path)
        with open(self.config_path, 'r') as file:
            data = file.read()
            self.config_map = loads(data)

        episode_regex = self.config_map.get("episode_regex")
        if episode_regex is None and len(self.season_regex) == 0:
            print("[{R}error{NC}] Failed to find episode regular expressions".format(R=RED, NC=NC))
            sys.exit(1)
        
        self.episode_regex = episode_regex

        if self.no_seasons is False:
            season_regex = self.config_map.get("season_regex")
            if season_regex is None and len(self.season_regex) == 0:
                print("[{R}error{NC}] Failed to find season regular expressions".format(R=RED, NC=NC))
                sys.exit(1)

            self.season_regex = season_regex

    def compile_regex(self):
        ret = []
        for regex in self.episode_regex:
            # print("Compiling: ", regex)
            ret.append(compile(regex))

        self.episode_regex = ret
        print(self.episode_regex)
        
        ret = []
        for regex in self.season_regex:
            # print("Compiling: ", regex)
            ret.append(compile(regex))

        self.season_regex = ret

    def match_str(self, string: str, regex_list: list):
        ret = None

        for regex in regex_list:
            search = regex.search(string)
            if search:
                ret = search
                break

        return ret

    def info(self, path: str):
        validate_path(path)

    def fetch_seasons(self, path: str):
        ret = []
        
        for root, directories, files in os.walk(path):
            for name in directories:
                full_path = os.path.join(root, name)

                match = self.match_str(name, self.season_regex)
                if match is not None:
                    ret.append(full_path)

        return ret

    def rename_episodes(self, seasons: list):
        renamed = []
        
        for path in seasons:
            for root, directories, files in os.walk(path):
                for name in files:
                    full_path = os.path.join(root, name)

                    match = self.match_str(name, self.episode_regex)
                    if match is not None:
                        file_ext = name.split(".")[-1]
                        sn = match.group(1)
                        en = match.group(2)
                        new_file_name = root + "/" + "{n} - S{sn}E{en}".format(n=self.show_name, sn=sn, en=en) + ".{}".format(file_ext)
                        print(new_file_name)
                        if self.dry_run is False:
                            os.rename(full_path, new_file_name)

                        renamed.append(new_file_name)

        return renamed

    def walk(self, path: str):        
        seasons = self.fetch_seasons(path)
        renamed = self.rename_episodes(seasons)

        return seasons, renamed