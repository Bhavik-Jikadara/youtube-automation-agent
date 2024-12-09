# YouTube Automation Agent

## Overview

The YouTube Automation Agent is a Python-based application designed to streamline the process of creating and managing YouTube videos. It automates various tasks such as video research, title creation, description writing, and email announcements, leveraging the YouTube Data API and various AI tools. This agent-based architecture allows for modular and efficient handling of different aspects of video production.

## Agent Functionality

### YouTube Automation Agent

The `YouTubeAutomationAgent` class in `src/crew.py` is the core of the application. It orchestrates the various agents and tasks involved in the video creation process. Here’s a breakdown of its functionality:

- **Initialization**: When an instance of `YouTubeAutomationAgent` is created, it takes a `video_topic` as input and generates a unique output filename based on the topic and timestamp.

- **Agent Definitions**: The agent methods (`youtube_manager`, `research_manager`, `title_creator`, `description_creator`, and `email_creator`) define the roles of each agent, including their configurations and the tools they utilize.

- **Task Definitions**: The task methods (`manage_youtube_video_creation`, `manage_youtube_video_research`, `create_youtube_video_title`, `create_youtube_video_description`, and `create_email_announcement_for_new_video`) define the actions that each agent will perform, along with their expected outputs.

- **Crew Management**: The `crew` method combines all agents and tasks into a cohesive process, allowing them to work together to achieve the overall goal of video creation.

## How to Use the YouTube Automation Agent

1. **Define Your Video Topic**: In the `main.py` file, specify the topic of your YouTube video in the `inputs` dictionary. This topic will guide the research and content creation process.

   ```python
   inputs = {
       "video_topic": "Your Video Topic Here",
       "video_details": "Detailed description of your video content."
   }
   ```

2. **Configure Agents**: The agents are defined in `src/config/agents.yaml`. Each agent has a specific role and goal:
   - **YouTube Manager**: Oversees the entire video preparation process.
   - **Research Manager**: Conducts research to find high-performing videos on the same topic.
   - **Title Creator**: Generates potential titles for the video.
   - **Description Creator**: Writes a compelling description for the video.
   - **Email Creator**: Prepares an email announcement for the new video.

3. **Configure Tasks**: The tasks are defined in `src/config/tasks.yaml`. Each task corresponds to an action that an agent will perform, such as managing video creation or conducting research.

4. **Run the Application**: After configuring the topic and ensuring the agents and tasks are set up correctly, run the application. The agents will work sequentially to complete the video creation process, producing outputs such as a research table, video titles, descriptions, and email drafts.

## Usage

### Project Structure

```plaintext
.
├── main.py                     # Entry point for the application
├── src/
│   ├── crew.py                 # Main logic for the YouTube Automation Agent
│   ├── config/
│   │   ├── agents.yaml         # Configuration for agent roles and goals
│   │   └── tasks.yaml          # Configuration for tasks and expected outputs
│   └── tools/
│       ├── youtube_video_search_tool.py   # Tool for searching YouTube videos
│       └── youtube_video_details_tool.py  # Tool for fetching video details
└── .env                         # Environment variables
```

### Environment Variables

Ensure the following environment variables are set in a `.env` file:

```
GOOGLE_API_KEY=your_google_api_key
OPENAI_API_KEY=your_openai_api_key
OPENAI_MODEL_NAME=your_openai_model_name
```

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/Bhavik-Jikadara/youtube-automation-agent.git
   cd youtube-automation-agent
   ```

2. Install the required libraries:

   ```bash
   pip install -r requirements.txt
   ```

### Running the Application

To run the application, execute the following command:

```bash
python main.py
```

This will initiate the YouTube Automation Agent, which will start the process of managing video creation based on the defined inputs.

### Expected Outputs

- **Research Table**: A `.md` file containing details of competitive videos.
- **Video Titles**: A list of `10` potential video titles.
- **Video Description**: A comprehensive description for the video.
- **Email Announcement**: A draft email for promoting the video.

### Troubleshooting

- **API Errors**: Ensure that your API keys are correctly set and have the necessary permissions.
- **Network Issues**: Check your internet connection and firewall settings.
- **Library Conflicts**: Ensure all dependencies are correctly installed and up-to-date.

## Contributing

Contributions are welcome! Feel free to submit a pull request or open an issue for any enhancements or bug fixes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Acknowledgments

- [YouTube Data API](https://developers.google.com/youtube/v3)
- [Langchain](https://langchain.com/)
- [Pydantic](https://pydantic-docs.helpmanual.io/)
- [OpenAI](https://openai.com/)
- [Google Generative AI](https://ai.google/)