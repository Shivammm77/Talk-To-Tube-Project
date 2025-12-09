from fastapi import FastAPI
from pydantic import BaseModel
import yt 
from fastapi.middleware.cors import CORSMiddleware
import yt_utils
from Auth.routes import router as auth_router
from users.routes import router as users_router
import requests
from dotenv import load_dotenv
import os
load_dotenv()
yt_api = os.getenv("youtube_api")
class Query(BaseModel):
    query : str

app = FastAPI()
app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(users_router, prefix="/users", tags=["users"])

app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,  # Allow cookies, authorization headers, etc.
        allow_methods=["*"],     # Allow all standard HTTP methods (GET, POST, PUT, DELETE, etc.)
        allow_headers=["*"],     # Allow all headers in the request
    )

@app.get("/")
def welcome():
    return {"message":"Welcome here"}

from urllib.parse import urlparse, parse_qs

@app.post("/ask/")
def ask_from_url(q: Query, url: str):
    parsed_url = urlparse(url)
    video_id = parse_qs(parsed_url.query).get('v', [None])[0]
    if not video_id:
        return {"error": "Invalid YouTube URL"}
    response = yt.ask_question(video_id, q.query)
    return response
    
@app.get("/video_info")
def video_data(video_url):
 video_id = yt_utils.extraxt_id(video_url)

 youtube_api1 = (f"https://www.googleapis.com/youtube/v3/videos?part=snippet&id={video_id}&key={yt_api}")
 response = requests.get(youtube_api1).json()
 if not response.get("items"):
       return {"error" : "Video not found"}
 snippet = response["items"][0]["snippet"]  
 return {
        "title" : snippet["title"],
        "thumbnail" : snippet["thumbnails"]["high"]["url"],
        "channel" : snippet["channelTitle"]
        
        }
print(video_data("https://www.youtube.com/watch?v=jxD0H79mdRI"))