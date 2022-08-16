"""
youtube.ipynb

author: Deekshith Reddy Addela
deekshithreddyaddel@gmail.com

last updated on: 17/07/2020
"""

import json
import requests
import difflib
import pandas as pd

# api_key = ""
api_key = ""

def getData(url):
    response = requests.get(url)
    if response.status_code == 200:
        return json.loads(response.text.encode('utf-8'))
    print(json.loads(response.text.encode('utf-8')))

def getChennelId(name):
    url = f"https://www.googleapis.com/youtube/v3/search?key={api_key}&q={name}&part=snippet"
    data = getData(url)
    channels = set()
    for channel in data['items']:
        channels.add(
            json.dumps(
                {
                    "channelId" :channel.get('snippet',dict()).get('channelId',''),
                    "channelTitle" :channel.get('snippet',dict()).get('channelTitle','')
                }
            )
        )
    channels = [json.loads(channel) for channel in channels]
    for channel in channels:
        match = difflib.SequenceMatcher(None, name.lower(), channel.get('channelTitle','').lower()).ratio()*100
        if match == 100:
            return channel.get('channelId','')
        elif match >= 90:
            channelId = channel.get('channelId','')
    return channelId

def getChannelData(channelId):
    curl = f"https://www.googleapis.com/youtube/v3/channels?part=statistics&part=snippet&id={c}&key={api_key}"
    cdata = getData(curl)

    channel = cdata['items'][0]
    ChannelInfo = {
        "channelId" : channel.get('id',''),
        "channelTitle" : channel.get('snippet',dict()).get('title',''),
        "channelDescription" : channel.get('snippet',dict()).get('description',''),
        "publishedAt" : channel.get('snippet',dict()).get('publishedAt',''),
        "subscriberCount" : channel.get('statistics',dict()).get('subscriberCount',''),
        "videoCount" : channel.get('statistics',dict()).get('videoCount',''),
        "viewCount" : channel.get('statistics',dict()).get('viewCount',''),
    }
    return ChannelInfo

def getVideoIds(channelId):
    cvdata = []
    nextPageToken = ""
    while True: 
        csurl = f"https://www.googleapis.com/youtube/v3/search?channelId={channelId}{nextPageToken}&part=id&maxResults=30&key={api_key}"
        csdata = getData(csurl)
        cvdata.append(csdata)
        nextPageToken = f"&pageToken={csdata.get('nextPageToken', '')}"
        if not nextPageToken:
            break
    print("channelData :", len(cvdata))

    videoIds=[]
    playlistIds=[]
    for v in cvdata:
        video = v['items']
        if video['id'].get('videoId',''):
            videoIds.append(video['id'].get('videoId',''))
        elif video['id'].get('playlistId',''):
            playlistIds.append(video['id'].get('playlistId',''))
    print("playlistIds :",len(playlistIds))
    print("videoIds :", len(videoIds))
    return videoIds

def getVideoIds(channelId):
    cvdata = []
    nextPageToken = ""
    while True: 
        csurl = f"https://www.googleapis.com/youtube/v3/search?channelId={channelId}{nextPageToken}&part=id&maxResults=30&key={api_key}"
        csdata = getData(csurl)
        cvdata.append(csdata)
        nextPageToken = f"&pageToken={csdata.get('nextPageToken', '')}"
        if not nextPageToken:
            break
    print("channelData :", len(cvdata))

    videoIds=[]
    playlistIds=[]
    for v in cvdata:
        video = v['items']
        if video['id'].get('videoId',''):
            videoIds.append(video['id'].get('videoId',''))
        elif video['id'].get('playlistId',''):
            playlistIds.append(video['id'].get('playlistId',''))
    print("playlistIds :",len(playlistIds))
    print("videoIds :", len(videoIds))
    return videoIds

def getVideoData(videoIds):
    videoData = []
    for id in videoIds:
        vurl = f"https://www.googleapis.com/youtube/v3/videos?part=id&part=snippet&part=statistics&part=contentDetails&id={id}&key={api_key}"
        vdata = getData(vurl)
        videoData.append(vdata)

    output = []
    for v in videoData:
        video = v['items']
        output.append(
            {   
                "channelId" : video.get('snippet',dict()).get('channelId',''),
                "channelTitle" : video.get('snippet',dict()).get('channelTitle',''),
                "videoId" : video.get('id',''),
                "videoUrl" : f"https://www.youtube.com/watch?v={video.get('id','')}",
                "title" : video.get('snippet',dict()).get('localized',dict()).get('title',''),
                "description" : video.get('snippet',dict()).get('description',''),
                "publishedAt" : video.get('snippet',dict()).get('publishedAt',''),
                "duration" : video.get('contentDetails',dict()).get('duration',''),
                "viewCount" : video.get('statistics',dict()).get('viewCount',''),
                "likeCount" : video.get('statistics',dict()).get('likeCount',''),
                "dislikeCount" : video.get('statistics',dict()).get('dislikeCount',''),
                "commentCount" : video.get('statistics',dict()).get('commentCount',''),
                "tags" : "",
                "embedvideo" : f"""<iframe width="1440" height="762" src="https://www.youtube-nocookie.com/embed/{video.get('id','')}" frameborder="0" allow="autoplay; encrypted-media" allowfullscreen></iframe>"""
            }
        )
    return output

def toCsv(fileName, data=output):
    df = pd.DataFrame(data)
    df.to_csv(fileName, index=False, header=data[0].keys())

def driver(name):
    print("user/channel name :", name)

    channelId = getChennelId(name)
    print("channelId :", channelId)

    ChannelInfo = getChannelData(channelId)
    print("ChannelInfo :", ChannelInfo)

    videoIds = getVideoIds(channelId)

    output = getVideoData(videoIds)

    toCsv("videos.csv", data=output)

if __name__ == "__main__":
    name = "TGG EXTRAS"
    driver(name)
