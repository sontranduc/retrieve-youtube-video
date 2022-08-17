#!/usr/bin/env python
# -*- coding: UTF-8 -*-


import requests


key = [ "AIzaSyDHJDdRdq9YfMr2RGtWfPjykk4DDUjymLw",	#nailbookingmonitor
        "AIzaSyAVrDarPdlKoW38zZX1buTBVrEiAeqmGvg",	#vibdummy
        "AIzaSyACTxgdOL4R1oo79GhZWRU6VxENDJiSWi4",	#vibappdummy
        "AIzaSyDaN2Sj6YK_Hcf88wugHDsPvtMk46K2PRE",	#vietipbox
        "AIzaSyC4T6_S6Ec2MCwnANLLO4DTLWenVSSIUE0",	#tranducsolutions
        "AIzaSyCb6tmf5dS5tI1Z7noyUZBVuvQxHfJVN2Y"  #sontranduc33
        ]


# get key which has quota
def get_api_key():
    for api_key in key:
        url_api = 'https://www.googleapis.com/youtube/v3/search?part=snippet&key='+api_key
        code = requests.get(url_api)
        
        if (code.status_code==200): 
            break
    return api_key 

