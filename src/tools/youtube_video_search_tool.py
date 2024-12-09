import requests
import os
from typing import List, Type
from pydantic import BaseModel, Field
from crewai_tools import BaseTool
from datetime import datetime, timezone
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

class VideoSearchResult(BaseModel):
    video_id: str
    title: str
    channel_id: str
    channel_title: str
    days_since_published: int

class YoutubeVideoSearchToolInput(BaseModel):
    keyword: str = Field(..., description="The search keyword.")
    max_results: int = Field(
        default=10, description="The maximum number of results to return."
    )

class YoutubeVideoSearchTool(BaseTool):
    name: str = "Search YouTube Videos"
    description: str = "Searches YouTube videos based on a keyword and returns a list of video search results."
    args_schema: Type[BaseModel] = YoutubeVideoSearchToolInput

    def _run(self, keyword: str, max_results: int = 10) -> List[VideoSearchResult]:
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("YouTube API key is not set in environment variables")

        url = "https://www.googleapis.com/youtube/v3/search"
        params = {
            "part": "snippet",
            "q": keyword,
            "maxResults": max_results,
            "type": "video",
            "key": api_key
        }

        try:
            # Print out the full request URL for debugging
            print(f"Request URL: {url}")
            print(f"Request Params: {params}")

            response = requests.get(url, params=params)
            
            # More detailed error handling
            if response.status_code != 200:
                print(f"Error Response: {response.text}")
                response.raise_for_status()

            data = response.json()
            items = data.get("items", [])

            results = []
            for item in items:
                try:
                    video_id = item["id"]["videoId"]
                    title = item["snippet"]["title"]
                    channel_id = item["snippet"]["channelId"]
                    channel_title = item["snippet"]["channelTitle"]
                    publish_date = datetime.fromisoformat(
                        item["snippet"]["publishedAt"].replace('Z', '+00:00')).astimezone(timezone.utc)
                    days_since_published = (datetime.now(
                        timezone.utc) - publish_date).days
                    results.append(VideoSearchResult(
                        video_id=video_id,
                        title=title,
                        channel_id=channel_id,
                        channel_title=channel_title,
                        days_since_published=days_since_published
                    ))
                except KeyError as parse_error:
                    print(f"Error parsing video item: {parse_error}")
                    print(f"Problematic item: {item}")

            return results

        except requests.RequestException as e:
            print(f"Request failed: {e}")
            raise