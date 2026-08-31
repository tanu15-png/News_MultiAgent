import streamlit as st
import json
import re
import html

from datetime import datetime
from zoneinfo import ZoneInfo
from textwrap import dedent

from pipeline import run_research_pipeline, hrs24_news


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="ResearchMind",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# ============================================================
# CONSTANTS
# ============================================================

IST = ZoneInfo("Asia/Kolkata")


# ============================================================
# HTML HELPER
# ============================================================

def render_html(content: str):
    """
    Render custom HTML using Streamlit's HTML renderer.

    st.html() is used instead of st.markdown() so that
    HTML is rendered as HTML rather than displayed as code.
    """
    st.html(dedent(content))


# ============================================================
# TIME
# ============================================================

def get_current_ist():
    """Return current date/time in IST."""
    return datetime.now(IST)


def get_noon_today():
    """Return today's 12:00 PM IST."""
    now = get_current_ist()

    return now.replace(
        hour=12,
        minute=0,
        second=0,
        microsecond=0,
    )


# ============================================================
# NEWS PARSER
# ============================================================

def parse_news(raw_news):
    """
    Convert the response returned by hrs24_news()
    into a Python list.

    Expected format:

    [
        {
            "title": "...",
            "url": "...",
            "source": "...",
            "category": "...",
            "summary": "..."
        }
    ]
    """

    if raw_news is None:
        return []

    # Already parsed
    if isinstance(raw_news, list):
        return raw_news

    # Dictionary response
    if isinstance(raw_news, dict):

        if isinstance(raw_news.get("news"), list):
            return raw_news["news"]

        if isinstance(raw_news.get("results"), list):
            return raw_news["results"]

        return []

    text = str(raw_news).strip()

    if not text:
        return []

    # Remove markdown JSON fences
    text = re.sub(
        r"^```json\s*",
        "",
        text,
        flags=re.IGNORECASE,
    )

    text = re.sub(
        r"^```\s*",
        "",
        text,
    )

    text = re.sub(
        r"\s*```$",
        "",
        text,
    )

    text = text.strip()

    # Try normal JSON
    try:

        data = json.loads(text)

        if isinstance(data, list):
            return data

        if isinstance(data, dict):

            if isinstance(data.get("news"), list):
                return data["news"]

            if isinstance(data.get("results"), list):
                return data["results"]

    except json.JSONDecodeError:
        pass

    # Sometimes the model adds text before/after JSON.
    # Try to extract the JSON array.
    start = text.find("[")
    end = text.rfind("]")

    if start != -1 and end != -1 and end > start:

        possible_json = text[start:end + 1]

        try:

            data = json.loads(possible_json)

            if isinstance(data, list):
                return data

        except json.JSONDecodeError:
            pass

    return []


# ============================================================
# DAILY NEWS FETCH
# ============================================================

@st.cache_data(
    show_spinner=False,
    max_entries=10,
)
def fetch_news_for_day(edition_date):
    """
    Fetch news once for a particular date.

    The date is part of the cache key.

    Therefore:

    September 1 -> one Tavily request
    September 2 -> new Tavily request

    The same day's result is reused from cache.
    """

    raw_news = hrs24_news()

    return parse_news(raw_news)


# ============================================================
# NEWS LOGIC
# ============================================================

def get_today_news():
    """
    Return today's news only when the time is 12 PM or later.

    BEFORE 12 PM:
        No API call.

    AFTER 12 PM:
        Call hrs24_news() once.
        Result is cached for the day.
    """

    now = get_current_ist()
    noon = get_noon_today()

    # --------------------------------------------------------
    # BEFORE 12 PM
    # --------------------------------------------------------

    if now < noon:

        return None

    # --------------------------------------------------------
    # 12 PM OR AFTER
    # --------------------------------------------------------

    today = now.date()

    return fetch_news_for_day(str(today))


# ============================================================
# CUSTOM CSS
# ============================================================

