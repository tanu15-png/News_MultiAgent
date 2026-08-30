# 🔬 ResearchMind

> **Multi-Agent AI Research Assistant** --- search, scrape, write, and
> critique research on any topic.

ResearchMind is an AI-powered research web application built for the
**InnovateX AI Hackathon**. It uses a multi-stage LangChain pipeline to
turn a research topic into a structured report by combining web search,
source scraping, AI-assisted writing, and critical evaluation.

------------------------------------------------------------------------

## 📌 Project Overview

Researching a topic manually often requires repeatedly searching for
sources, opening multiple pages, extracting useful information,
organizing findings, and checking the quality of the final write-up.

**ResearchMind automates this workflow.**

A user enters a research topic, and the application runs the following
pipeline:

1.  🔎 **Search Agent** --- finds recent and relevant web information.
2.  📄 **Reader Agent** --- selects a relevant source and scrapes deeper
    content from it.
3.  ✍️ **Writer Chain** --- converts the gathered research into a
    structured report.
4.  🧐 **Critic Chain** --- evaluates the generated report and provides
    a score, strengths, and improvement areas.

The final report can be downloaded as a Markdown (`.md`) file.

------------------------------------------------------------------------

## 🎯 Problem Statement

Finding reliable information and turning it into a useful research
report is time-consuming.

A typical research workflow requires users to:

-   Search across multiple sources.
-   Identify useful and relevant resources.
-   Read and extract information from web pages.
-   Organize scattered findings.
-   Write a coherent report.
-   Review the report for quality and completeness.

**ResearchMind addresses this problem by creating an AI-assisted
research pipeline that performs these stages automatically.**

------------------------------------------------------------------------

## 💡 Solution

ResearchMind combines specialized AI components and external tools
rather than asking a single LLM to perform the entire task at once.

### Pipeline

``` text
                    ┌─────────────────────┐
                    │   User enters topic │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │    SEARCH AGENT     │
                    │  Tavily Web Search  │
                    └──────────┬──────────┘
                               │
                         Search results
                               │
                               ▼
                    ┌─────────────────────┐
                    │    READER AGENT     │
                    │ URL scraping +      │
                    │ content extraction  │
                    └──────────┬──────────┘
                               │
                       Detailed content
                               │
                               ▼
                    ┌─────────────────────┐
                    │    WRITER CHAIN     │
                    │  Research report    │
                    │     generation      │
                    └──────────┬──────────┘
                               │
                         Final report
                               │
                               ▼
                    ┌─────────────────────┐
                    │    CRITIC CHAIN     │
                    │ Score + feedback    │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │  Report + Feedback  │
                    └─────────────────────┘
```

------------------------------------------------------------------------

## ✨ Key Features

### 🔎 AI Web Research

The Search Agent uses **Tavily** to retrieve up to five search results
containing titles, URLs, and snippets.

### 📄 Deep Source Reading

The Reader Agent can select a relevant URL and use a scraping tool to
extract readable page content while removing elements such as scripts,
styles, navigation, and footers.

### ✍️ Structured Report Generation

The Writer Chain generates a professional report containing:

-   Introduction
-   Key Findings
-   Conclusion
-   Sources

### 🧐 Automated Critique

The Critic Chain reviews the generated report and returns:

-   Score out of 10
-   Strengths
-   Areas to improve
-   One-line verdict

### 🖥️ Interactive Web Interface

The application is built with **Streamlit** and provides:

-   Research topic input
-   Pipeline progress/status cards
-   Raw search results
-   Scraped content
-   Final formatted report
-   Critic feedback
-   Markdown report download

### 📥 Report Export

Generated reports can be downloaded directly from the application as
`.md` files.

------------------------------------------------------------------------

## 🏗️ Technology Stack

  -----------------------------------------------------------------------
  Technology                          Purpose
  ----------------------------------- -----------------------------------
  **Python**                          Core application language

  **Streamlit**                       Interactive web interface

  **LangChain**                       Agent and LLM orchestration

  **Mistral AI**                      Language model used for agents and
                                      report generation

  **Tavily**                          Web search

  **Requests**                        HTTP requests for page scraping

  **BeautifulSoup**                   HTML parsing and text extraction

  **python-dotenv**                   Environment variable management

  **Rich**                            Console output formatting
  -----------------------------------------------------------------------

