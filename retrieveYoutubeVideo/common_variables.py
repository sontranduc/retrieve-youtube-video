#!/usr/bin/env python
# -*- coding: UTF-8 -*-


import requests

# sample API
key = [ "xxx",	#key1
        "yyy",	#key2
        "zzz"	#key3
        ]


# get key which has quota
def get_api_key():
    for api_key in key:
        url_api = 'https://www.googleapis.com/youtube/v3/search?part=snippet&key='+api_key
        code = requests.get(url_api)
        
        if (code.status_code==200): 
            break
    return api_key 