render_html(
    """
    <style>

        /* ====================================================
           FONTS
           ==================================================== */

        @import url(
            'https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@500;600;700;800&display=swap'
        );


        /* ====================================================
           PAGE
           ==================================================== */

        .researchmind-page {
            font-family: 'DM Sans', sans-serif;
            color: #0d0d24;
        }


        .researchmind-page * {
            box-sizing: border-box;
        }


        /* ====================================================
           BRAND
           ==================================================== */

        .brand-row {
            display: flex;
            align-items: center;
            justify-content: space-between;

            padding: 12px 0 22px;

            border-bottom: 1px solid #eeeeF4;
        }


        .brand {
            font-family: 'Manrope', sans-serif;

            font-size: 25px;

            font-weight: 800;

            letter-spacing: -1.5px;

            color: #0d0d24;
        }


        .brand-dot {
            color: #7367f0;
        }


        .brand-tag {
            padding: 10px 15px;

            border-radius: 12px;

            background: #f7f5ff;

            color: #7367f0;

            font-size: 12px;

            font-weight: 700;

            letter-spacing: 0.04em;
        }


        /* ====================================================
           HERO
           ==================================================== */

        .hero {
            padding: 85px 0 65px;
        }


        .hero-kicker {
            color: #7367f0;

            font-size: 12px;

            font-weight: 800;

            letter-spacing: 0.16em;

            text-transform: uppercase;

            margin-bottom: 18px;
        }


        .hero-title {
            margin: 0;

            max-width: 850px;

            font-family: 'Manrope', sans-serif;

            font-size: clamp(48px, 7vw, 82px);

            line-height: 0.98;

            font-weight: 800;

            letter-spacing: -5px;

            color: #0d0d24;
        }


        .hero-title-accent {
            color: #f2a9c7;
        }


        .hero-description {
            max-width: 650px;

            margin-top: 25px;

            color: #6e6c7c;

            font-size: 17px;

            line-height: 1.7;
        }


        /* ====================================================
           SECTION
           ==================================================== */

        .section {
            margin-top: 55px;
        }


        .section-kicker {
            color: #7367f0;

            font-size: 11px;

            font-weight: 800;

            letter-spacing: 0.16em;

            text-transform: uppercase;

            margin-bottom: 7px;
        }


        .section-title {
            font-family: 'Manrope', sans-serif;

            font-size: 32px;

            font-weight: 800;

            letter-spacing: -1.8px;

            color: #0d0d24;
        }


        .section-description {
            margin-top: 8px;

            color: #777587;

            font-size: 14px;

            line-height: 1.6;
        }


        /* ====================================================
           NEWS STATUS
           ==================================================== */

        .news-status {
            display: inline-flex;

            align-items: center;

            gap: 8px;

            margin-top: 20px;

            padding: 8px 13px;

            border: 1px solid #e9e7f1;

            border-radius: 999px;

            background: #faf9fd;

            color: #6f6c7d;

            font-size: 12px;

            font-weight: 600;
        }


        .news-dot {
            width: 7px;

            height: 7px;

            border-radius: 50%;

            background: #7367f0;
        }


        /* ====================================================
           NEWS CARD
           ==================================================== */

        .news-card {
            padding: 22px;

            margin-top: 12px;

            border: 1px solid #e8e6ef;

            border-radius: 18px;

            background: #ffffff;

            transition: all 0.2s ease;
        }


        .news-card:hover {
            border-color: #d7d3e7;

            box-shadow:
                0 12px 35px
                rgba(13, 13, 36, 0.06);
        }


        .news-category {
            margin-bottom: 8px;

            color: #7367f0;

            font-size: 10px;

            font-weight: 800;

            letter-spacing: 0.14em;

            text-transform: uppercase;
        }


        .news-title {
            font-family: 'Manrope', sans-serif;

            color: #0d0d24;

            font-size: 19px;

            font-weight: 800;

            line-height: 1.35;

            letter-spacing: -0.5px;
        }


        .news-source {
            margin-top: 8px;

            color: #858293;

            font-size: 12px;

            font-weight: 600;
        }


        .news-summary {
            margin-top: 16px;

            color: #5f5d6d;

            font-size: 14px;

            line-height: 1.7;
        }


        .news-link {
            display: inline-block;

            margin-top: 18px;

            color: #7367f0;

            font-size: 13px;

            font-weight: 700;

            text-decoration: none;
        }


        /* ====================================================
           NOON MESSAGE
           ==================================================== */

        .noon-card {
            margin-top: 25px;

            padding: 35px;

            border: 1px solid #e8e6ef;

            border-radius: 22px;

            background: #faf9fd;

            text-align: center;
        }


        .noon-icon {
            font-size: 30px;

            margin-bottom: 10px;
        }


        .noon-title {
            font-family: 'Manrope', sans-serif;

            font-size: 20px;

            font-weight: 800;

            color: #0d0d24;
        }


        .noon-description {
            max-width: 570px;

            margin: 10px auto 0;

            color: #777587;

            font-size: 14px;

            line-height: 1.7;
        }


        /* ====================================================
           RESEARCH RESULT
           ==================================================== */

        .result-header {
            margin-top: 45px;

            padding: 20px 0;

            border-top: 1px solid #eeeeF4;
        }


        .result-label {
            color: #7367f0;

            font-size: 11px;

            font-weight: 800;

            letter-spacing: 0.16em;

            text-transform: uppercase;
        }


        /* ====================================================
           PIPELINE
           ==================================================== */

        .pipeline-card {
            padding: 20px;

            margin-top: 10px;

            border: 1px solid #e8e6ef;

            border-radius: 18px;

            background: #ffffff;
        }


        .pipeline-number {
            color: #7367f0;

            font-size: 11px;

            font-weight: 800;

            letter-spacing: 0.12em;
        }


        .pipeline-name {
            margin-top: 5px;

            font-family: 'Manrope', sans-serif;

            font-size: 17px;

            font-weight: 800;

            color: #0d0d24;
        }


        .pipeline-description {
            margin-top: 5px;

            color: #777587;

            font-size: 13px;

            line-height: 1.5;
        }


        /* ====================================================
           FOOTER
           ==================================================== */

        .footer {
            margin-top: 70px;

            padding: 25px 0;

            border-top: 1px solid #eeeeF4;

            color: #9996a8;

            text-align: center;

            font-size: 12px;
        }


    </style>
    """
)


