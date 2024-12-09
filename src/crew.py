# src/crew.py

import logging
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from .tools.youtube_video_details_tool import YoutubeVideoDetailsTool
from .tools.youtube_video_search_tool import YoutubeVideoSearchTool
import os
from dotenv import load_dotenv, find_dotenv
from langchain_google_genai import GoogleGenerativeAI
from langchain_openai import OpenAI
from langchain.tools import Tool
from langchain_community.tools import HumanInputRun
from pydantic import BaseModel
from datetime import datetime
from typing import Union, Optional, Any
import re

load_dotenv(find_dotenv())

# human_tool = load_tools(['human'])
search_tool = YoutubeVideoSearchTool()
details_tool = YoutubeVideoDetailsTool()

google_llm = GoogleGenerativeAI(
    model="gemini-pro", google_api_key=os.getenv("GOOGLE_API_KEY")
)

openai_llm = OpenAI(
    model=os.getenv("OPENAI_MODEL_NAME"),   
    api_key=os.getenv("OPENAI_API_KEY")
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def generate_output_filename(topic: str) -> str:
    """Generate a unique filename based on topic and timestamp."""
    # Clean the topic string to be filesystem-friendly
    clean_topic = "".join(c if c.isalnum() or c in (' ', '-', '_') else '_' for c in topic)
    clean_topic = clean_topic.replace(' ', '_')
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"output/{clean_topic}_{timestamp}.md"

# Define a proper input schema for the human input tool
class HumanInputSchema(BaseModel):
    tool_input: Union[str, dict[str, Any]]
    

@CrewBase
class YouTubeAutomationAgent:
    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"
    
    def __init__(self, video_topic: str):
        self.video_topic = video_topic
        self.output_file = generate_output_filename(video_topic)
        # Ensure output directory exists
        os.makedirs("output", exist_ok=True)
    
    @agent
    def youtube_manager(self) -> Agent:
        return Agent(
            config=self.agents_config['youtube_manager'],
            verbose=True,
        )
        
    @agent
    def research_manager(self):
        return Agent(
            config=self.agents_config['research_manager'],
            verbose=True,
            tools=[search_tool, details_tool]
        )
    
    @agent
    def title_creator(self):
        return Agent(
            config=self.agents_config['title_creator'],
            verbose=True
        )
    
    @agent
    def description_creator(self):
        return Agent(
            config=self.agents_config['description_creator'],
            verbose=True
        )
    
    @agent
    def email_creator(self):
        human_input_run = HumanInputRun()
        human_input_tool = Tool(
            name="Human Input",
            description="Tool to get input from human",
            func=human_input_run.run,
            args_schema=HumanInputSchema
        )

        return Agent(
            config=self.agents_config['email_creator'],
            verbose=True,
            tools=[human_input_tool]
        )
    
    @task
    def manage_youtube_video_creation(self):
        return Task(
            config=self.tasks_config['manage_youtube_video_creation'],
            verbose=True,
            output_file=self.output_file
        )
        
    @task
    def manage_youtube_video_research(self):
        return Task(
            config=self.tasks_config['manage_youtube_video_research'],
            verbose=True,
        )
    
    @task
    def create_youtube_video_title(self):
        return Task(
            config=self.tasks_config['create_youtube_video_title'],
            verbose=True,
        )
    
    @task
    def create_youtube_video_description(self):
        return Task(
            config=self.tasks_config['create_youtube_video_description'],
            verbose=True,
        )
    
    @task
    def create_email_announcement_for_new_video(self):
        return Task(
            config=self.tasks_config['create_email_announcement_for_new_video'],
            verbose=True,
        )
    
    @crew
    def crew(self):
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
            manager_llm=openai_llm
        )