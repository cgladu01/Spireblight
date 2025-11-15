from aiohttp import ClientSession, ClientError, ServerDisconnectedError

import traceback
import platform
import asyncio
import pickle
import time
import yaml
import os
from src.util.config import config
import shutil

'''
This file serves to fetch save file from local machine for server to use.
This file should not be called if local is set in local config
'''

class Extract:
    
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
            
    
    def fetch_save(self):
        content = ""

        for file in os.listdir(os.path.join(os.sep, config.local_source.location + os.sep, "saves")):
            try:
                if file.endswith(".autosave"):
                    if self.save_file is None:
                        self.save_file = file
                    else:
                        print("Error: Multiple savefiles detected.")
                        self.save_file = None
                        raise ValueError("Multiple savefiles detected")
            except:
                print("Cannot find save file")
                return None

        try:
            with open(os.path.join(config.local_source.location, "saves", self.save_file)) as f:
                content = f.read()
        except OSError:
            self.save_file = None
            return None
        content = content
        char = self.save_file[:-9]
        return {
            "data" : {"savefile": content, "character": char},
            "params" : {"start": time.time()}
        }

    def fetch_runs():
        if not config.local_source.enabled:
            return
        
        charcterDirects = []
        for file in os.listdir(os.path.join(os.sep, config.local_source.location + os.sep, "runs")):
            try:
                if file.endswith("DAILY"): #We don't want daily runs I mean at least I dont
                    continue
                charcterDirects.append(file)
            except Exception as e:
                print("Cannot find runs directory as error : " , repr(e))
                return

        for character in charcterDirects:
            shutil.copytree(os.path.join(os.sep, config.local_source.location + os.sep, "runs", character), os.path.join(os.getcwd(), "data", "runs", "0"), copy_function=shutil.copy, dirs_exist_ok=True)