# ============================================================
# MAIN PAGE WRAPPER
# ============================================================

render_html(
    """
    <div class="researchmind-page">

        <div class="brand-row">

            <div class="brand">
                Research<span class="brand-dot">Mind</span>
            </div>

            <div class="brand-tag">
                AI-powered research intelligence
            </div>

        </div>


        <section class="hero">

            <div class="hero-kicker">
                Research intelligence
            </div>

            <h1 class="hero-title">

                Know what changed.<br>

                <span class="hero-title-accent">
                    Understand why it matters.
                </span>

            </h1>

            <div class="hero-description">

                ResearchMind combines live web information
                with specialized AI agents to discover,
                read, write, and critique research for you.

            </div>

        </section>

    </div>
    """
)


# ============================================================
# LATEST NEWS SECTION
# ============================================================

render_html(
    """
    <div class="section">

        <div class="section-kicker">
            Latest intelligence
        </div>

        <div class="section-title">
            What changed recently?
        </div>

        <div class="section-description">

            Fresh news from different categories,
            updated once every day at 12:00 PM IST.

        </div>

    </div>
    """
)


# ============================================================
# NEWS SECTION
#
# st.fragment checks every minute.
#
# This means:
#
# Before 12 PM:
#     No API call.
#
# At/after 12 PM:
#     Today's news is fetched.
#
# cache_data prevents repeated Tavily calls.
# ============================================================

@st.fragment(run_every="60s")
def display_daily_news():

    now = get_current_ist()
    noon = get_noon_today()

    # --------------------------------------------------------
    # BEFORE NOON
    # --------------------------------------------------------

    if now < noon:

        remaining = noon - now

        seconds = max(
            0,
            int(
                remaining.total_seconds()
            ),
        )

        hours = seconds // 3600

        minutes = (
            seconds % 3600
        ) // 60

        render_html(
            f"""
            <div class="noon-card">

                <div class="noon-icon">
                    ◷
                </div>

                <div class="noon-title">
                    Today's news edition isn't available yet.
                </div>

                <div class="noon-description">

                    ResearchMind refreshes its news intelligence
                    once daily at
                    <strong>12:00 PM IST</strong>.

                    <br><br>

                    No Tavily request is made before
                    the daily edition time.

                    <br><br>

                    Today's edition arrives in approximately

                    <strong>
                        {hours}h {minutes}m
                    </strong>.

                </div>

            </div>
            """
        )

        return


    # --------------------------------------------------------
    # AFTER NOON
    # --------------------------------------------------------

    try:

        news_items = get_today_news()

    except Exception as error:

        st.error(
            "Unable to load today's news. "
            f"Error: {error}"
        )

        return


    # --------------------------------------------------------
    # NO RESULTS
    # --------------------------------------------------------

    if not news_items:

        st.warning(
            "No news articles were returned by the news agent."
        )

        return


    # --------------------------------------------------------
    # STATUS
    # --------------------------------------------------------

    render_html(
        """
        <div class="news-status">

            <span class="news-dot"></span>

            Live Tavily intelligence ·
            Today's edition ·
            12:00 PM IST

        </div>
        """
    )


    # --------------------------------------------------------
    # NEWS ARTICLES
    # --------------------------------------------------------

    for index, article in enumerate(news_items):

        if not isinstance(article, dict):
            continue


        title = str(
            article.get(
                "title",
                "Untitled news",
            )
        )


        source = str(
            article.get(
                "source",
                "Unknown source",
            )
        )


        category = str(
            article.get(
                "category",
                "LATEST",
            )
        )


        summary = str(
            article.get(
                "summary",
                article.get(
                    "snippet",
                    article.get(
                        "content",
                        "No summary available.",
                    ),
                ),
            )
        )


        url = str(
            article.get(
                "url",
                "",
            )
        )


        # ----------------------------------------------------
        # HTML ESCAPING
        # ----------------------------------------------------

        safe_title = html.escape(title)

        safe_source = html.escape(source)

        safe_category = html.escape(category)

        safe_summary = html.escape(summary)


        # ----------------------------------------------------
        # EXPANDABLE NEWS CARD
        # ----------------------------------------------------

        with st.expander(
            f"{category.upper()}  ·  {title}",
            expanded=False,
        ):

            render_html(
                f"""
                <div class="news-card">

                    <div class="news-category">
                        {safe_category}
                    </div>

                    <div class="news-title">
                        {safe_title}
                    </div>

                    <div class="news-source">
                        {safe_source}
                    </div>

                    <div class="news-summary">
                        {safe_summary}
                    </div>

                </div>
                """
            )


            if (
                url.startswith("http://")
                or url.startswith("https://")
            ):

                safe_url = html.escape(
                    url,
                    quote=True,
                )

                render_html(
                    f"""
                    <a
                        class="news-link"
                        href="{safe_url}"
                        target="_blank"
                    >
                        Read original story →
                    </a>
                    """
                )


