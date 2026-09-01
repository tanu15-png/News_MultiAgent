# ResearchMind — AI Multi-Agent Research Assistant

ResearchMind is an AI-powered web application that turns a single topic into a complete, fact-checked research report. It orchestrates four specialized AI agents — **Search**, **Reader**, **Writer**, and **Critic** — that work in sequence to gather live information from the web, extract deeper context, draft a structured report, and critically review the output before handing it back to the user.

Built for the 29–30 August Hackathon.

---

##  Problem Statement

Researching any topic thoroughly today means juggling multiple tabs, sifting through search results, reading full articles, and manually synthesizing everything into a coherent, well-structured write-up — a process that is slow, repetitive, and easy to get wrong.

**ResearchMind** solves this by automating the entire research workflow with a pipeline of cooperating AI agents, each responsible for one stage of the process, so a user can go from "a topic I want to understand" to "a structured, reviewed report" in a single click.

---

##  Features

- **Four-agent research pipeline**
  -  **Search Agent** — queries the live web (via Tavily) for recent, relevant sources on the topic.
  -  **Reader Agent** — scrapes and extracts clean, deep content from the most relevant source found.
  -  **Writer Chain** — synthesizes the gathered research into a structured report (Introduction, Key Findings, Conclusion, Sources).
  -  **Critic Chain** — independently reviews the report, scores it out of 10, and lists strengths and areas to improve.
- **Live pipeline visualization** — a real-time UI panel showing each agent's status (waiting / running / done) as the pipeline executes.
- **Clean, modern web interface** built with Streamlit, including example topic chips for quick testing.
- **Downloadable output** — export the final report as a Markdown (`.md`) file.
- **Actual AI agent usage** — powered by [LangChain](https://www.langchain.com/) agents and [Mistral AI](https://mistral.ai/) (`mistral-medium-3-5`) for reasoning, tool use, and text generation.

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Frontend / UI | [Streamlit](https://streamlit.io/) |
| Agent framework | [LangChain](https://www.langchain.com/) (`create_agent`) |
| LLM | [Mistral AI](https://mistral.ai/) via `langchain-mistralai` |
| Web search tool | [Tavily API](https://tavily.com/) |
| Web scraping | `requests` + `BeautifulSoup4` |
| Config | `python-dotenv` |
| Language | Python 3.10+ |

---

##  Project Structure

```
multi_agent_news/
├── agents.py         # Agent + chain definitions (search, reader, writer, critic)
├── tools.py           # Tool implementations: web_search (Tavily), scrape_url (BeautifulSoup)
├── pipeline.py         # Orchestrates the 4-agent pipeline end-to-end (CLI runnable)
├── app.py             # Streamlit web application (UI + pipeline integration)
├── requirements.txt      # Python dependencies
├── .env             # API keys (not committed — see setup below)
├── .gitignore
└── README.md
```

---

##  Setup / Installation

### 1. Clone the repository

```bash
git clone https://github.com/<your-username>/multi_agent_news.git
cd multi_agent_news
```

### 2. Create and activate a virtual environment

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root with the following keys:

```env
TAVILY_API_KEY=your_tavily_api_key_here
MISTRAL_API_KEY=your_mistral_api_key_here
```

- Get a Tavily API key from [tavily.com](https://tavily.com/)
- Get a Mistral API key from [console.mistral.ai](https://console.mistral.ai/)

---

## ▶️ Usage

### Run as a web app (recommended)

```bash
streamlit run app.py
```

Then open the local URL Streamlit prints (usually `http://localhost:8501`) in your browser:

1. Enter a research topic in the input box (or click one of the example chips).
2. Click **Run research →**.
3. Watch the four-agent pipeline progress in real time.
4. Read the generated **Final Research Report** and the **Critic Feedback** below it.
5. Optionally, click **Download Report (.md)** to save the report locally.

### Run from the command line

```bash
python pipeline.py
```

You'll be prompted to enter a topic, and the pipeline will print each stage's output (search results, scraped content, final report, and critic feedback) directly to the terminal.

---

## 🧠 How It Works

```
User Topic
    │
    ▼
1. Search Agent  ──► Tavily web search → titles, URLs, snippets
    │
    ▼
2. Reader Agent  ──► Scrapes the most relevant URL for deeper content
    │
    ▼
3. Writer Chain  ──► Synthesizes research into a structured report
    │
    ▼
4. Critic Chain  ──► Scores and critiques the report
    │
    ▼
Final Report + Feedback (displayed in UI, downloadable as .md)
```

---

## 🚀 Future Improvements

- Adding RAG so the system can retrieve the most relevant evidence from the scraped research instead of simply passing all the extracted content to the LLM.
- Support multiple source scraping (not just the single top URL) for richer reports.
- Add citation-level linking between report claims and their source URLs.
- Allow the Critic Agent's feedback to trigger an automatic re-draft loop.
- Add report history / session persistence across runs.

---



