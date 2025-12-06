# from dotenv import load_dotenv
# import os
# import requests 
# import re
# load_dotenv()
# youtube_api = os.getenv("youtube_api")
# def extraxt_video_id(url : str):
#     match = re.search(r"(?:v=|youtu\.be/)([a-zA-Z0-9_-]{11})" , url)
#     return match.group(1) if match else None
# def youtube_data(video_url:str):
#     video_id = extraxt_video_id(video_url)
#     if not video_id :
#         return {"error" : "Invalid Youtube Url"}
#     youtube_api = (
#         f"https://www.googleapis.com/youtube/v3/videos?part=snippet&id={video_id}&key={youtube_api}"
#     )
#     response = requests.get(youtube_api).json()
#     if not response.get("items"):
#        return {"error" : "Video not found"}
#     snippet = response["items"][0]["snippet"]  
#     return {
#         "title" : snippet["title"],
#         "thumbnail" : snippet["thumbnails"]["high"]["url"],
#         "channel" : snippet["channelTitle"]
        
#         }

# dotenv se api -> url se video id -> se then using api return name thumbnail
from dotenv import load_dotenv
import requests
import re
import os
load_dotenv()
yt_api = os.getenv("youtube_api")
def extraxt_id(url):
  video_id = re.search(r"(?:v=|youtu\.be/)([a-zA-Z0-9_-]{11})" , url)
  return video_id.group(1) if video_id else None
def youtube_data(url):
     video_id = extraxt_id(url)
     if not video_id :
         return {"message" : "wrong id you give"}
     youtube_url = (f"https://www.googleapis.com/youtube/v3/videos?part=snippet&id={video_id}&key={yt_api}")
     response = requests.get(youtube_url).json()
     snippet = response["items"][0]["snippet"]  
     return {
        "title" : snippet["title"],
         "thumbnail" : snippet["thumbnails"]["high"]["url"],
        "channel" : snippet["channelTitle"]
        
       }