------------------------------------------------------------------------

## 🧠 AI Architecture

ResearchMind uses a combination of **agents and chains**.

### 1. Search Agent

The Search Agent is created with a Mistral model and the `web_search`
tool.

Its responsibility is to find recent, reliable, and detailed information
about the user's topic.

``` text
User Topic
    ↓
Mistral AI Agent
    ↓
Tavily Search Tool
    ↓
Search Results
```

### 2. Reader Agent

The Reader Agent receives the search results and is instructed to select
a relevant URL and scrape it for deeper content.

``` text
Search Results
    ↓
Mistral AI Agent
    ↓
scrape_url Tool
    ↓
Cleaned Page Content
```

### 3. Writer Chain

The Writer Chain receives both search results and scraped content.

It uses a structured prompt to generate the final research report.

``` text
Search Results
      +
Scraped Content
      ↓
Mistral AI
      ↓
Structured Research Report
```

### 4. Critic Chain

The Critic Chain receives the generated report and evaluates it using a
fixed output structure.

``` text
Research Report
      ↓
Mistral AI
      ↓
Score + Strengths + Improvements + Verdict
```

------------------------------------------------------------------------

## 📂 Project Structure

``` text
multi_agent_news/
│
├── agents.py          # Search/Reader agents and Writer/Critic chains
├── tools.py           # Tavily search and URL scraping tools
├── pipeline.py        # Sequential research pipeline
├── app.py             # Streamlit web application
├── requirements.txt   # Python dependencies
├── .env               # API keys (local only)
├── .gitignore         # Files excluded from Git
└── README.md          # Project documentation
```

------------------------------------------------------------------------

## 🔄 How the Pipeline Works

The main research workflow is implemented in `pipeline.py`.

### Step 1 --- Search

The application creates the Search Agent and asks it to find:

> recent, reliable and detailed information

about the supplied topic.

The resulting agent response is stored as `search_results`.

### Step 2 --- Read

The Reader Agent receives the search output and is asked to:

-   identify the most relevant URL
-   scrape that resource
-   extract deeper content

The scraped output is stored as `scraped_content`.

### Step 3 --- Write

The search results and scraped content are combined and passed to the
Writer Chain.

The Writer Chain creates the final report with:

-   Introduction
-   Key Findings
-   Conclusion
-   Sources

### Step 4 --- Critique

The generated report is passed to the Critic Chain.

The critic produces a structured evaluation:

``` text
Score: X/10

Strengths:
- ...

Areas to Improve:
- ...

One line verdict:
...
```

------------------------------------------------------------------------

## ⚙️ Installation

### Prerequisites

Make sure you have:

-   Python 3.10+ recommended
-   A Mistral AI API key
-   A Tavily API key

### 1. Clone the repository

``` bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd multi_agent_news
```

### 2. Create a virtual environment

#### Windows

``` bash
python -m venv .venv
.venv\Scripts\activate
```

#### macOS / Linux

``` bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

``` bash
pip install -r requirements.txt
```

------------------------------------------------------------------------

## 🔐 Environment Variables

Create a `.env` file in the project root:

``` env
MISTRAL_API_KEY=your_mistral_api_key
TAVILY_API_KEY=your_tavily_api_key
```

**Never commit your `.env` file or API keys to GitHub.**

Make sure `.env` is included in `.gitignore`.

------------------------------------------------------------------------

## ▶️ Running the Application

Start the Streamlit application with:

``` bash
streamlit run app.py
```

Streamlit will provide a local URL, normally similar to:

``` text
http://localhost:8501
```

Open that URL in your browser.

------------------------------------------------------------------------

## 🚀 Usage

1.  Open the ResearchMind web application.
2.  Enter a research topic in the **Research Topic** field.
3.  Click **Run Research Pipeline**.
4.  Wait while the four pipeline stages execute.
5.  Review the generated research report.
6.  Open the raw search/scraped outputs if deeper inspection is needed.
7.  Review the Critic feedback and score.
8.  Download the final report as a Markdown file.

### Example Topics

``` text
LLM agents 2025
```

``` text
CRISPR gene editing
```

``` text
Fusion energy progress
```

------------------------------------------------------------------------

## 📊 Output

For each research request, the application produces:

### Search Output

Web search results with:

-   Title
-   URL
-   Snippet

### Reader Output

Extracted text from a selected web resource.

### Final Report

A structured research document containing:

-   Introduction
-   Key Findings
-   Conclusion
-   Sources

### Critic Feedback

An evaluation containing:

-   Score
-   Strengths
-   Areas to Improve
-   One-line Verdict

------------------------------------------------------------------------

## 🛡️ Error Handling

The URL scraping tool uses a timeout and catches request/scraping
exceptions.

If scraping fails, the tool returns an error message instead of crashing
the entire scraping function.

The application also checks whether a research topic has been entered
before starting the pipeline.

------------------------------------------------------------------------

## 🔒 Security & API Key Handling

This project requires external API keys.

For safe usage:

-   Store keys in `.env`.
-   Add `.env` to `.gitignore`.
-   Never hard-code API keys in Python files.
-   Never push API keys to the public repository.
-   If a key is accidentally exposed, revoke/rotate it immediately.

------------------------------------------------------------------------

## ⚠️ Limitations

The current version has several practical limitations:

-   Web-page scraping depends on the target website allowing normal HTTP
    requests.
-   JavaScript-heavy or protected websites may not return useful
    content.
-   The Reader Agent currently works from a limited portion of the
    search results passed to it.
-   Search results depend on Tavily's available web data.
-   AI-generated reports should still be reviewed by a human before
    being treated as authoritative.
-   The current workflow is sequential rather than running agents in
    parallel.

These limitations can be addressed in future iterations.

------------------------------------------------------------------------

## 🔮 Future Improvements

Potential improvements include:

-   Multiple-source deep reading instead of a single selected URL.
-   Source credibility/reliability scoring.
-   Citation verification.
-   Fact-checking agent.
-   Parallel research agents for different subtopics.
-   Automatic report regeneration based on critic feedback.
-   PDF/DOCX export.
-   Research history and saved reports.
-   More advanced source filtering.
-   Better handling of JavaScript-rendered websites.
-   Human-in-the-loop approval before final report generation.
-   Persistent research memory.

------------------------------------------------------------------------

## 🏆 Hackathon Relevance

ResearchMind is designed around the InnovateX Hackathon requirements:

  -----------------------------------------------------------------------
  Requirement                         Implementation
  ----------------------------------- -----------------------------------
  Working AI-powered project          Streamlit research application

  Real-world problem                  Automates time-consuming research
                                      workflow

  Actual AI usage                     Mistral AI-powered agents and
                                      chains

  Multiple AI components              Search Agent, Reader Agent, Writer
                                      Chain, Critic Chain

  Web application                     Streamlit interface

  Public GitHub repository            Project can be hosted in a public
                                      repository

  Documentation                       This README contains setup, usage,
                                      architecture, and features
  -----------------------------------------------------------------------

------------------------------------------------------------------------

## 📁 Important Files

### `tools.py`

Contains the two external tools:

-   `web_search()` --- Tavily-powered web search.
-   `scrape_url()` --- requests + BeautifulSoup webpage extraction.

### `agents.py`

Contains:

-   Search Agent
-   Reader Agent
-   Writer Chain
-   Critic Chain

### `pipeline.py`

Connects the components into the sequential research workflow.

### `app.py`

Provides the Streamlit UI and executes the research workflow from the
browser.

------------------------------------------------------------------------

## 🧪 Development

When contributing changes, keep the project organized and use meaningful
commits.

Example:

``` bash
git add .
git commit -m "Add research critic stage"
git push
```

Avoid committing:

``` text
.env
.venv/
__pycache__/
```

------------------------------------------------------------------------

## 👥 Team

**InnovateX Hackathon Project**

Team members:

-   Add Member 1
-   Add Member 2
-   Add Member 3
-   Add Member 4

> Replace the placeholders above with your actual team members before
> submission.

------------------------------------------------------------------------

## 📜 License

Add your preferred license here, for example:

``` text
MIT License
```

If this project is only being submitted for the hackathon, you can also
specify the repository's intended usage terms.

------------------------------------------------------------------------

## ⭐ Final Note

ResearchMind demonstrates how specialized AI components can collaborate
as a research workflow instead of relying on a single prompt.

**Search → Read → Write → Critique**

Built for the **InnovateX AI Hackathon**.
