#!/usr/bin/python3
################################################################################
# Copyright 2023 highstreet technologies GmbH
#
# Licensed under the Apache License, Version 2.0 (the 'License');
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an 'AS IS' BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import sys
import os
import subprocess
import json
import re
from typing import List

class Installer:

    def __init__(self, url, branch, dstFolder) -> None:
        self.downloadUrl = url
        self.publicUrlFormat = self.createPublicUrlFormat(url, branch)
        for key,value in self.publicUrlFormat.items():
            print(f'fmt={key}->{value}')
        self.branch = branch
        self.baseFolder = dstFolder
        self.subfolder = self.createSubFolder(url, branch)

    def createPublicUrlFormat(self, url:str, branch:str)->dict:
        fmt: dict = {}
        if url.endswith('.git'):
            url = url[:-4]
        if url.startswith('git@'):
            url = 'https://'+url[4:]
        fmt["raw"]=url+'/raw/'+branch+'/{}'
        fmt["blob"]=url+'/blob/'+branch+'/{}'
        return fmt
    def createSubFolder(self, gitUrl:str, branch:str) -> str:
        regex = r"^[^\/]+\/\/(.*)$"
        matches = re.finditer(regex, gitUrl)
        match = next(matches)
        name = match.group(1)
        if name.endswith('.git'):
            name=name[:-4]
        tmp:List[str]=[]
        hlp1 = name.split('/')
        for h in hlp1:
            if '.' in h:
                hlp2=h.split('.')
                for h2 in hlp2:
                    tmp.append(h2)
            else:
                tmp.append(h)

        return '/'.join(tmp)+'/'+branch 
    
    def getDstFolder(self)->str:
        return f'{self.baseFolder}/{self.subfolder}'
    
    def exec(self, cmd:str):
        output = subprocess.Popen(
            cmd, shell=True, stdout=subprocess.PIPE).stdout.read()
        return output

    def download(self) -> bool:
        print(f'try to download repo {self.downloadUrl} to {self.getDstFolder()}')
        self.exec(f'git clone --single-branch --branch {self.branch} {self.downloadUrl} {self.getDstFolder()}')
    
    def getFilesFiltered(self, lst:List[str]=None, path=None, root=None, filter=['yaml','yml'])->List[str]:
        if lst is None:
            lst=[]
        if root is None:
            root=str(self.getDstFolder())
        if path is None:
            path=self.getDstFolder()
        if os.path.exists(path) and os.path.isdir(path):
            # Iterate over all files and directories in the given path
            for filename in os.listdir(path):
                if filename.startswith("."):
                    continue
                fmatch=False
                # Get the absolute path of the file/directory
                abs_path = os.path.join(path, filename)
                # If it is a directory, recursively call this function on it
                if os.path.isdir(abs_path):
                    self.getFilesFiltered(lst=lst, path=abs_path, root=root, filter=filter )
                # If it is a file, print its absolute path
                elif os.path.isfile(abs_path):
                    for fi in filter:
                        if abs_path.endswith(fi):
                            fmatch=True
                            break
                    if not fmatch:
                        continue
                    relpath=abs_path[len(root)+1:]
                    lst.append(relpath)
        return lst

    def urlAlreadyInData(self, data:List[dict], pubUrl:str, key='publicURL'):
        for item in data:
            if key in item and item[key]==pubUrl:
                return True
        return False

    def createSchemaMap(self):
        schemaMapFile = f'{self.baseFolder}/schema-map.json'
        if os.path.isfile(schemaMapFile):
            with open(schemaMapFile) as fp:
                data = json.load(fp)
        else:
            data:List[dict] = []
        files = self.getFilesFiltered()
        for file in files:
            print(file)
            for key,value in self.publicUrlFormat.items():
                pubUrl = value.format(file)
                if self.urlAlreadyInData(data,pubUrl):
                    print(f'entry with url {pubUrl} already exists. ignoring')
                    continue
                data.append({
                    'publicURL': pubUrl,
                    'localURL': f'{self.subfolder}/{file}'
                })
        with open(schemaMapFile,'w') as fp:
            json.dump(data,fp)

def printHelp(msg:str = None):
    if msg is not None:
        print('ERR: {msg}')
    print('Installation script for VES additional formats')
    print(' usage: ')
    print('    install.py [OPTIONS]')
    print('       -c  CONFIG_FILE')
    print('       -d  DESTINATION_PATH')
    

args = sys.argv
args.pop(0)
configFilename = None
dstPath = None
while True:
    arg = args.pop(0)
    if arg == '-c':
        configFilename = args.pop(0)
    elif arg == '-d':
        dstPath = args.pop(0)
    else:
        printHelp(f'bad parameter {arg}')
        exit(1)
    if len(args)<=0:
        break

if configFilename is None or dstPath is None:
    printHelp('missing parameter')
    exit(1)


config = json.load(open(configFilename))
if not isinstance(config, list):
    printHelp('invalid config json. has to be a array')
    exit(1)

for item in config:
    dlRepo = item['repository']
    dlBranch = item['branch']
    installer = Installer(dlRepo, dlBranch, dstPath)
    installer.download()
    installer.createSchemaMap()
