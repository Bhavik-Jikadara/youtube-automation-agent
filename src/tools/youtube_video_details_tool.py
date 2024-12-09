from typing import Type
from crewai_tools import BaseTool
from pydantic import BaseModel, Field
import os
import requests
import logging
from dotenv import load_dotenv, find_dotenv

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
load_dotenv(find_dotenv())

class VideoDetails(BaseModel):
    title: str
    view_count: int
    like_count: int
    dislike_count: int
    comment_count: int
    channel_subscriber_count: int

class YoutubeVideoDetailsToolInput(BaseModel):
    """Input for YoutubeVideoDetailsTool."""
    video_id: str = Field(..., description="The ID of the YouTube video.")

class YoutubeVideoDetailsTool(BaseTool):
    name: str = "Get YouTube Video Details"
    description: str = "Retrieves details for a specific YouTube video."
    args_schema: Type[BaseModel] = YoutubeVideoDetailsToolInput

    def _run(self, video_id: str) -> VideoDetails:
        # Validate API key
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("YouTube API key is not set in environment variables")

        # Fetch Video Details
        try:
            video_details = self._fetch_video_details(api_key, video_id)
            channel_details = self._fetch_channel_details(api_key, video_details['channel_id'])

            return VideoDetails(
                title=video_details['title'],
                view_count=video_details['view_count'],
                like_count=video_details['like_count'],
                dislike_count=video_details['dislike_count'],
                comment_count=video_details['comment_count'],
                channel_subscriber_count=channel_details['subscriber_count']
            )
        except Exception as e:
            logger.error(f"Error fetching YouTube video details: {e}")
            raise

    def _fetch_video_details(self, api_key: str, video_id: str) -> dict:
        """Fetch detailed information for a specific video."""
        url = "https://www.googleapis.com/youtube/v3/videos"
        params = {
            "part": "snippet,statistics",
            "id": video_id,
            "key": api_key
        }

        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            
            items = response.json().get("items", [])
            if not items:
                raise ValueError(f"No video found with ID: {video_id}")

            item = items[0]
            return {
                'title': item["snippet"]["title"],
                'channel_id': item["snippet"]["channelId"],
                'view_count': int(item["statistics"].get("viewCount", 0)),
                'like_count': int(item["statistics"].get("likeCount", 0)),
                'dislike_count': int(item["statistics"].get("dislikeCount", 0)),
                'comment_count': int(item["statistics"].get("commentCount", 0))
            }
        except requests.RequestException as e:
            logger.error(f"Request failed for video details: {e}")
            raise
        except (KeyError, ValueError, TypeError) as e:
            logger.error(f"Error parsing video details: {e}")
            raise

    def _fetch_channel_details(self, api_key: str, channel_id: str) -> dict:
        """Fetch channel statistics."""
        url = "https://www.googleapis.com/youtube/v3/channels"
        params = {
            "part": "statistics",
            "id": channel_id,
            "key": api_key
        }

        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            
            items = response.json().get("items", [])
            if not items:
                raise ValueError(f"No channel found with ID: {channel_id}")

            item = items[0]
            return {
                'subscriber_count': int(item["statistics"].get("subscriberCount", 0))
            }
        except requests.RequestException as e:
            logger.error(f"Request failed for channel details: {e}")
            raise
        except (KeyError, ValueError, TypeError) as e:
            logger.error(f"Error parsing channel details: {e}")
            raise