display_daily_news()


# ============================================================
# DEEP RESEARCH
# ============================================================

render_html(
    """
    <div class="section">

        <div class="section-kicker">
            Deep research
        </div>

        <div class="section-title">
            Research any topic.
        </div>

        <div class="section-description">

            Let specialized AI agents search, read,
            write, and critique a research report.

        </div>

    </div>
    """
)


# ============================================================
# TOPIC INPUT
# ============================================================

topic = st.text_input(
    "Research topic",
    placeholder="e.g. AI agents in software development",
    label_visibility="collapsed",
)


# ============================================================
# RUN RESEARCH
# ============================================================

run_research = st.button(
    "✦  Run Research Pipeline",
    use_container_width=True,
)


if run_research:

    if not topic.strip():

        st.warning(
            "Please enter a research topic first."
        )

    else:

        try:

            with st.spinner(
                "ResearchMind is researching..."
            ):

                result = run_research_pipeline(
                    topic.strip()
                )


            st.session_state["research_result"] = result


        except Exception as error:

            st.error(
                f"Research pipeline failed: {error}"
            )


# ============================================================
# DISPLAY RESEARCH RESULT
# ============================================================

if "research_result" in st.session_state:

    result = st.session_state["research_result"]


    render_html(
        """
        <div class="result-header">

            <div class="result-label">
                Research output
            </div>

        </div>
        """
    )


    # --------------------------------------------------------
    # SEARCH RESULTS
    # --------------------------------------------------------

    if result.get("search_results"):

        with st.expander(
            "🔎  View raw search results",
            expanded=False,
        ):

            st.write(
                result["search_results"]
            )


    # --------------------------------------------------------
    # SCRAPED CONTENT
    # --------------------------------------------------------

    if result.get("scraped_content"):

        with st.expander(
            "📄  View scraped source content",
            expanded=False,
        ):

            st.write(
                result["scraped_content"]
            )


    # --------------------------------------------------------
    # FINAL REPORT
    # --------------------------------------------------------

    if result.get("report"):

        render_html(
            """
            <div class="result-header">

                <div class="result-label">
                    Final research report
                </div>

            </div>
            """
        )


        st.markdown(
            result["report"]
        )


        st.download_button(
            "↓  Download research report",
            data=result["report"],
            file_name="research_report.md",
            mime="text/markdown",
        )


    # --------------------------------------------------------
    # CRITIC
    # --------------------------------------------------------

    if result.get("feedback"):

        render_html(
            """
            <div class="result-header">

                <div class="result-label">
                    Critic review
                </div>

            </div>
            """
        )


        st.markdown(
            result["feedback"]
        )


# ============================================================
# HOW IT WORKS
# ============================================================

render_html(
    """
    <div class="section">

        <div class="section-kicker">
            How it works
        </div>

        <div class="section-title">
            Four specialized stages.
        </div>

    </div>
    """
)


pipeline_steps = [
    (
        "01",
        "Search Agent",
        "Finds recent and relevant information from the web using Tavily.",
    ),
    (
        "02",
        "Reader Agent",
        "Selects relevant sources and extracts deeper webpage content.",
    ),
    (
        "03",
        "Writer Chain",
        "Turns gathered research into a structured research report.",
    ),
    (
        "04",
        "Critic Chain",
        "Reviews the report and identifies strengths and improvements.",
    ),
]


for number, name, description in pipeline_steps:

    render_html(
        f"""
        <div class="pipeline-card">

            <div class="pipeline-number">
                {number}
            </div>

            <div class="pipeline-name">
                {html.escape(name)}
            </div>

            <div class="pipeline-description">
                {html.escape(description)}
            </div>

        </div>
        """
    )


# ============================================================
# FOOTER
# ============================================================

render_html(
    """
    <div class="footer">

        ResearchMind · AI-powered multi-agent research

        <br>

        Built with Streamlit · LangChain · Mistral AI · Tavily

    </div>
    """
)