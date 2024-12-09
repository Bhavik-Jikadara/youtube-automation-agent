# main.py
from src.crew import YouTubeAutomationAgent

def run():
    """
    Run the crew.
    """
    inputs = {
        "video_topic" : "How to Build Your First Streamlit App: A Beginner's Guide",
        "video_details" : """
        In this tutorial, we'll walk you through the process of creating your very first Streamlit app, even if you're a complete beginner! Streamlit is a powerful and easy-to-use framework for building interactive web applications with Python. Whether you're looking to create data visualizations, machine learning models, or simple dashboards, Streamlit makes it quick and fun to get your project online.

        In this video, we will:

        Install Streamlit and set up the environment
        Understand the basic structure of a Streamlit app
        Create a simple interactive web app with a few lines of code
        Explore key Streamlit features such as widgets, charts, and text elements
        
        By the end of this tutorial, you'll have a functional Streamlit app up and running, and the confidence to build more advanced apps in the future. Perfect for Python developers and anyone looking to dive into data science web apps!
        """
    }
    
    YouTubeAutomationAgent(video_topic=inputs["video_topic"]).crew().kickoff(inputs=inputs)

if __name__ == "__main__":
    run()