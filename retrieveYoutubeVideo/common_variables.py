#!/usr/bin/env python
# -*- coding: UTF-8 -*-


import requests
import os
import shutil
import stat


##################################################################################
#                                 
#                            USER defined variables
#
##################################################################################

NUMBER_OF_PAGE = 4
VIDEO_MAX_RESULTS_IN_PAGE = 20   # max = 50

# keywords to search: you can modify keyword list
keywords = [
                "action+movies",\
                "drama+movies",\
                "comedy+movies"
           ]


# sample API: use your own API keys, and add as many key as you want
key = [	"xxx",	#key1
		"yyy",	#key2
		"xxx",	#key3
		]




#####################################################################################
#
#          Helper Functions
#
#####################################################################################

# get key which has quota
def get_api_key():
    for api_key in key:
        url_api = 'https://www.googleapis.com/youtube/v3/search?part=snippet&key='+api_key
        code = requests.get(url_api)
        
        # test if key still has available quota
        if (code.status_code==200): 
            break
    return api_key 


# function remove current directory (folder), the create a new one.
def create_dir(the_path):
    #remove it first
    if os.path.isdir(the_path):
        shutil.rmtree(the_path, onerror=removeReadOnly)
    os.mkdir(the_path)


# defining a function that force removes read only documents
def removeReadOnly(func, the_path, excinfo):
    # Using os.chmod with stat.S_IWRITE to allow write permissions
    os.chmod(the_path, stat.S_IWRITE)
    func(the_path)


# function remove video results which have no thumpnail image
def TrimTheList(obj):
    item = obj["items"] # save page items
    obj["items"] = []   # empty current page items
    for i in range(len(item)):
        if (item[i]["snippet"]["thumbnails"]["default"]["url"] != "https://i.ytimg.com/img/no_thumbnail.jpg"):
            obj["items"].append(item[i])