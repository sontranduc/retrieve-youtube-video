#
# use Google api to search youtube video by keywords, write the returned data to the files
#
# Author: Son Tranduc


import os
from pathlib import Path
import requests
import json
import common_variables as c

CurDir = os.getcwd()
path = Path(CurDir)
URL_VIDEO_SEARCH = "https://www.googleapis.com/youtube/v3/search?part=id,snippet&type=video&maxResults="+str(c.VIDEO_MAX_RESULTS_IN_PAGE)+"&q="


# search youtube by keywords and write playlist returned JSON to file
def searchByKeyword(keyword):
    print("Searching Keyword: ", keyword)
    API_key = c.get_api_key()
    print("Use API key:", API_key)
    
    # initialize token
    token = ""
    
    # setup locations to store the results: returned video details are dumped into files which located
    # in the folders that folder's name is the searched keyword
    results_directory = str(path.parent) + "\\results"
    directory_by_keyword = results_directory + "\\" + keyword
    print("Store video details at: ", directory_by_keyword)
    c.create_dir(directory_by_keyword)


    for n in range(c.NUMBER_OF_PAGE):
        page = n+1
        if page != 1:
            resp = requests.get(URL_VIDEO_SEARCH+keyword+"&key="+API_key+'&pageToken='+token)
            pageName = token
        else:
            resp = requests.get(URL_VIDEO_SEARCH+keyword+"&key="+API_key)
            pageName = "first" 
        p = resp.json()

        try: 
            token = p["nextPageToken"]
        except: 
            token = ''

        # test if API_key still has quota (if key ran out its quota, the "items" won't be returned)
        try:
            p["items"]
        except:
            print("OUT OF QUOTA")
            return False
        

        # trim the results       
        c.TrimTheList(p)
 
        # dump results to file
        with open(directory_by_keyword + "/" + str(pageName) + ".txt", "w", encoding='utf-8') as outfile:
            json.dump(p, outfile, ensure_ascii=False, indent=4)  
            
    return True



if __name__ == "__main__":

    print("......retrieving ....please wait .....")

    for i in range(len(c.keywords)):  
        # if api is out of quota, start again with new api
        if searchByKeyword(c.keywords[i]) == False:
            searchByKeyword(c.keywords[i])

        print("Done!")



