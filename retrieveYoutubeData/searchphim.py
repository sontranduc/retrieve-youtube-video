	#
# use youtube api to search tv show with provided keywords, write the returned data to the files
#
# Author: Son Tranduc


import os
import os.path
import shutil
import stat
from os import listdir
import requests
import json
from common_variables import *

#API_key = get_api_key()
GitPath = "D:\\Desktop\\MyWorkPlace\\PhimYoutube"+"\\GitLab\\youtubepages\\YTphim\\"
URL_PLAYLIST_SEARCH = "https://www.googleapis.com/youtube/v3/search?part=id,snippet&type=playlist&maxResults=50&q="
URL_VIDEO_SEARCH = "https://www.googleapis.com/youtube/v3/search?part=id,snippet&type=video&maxResults=50&q="
URL_PLAYLIST = "https://www.googleapis.com/youtube/v3/playlistItems?part=id,snippet,contentDetails&maxResults=50"
NUMBER_OF_PAGE = 5



#keywords
phongSu = "phong+su+du+lich" #new
vanSon = "ky+su+van+son" #new
khoaiLangThang = "ky+su+khoai+lang+thang" #new

keywords = [\
                "phim+bo+hong+kong",\
                "phim+bo+han+quoc",\
                "phim+bo+trung+quoc",\
                "phim+bo+dai+loan",\
                "phim+an+do",\
                "phim+thai+lan",\
                "phim+bo+viet+nam",\
                "kenh+tvb+tieng+viet",\
                "phong+su+du+lich",\
                "ky+su+van+son",\
                "ky+su+khoai+lang+thang" \
           ]


# search youtube by keywords and write playlist returned JSON to file
def searchByKeyword(keyword):
    print(keyword)
    API_key = get_api_key()
    print(API_key)
    if (keyword != phongSu) and (keyword != vanSon) and (keyword != khoaiLangThang): # search phim bo with playlist
        
        countryPath = GitPath+keyword+"/"
        
        #first remove old directory, and then create new one
        create_dir(countryPath)

        #remove sub directory
        remove_sub_directory(countryPath)

        token = ""
        for n in range(NUMBER_OF_PAGE):
            page = n+1
            if page != 1:
                resp = requests.get(URL_PLAYLIST_SEARCH+keyword+"&key="+API_key+'&pageToken='+token)
                pageName = token
            else:
                resp = requests.get(URL_PLAYLIST_SEARCH+keyword+"&key="+API_key)
                pageName = "first" 
            p = resp.json()
            try: token = p["nextPageToken"]
            except: token = ''
            try: availablevideos = p["pageInfo"]["totalResults"]
            except: availablevideos = 1
            
            #test if API_key still has quota
            try:
                test = p["items"]
            except:
                print("OUT OF QUOTA")
                return False
                break

            # trim playlist        
            TrimTheList(p)
                    
                
            returnedPlaylists = p["items"]

            #write playlist pages to file
            with open(countryPath+str(pageName)+".txt", "w", encoding='utf-8') as outfile:
                json.dump(p, outfile, ensure_ascii=False, indent=4)              
            if returnedPlaylists:
                videoPageNum = 0
                # if sub directory does not exist, create it
                if os.path.isdir(countryPath+"sub") == False:
                    os.mkdir(countryPath+"sub")
                for playlist in returnedPlaylists:
                    if ("playlistId" in playlist["id"]):
                        videoPageNum +=1
                        playlistid = playlist["id"]["playlistId"]
                        get_playlist_page(countryPath, playlistid, videoPageNum, pageToken, API_key)
        return True
    else: #
        print("start Ky Su")
        countryPath = GitPath+keyword+"/"
        create_dir(countryPath)
        
        token = ""
        
        for n in range(NUMBER_OF_PAGE):
            page = n+1
            if page != 1:
                resp = requests.get(URL_VIDEO_SEARCH+keyword+"&key="+API_key+'&pageToken='+token)
                pageName = token
            else:
                resp = requests.get(URL_VIDEO_SEARCH+keyword+"&key="+API_key)
                pageName = "first" 
            p = resp.json()
            #print(p['items'])
            try: token = p["nextPageToken"]
            except: token = ''
            try: availablevideos = p["pageInfo"]["totalResults"]              
            except: availablevideos = 1
                
            
            #test if API_key still has quota
            try:
                test = p["items"]
            except:
                print("OUT OF QUOTA")
                return False
                break
           

            # trim playlist        
            TrimTheList(p)

            #returnedPlaylists = p["items"]

            with open(GitPath+keyword+"/"+str(pageName)+".txt", "w", encoding='utf-8') as outfile:
                json.dump(p, outfile, ensure_ascii=False, indent=4)  
                
        return True


# write video info from returned JSON to file
def get_playlist_page(country, url, vpage,pageToken, API_key ):

    response = requests.get(URL_PLAYLIST+"&key="+API_key+"&playlistId="+url)
    json_object = response.json()
    try: pageToken = json_object["nextPageToken"]
    except: pageToken = ""
    with open(country+"sub/"+url+".txt", "w", encoding='utf-8') as outfile:
        json.dump(json_object, outfile, ensure_ascii=False, indent=4)

    n=1
    while (pageToken != ""):
        n+=1
        response = requests.get(URL_PLAYLIST+"&key="+API_key+"&playlistId="+url+"&pageToken="+pageToken)
        json_object = response.json()
        try: pageToken = json_object["nextPageToken"]
        except: pageToken = ""
        with open(country+"sub/"+url+"PAGE"+str(n)+".txt", "w", encoding='utf-8') as outfile:
            json.dump(json_object, outfile, ensure_ascii=False, indent=4)


# function remove current directory (folder), the create a new one.
def create_dir(countryPath):
    #remove it first
    shutil.rmtree(countryPath, onerror=removeReadOnly)
    os.mkdir(countryPath)

# function remove sub directory
def remove_sub_directory(countryPath):
    if os.path.isdir(countryPath+"sub") == True:
        shutil.rmtree(countryPath+"/sub")

# defining a function that force removes read only documents
def removeReadOnly(func, path, excinfo):
    # Using os.chmod with stat.S_IWRITE to allow write permissions
    os.chmod(path, stat.S_IWRITE)
    func(path)

# function retrieve the list for single page, return json and Page name
def PullPlayListFromYoutube(page_num, yt_url, keyword, API_key, token):
    arr = []
    page = page_num + 1
    if page != 1:
        resp = requests.get(yt_url+keyword+"&key="+API_key+'&pageToken='+token)
        pageName = token
    else:
        resp = requests.get(yt_url+keyword+"&key="+API_key)
        pageName = "first" 
    p = resp.json()
    try: token = p["nextPageToken"]
    except: token = ''
    try: availablevideos = p["pageInfo"]["totalResults"]
    except: availablevideos = 1
    arr.append(p)
    arr.append(pageName)
    return arr


# function remove the list which has no thumpnail image
def TrimTheList(playlist):
    item = playlist["items"] # save page items
    playlist["items"] = []   # empty current page items
    for i in range(len(item)):
        if (item[i]["snippet"]["thumbnails"]["default"]["url"] != "https://i.ytimg.com/img/no_thumbnail.jpg"):
            playlist["items"].append(item[i])


            
print(GitPath)
#page = 0
pageToken = ""

print("......processing ....please wait .....")

print(GitPath)

for i in range(len(keywords)):
    
    # if api is out of quota, search again with new api
    if searchByKeyword(keywords[i]) == False:
        searchByKeyword(keywords[i])

    print("Done!")


