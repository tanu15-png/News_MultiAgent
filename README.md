ResearchMind

AI-powered multi-agent research and news discovery platform

ResearchMind is an AI-powered web application that helps users stay
updated with recent news and turn any research topic into a structured
research report.

It combines Tavily web/news search, Mistral AI, LangChain
agents, and a multi-stage research pipeline to move from information
discovery to deeper reading, report generation, and critical review.

🚀 Project Overview

Researching a topic manually often requires switching between search
engines, opening multiple articles, extracting useful information,
writing notes, and checking the final result.

ResearchMind simplifies this workflow through specialized AI components.

The homepage first presents news from the past 24 hours, dynamically
fetched through the Tavily API. Users can refresh the feed to request a
fresh set of results.

For deeper research, users can enter any topic and start the multi-agent
research pipeline:

User Topic
    ↓
Search Agent
    ↓
Reader Agent
    ↓
Writer Chain
    ↓
Critic Chain
    ↓
Structured Research Report

🎯 Problem Statement

Finding reliable and useful information on a current topic can be
time-consuming.

A typical research process involves:

Searching for recent information

Identifying useful sources

Opening and reading long webpages

Extracting relevant information

Combining information from different sources

Writing a structured report

Reviewing the quality of the final report

ResearchMind addresses this problem by creating an AI-assisted research
workflow that separates these responsibilities into specialized stages.

💡 Solution

ResearchMind provides two connected experiences.

1. Latest 24-Hour News

The homepage dynamically retrieves recent news using Tavily.

The news discovery layer:

Searches for important news from the past 24 hours

Uses a category-oriented prompt covering areas such as technology,
AI, business, science, politics, environment, and trading

Displays article title, source, summary, and URL

Allows users to expand individual news cards

Provides a Refresh 24h News button that triggers a new API
request

2. Deep Research Pipeline

Users can enter a research topic and run a multi-stage AI workflow.

Search Agent --- Finds recent, reliable and relevant web information
using the Tavily search tool.

Reader Agent --- Selects a relevant URL and uses the scraping tool
to extract deeper webpage content.

Writer Chain --- Combines search results and scraped content to
generate a structured research report.

Critic Chain --- Reviews the generated report and provides a score,
strengths, areas for improvement, and a final verdict.

✨ Key Features

📰 Dynamic 24-hour news discovery

🔄 Refreshable news feed

🗂️ Category-oriented news retrieval

📖 Expandable news cards

🔎 AI-powered web research

🌐 Tavily web/news search integration

📄 Webpage content extraction

✍️ AI-generated research reports

🧐 AI critic/reviewer

📊 Research quality score and feedback

⬇️ Downloadable Markdown reports

🖥️ Streamlit web interface

🤖 Specialized multi-agent architecture

🧠 AI / Agent Architecture

News Discovery

Streamlit
   ↓
hrs24_news()
   ↓
get_latest_news()
   ↓
News Agent
   ↓
latest_news tool
   ↓
Tavily API
   ↓
Recent News
   ↓
Expandable News Cards

Research Pipeline

                    ┌─────────────────┐
                    │   User Topic    │
                    └────────┬────────┘
                             ↓
                    ┌─────────────────┐
                    │  Search Agent   │
                    │     Tavily      │
                    └────────┬────────┘
                             ↓
                    ┌─────────────────┐
                    │  Reader Agent   │
                    │  URL Scraping   │
                    └────────┬────────┘
                             ↓
                    ┌─────────────────┐
                    │  Writer Chain   │
                    │   Mistral AI    │
                    └────────┬────────┘
                             ↓
                    ┌─────────────────┐
                    │  Critic Chain   │
                    │   Mistral AI    │
                    └────────┬────────┘
                             ↓
                    ┌─────────────────┐
                    │ Research Report │
                    └─────────────────┘

The architecture separates information retrieval, reading, writing, and
review instead of asking a single LLM prompt to perform the entire
workflow.

🛠️ Technology Stack

Technology      Purpose

Python          Core application language
Streamlit       Web application interface
LangChain       Agent and LLM orchestration
Mistral AI      Language model used by agents and chains
Tavily          Web and news search
BeautifulSoup   Webpage text extraction
Requests        HTTP requests for webpage scraping
python-dotenv   Environment variable management
Rich            Terminal output formatting

📁 Project Structure

multi_agent_news/
│
├── app.py
├── agents.py
├── pipeline.py
├── tools.py
├── requirements.txt
├── README.md
├── .gitignore
└── .env

app.py

Contains the Streamlit interface, including the latest 24-hour news
feed, news refresh, expandable cards, research input, pipeline status,
report, critic feedback, and report download.

agents.py

Defines the Search Agent, Reader Agent, Latest News Agent, Writer Chain,
and Critic Chain.

tools.py

Contains the external tools used by the agents:

web_search

scrape_url

latest_news

pipeline.py

Controls the research workflow and connects:

Search → Read → Write → Critique

⚙️ Setup & Installation

1. Clone the repository

git clone <YOUR_PUBLIC_GITHUB_REPOSITORY_URL>
cd multi_agent_news

2. Create a virtual environment

Windows:

python -m venv .venv
.venv\Scripts\activate

Linux / WSL / macOS:

python3 -m venv .venv
source .venv/bin/activate

3. Install dependencies

pip install -r requirements.txt

4. Configure API keys

Create a .env file in the project root:

TAVILY_API_KEY=your_tavily_api_key
MISTRAL_API_KEY=your_mistral_api_key

Never commit .env or API keys to the public repository.

▶️ Running the Application

streamlit run app.py

Then open:

http://localhost:8501

📖 Usage

View Latest News

Open the application.

The Latest 24 Hours section loads automatically.

News is fetched dynamically through the Tavily API.

Click a news card to expand it.

Use Refresh 24h News to perform a fresh search.

Research a Topic

Enter a topic in Research a Topic.

Click Run Research Pipeline.

The Search Agent finds relevant web information.

The Reader Agent extracts deeper content from a selected source.

The Writer Chain generates the report.

The Critic Chain evaluates it.

Review or download the final report.

🔄 Research Workflow

Step 1 --- Search Agent

The Search Agent receives the user's topic and searches the web for
recent and reliable information.

Step 2 --- Reader Agent

The Reader Agent selects a relevant URL and uses scrape_url to extract
webpage content.

Step 3 --- Writer Chain

The Writer Chain combines the search results and scraped content and
generates:

Introduction

Key Findings

Conclusion

Sources

Step 4 --- Critic Chain

The Critic Chain evaluates the report and returns:

Score: X/10

Strengths:
- ...

Areas to Improve:
- ...

One line verdict:
...

🧪 Hackathon Demo Flow

Demo 1 --- Current News

Open ResearchMind
       ↓
Latest 24 Hours
       ↓
Fresh Tavily results
       ↓
Expand a news card
       ↓
Open original source
       ↓
Refresh 24h News
       ↓
New API results

Demo 2 --- AI Research

Example topic:

AI agents in software development

Then demonstrate:

Search Agent
      ↓
Reader Agent
      ↓
Writer Chain
      ↓
Critic Chain
      ↓
Final Report

This demonstrates actual AI usage across multiple stages of the
application.

🏆 Why ResearchMind?

ResearchMind focuses on a practical problem: turning scattered and
constantly changing web information into useful research.

Instead of treating AI as a single chatbot, the application uses
specialized components for different stages of the workflow.

The core idea is:

Discover → Read → Write → Critique

The application combines current information retrieval with AI reasoning
and review, giving users both current information and a deeper research
workflow.

🔮 Future Improvements

Deterministic one-article-per-category news retrieval

Source credibility scoring

Duplicate-news detection

More precise publication-time filtering

Multiple-source comparison

Citation verification

Research history

Saved reports

PDF export

Personalized news categories

Fact-checking agent

Parallel research agents

Public deployment

📌 Current Limitations

News availability depends on the Tavily API.

Some websites may block automated scraping or require JavaScript
rendering.

AI-generated reports should be reviewed before being treated as
authoritative.

The current category-oriented news prompt does not guarantee exactly
one article from every category.

The current system retrieves a limited number of articles for the
homepage.

👥 Team

Project: ResearchMind
Hackathon: InnovateX AI Hackathon

Team Members

Add team member name

Add team member name

Add team member name

📄 License

This project was created for the InnovateX AI Hackathon.

Add an open-source license if the project will be distributed for public
reuse.