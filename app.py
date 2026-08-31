import streamlit as st
import time
from pipeline import run_research_pipeline

st.set_page_config(
    page_title="ResearchMind · AI Research Assistant",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Demo homepage news. Refresh cycles through different sets.
# These are intentionally demo stories and do not call an API.
DEMO_NEWS = [
    [
        {
            "category": "AI & TECHNOLOGY",
            "title": "AI agents are moving from chat to real-world workflows",
            "source": "ResearchMind Demo",
            "time": "2 hours ago",
            "summary": "AI systems are increasingly being designed to plan tasks, use tools, gather information, and complete multi-step workflows instead of only generating text.",
            "details": "This demo story represents the kind of development ResearchMind could surface in its 24-hour discovery feed. The interesting shift is from single-prompt assistants toward systems that can search, reason, use external tools, and coordinate multiple stages of work.",
        },
        {
            "category": "SCIENCE",
            "title": "New advances make scientific research more AI-assisted",
            "source": "ResearchMind Demo",
            "time": "4 hours ago",
            "summary": "Researchers are experimenting with AI systems that help discover patterns, summarize literature, and accelerate parts of scientific investigation.",
            "details": "AI-assisted science is becoming a broader workflow rather than a single tool. Systems can help researchers navigate large collections of papers, compare findings, identify promising directions, and prepare early research summaries.",
        },
        {
            "category": "BUSINESS",
            "title": "Companies rethink how knowledge workers use AI",
            "source": "ResearchMind Demo",
            "time": "6 hours ago",
            "summary": "Organizations are moving beyond generic chatbots and exploring AI workflows tailored to specific business tasks.",
            "details": "The demo story highlights a broader product trend: instead of asking employees to use a general chatbot for everything, companies are building AI into research, support, analysis, documentation, and operational workflows.",
        },
        {
            "category": "TECHNOLOGY",
            "title": "Smaller AI models are becoming more useful for everyday applications",
            "source": "ResearchMind Demo",
            "time": "8 hours ago",
            "summary": "Developers are increasingly evaluating smaller models for applications where speed, cost, and deployment flexibility matter.",
            "details": "Smaller models can be attractive when an application needs fast responses or lower inference costs. This creates more options for developers choosing between large general-purpose models and focused models for specific tasks.",
        },
        {
            "category": "STARTUPS",
            "title": "AI-native products focus on complete workflows, not features",
            "source": "ResearchMind Demo",
            "time": "10 hours ago",
            "summary": "A growing number of AI products are being designed around complete user journeys rather than adding AI as an isolated feature.",
            "details": "The demo reflects a product-design trend where AI is embedded across a workflow: collecting information, making decisions, producing an output, and helping the user take the next action.",
        },
        {
            "category": "FUTURE",
            "title": "The next generation of AI interfaces may feel less like chat",
            "source": "ResearchMind Demo",
            "time": "12 hours ago",
            "summary": "New AI products are exploring interfaces that combine search, cards, actions, documents, and autonomous workflows.",
            "details": "Rather than placing every interaction inside a chat window, designers are experimenting with interfaces where AI results appear as structured information and actions. ResearchMind follows this direction with a news discovery layer and a deeper research pipeline.",
        },
    ],
    [
        {
            "category": "AI & TECHNOLOGY",
            "title": "Multi-agent systems gain attention for complex research tasks",
            "source": "ResearchMind Demo",
            "time": "1 hour ago",
            "summary": "Developers are experimenting with specialized AI agents that divide complex tasks into research, analysis, writing, and review stages.",
            "details": "The demo story represents a key idea behind ResearchMind: specialized components can be easier to reason about than one large prompt handling every part of a research workflow.",
        },
        {
            "category": "SCIENCE",
            "title": "AI helps researchers navigate rapidly growing literature",
            "source": "ResearchMind Demo",
            "time": "3 hours ago",
            "summary": "As scientific literature grows, AI-assisted discovery tools are being explored to help researchers find relevant work faster.",
            "details": "Research discovery is especially suitable for AI because researchers often need to search across many documents before identifying the few sources worth reading deeply.",
        },
        {
            "category": "PRODUCT",
            "title": "AI interfaces are becoming more visual and task-oriented",
            "source": "ResearchMind Demo",
            "time": "5 hours ago",
            "summary": "Modern AI applications increasingly combine structured cards, actions, summaries, and conversational interactions.",
            "details": "This demo story mirrors the design direction of ResearchMind: give users useful information immediately, then provide a clear path from discovery to deeper investigation.",
        },
        {
            "category": "DEVELOPMENT",
            "title": "Developers adopt tool-using AI for automated workflows",
            "source": "ResearchMind Demo",
            "time": "7 hours ago",
            "summary": "Tool calling allows AI systems to interact with search, databases, APIs, and other external services.",
            "details": "A tool-using model can decide when external information is needed and then incorporate the returned information into its next step. ResearchMind uses this pattern for web research and webpage extraction.",
        },
        {
            "category": "STARTUPS",
            "title": "AI startups compete on workflow reliability and usefulness",
            "source": "ResearchMind Demo",
            "time": "9 hours ago",
            "summary": "As AI capabilities become more accessible, product differentiation increasingly depends on solving specific user problems well.",
            "details": "The demo story emphasizes an important product lesson: the value of an AI application comes from the workflow it enables, not simply from having an LLM behind the interface.",
        },
        {
            "category": "FUTURE",
            "title": "Human-in-the-loop AI remains important for high-value decisions",
            "source": "ResearchMind Demo",
            "time": "11 hours ago",
            "summary": "AI systems can accelerate information gathering while humans remain responsible for judging important conclusions.",
            "details": "ResearchMind follows this principle by showing the generated report and critic feedback rather than treating an AI response as unquestionable truth.",
        },
    ],
]

if "news_set" not in st.session_state:
    st.session_state.news_set = 0
if "results" not in st.session_state:
    st.session_state.results = {}
if "running" not in st.session_state:
    st.session_state.running = False
if "done" not in st.session_state:
    st.session_state.done = False

st.markdown(
    '''
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@500;600;700;800&display=swap');

    :root {
        --ink:#0d0d24; --muted:#77758a; --soft:#f7f7fb;
        --line:#e9e8f0; --purple:#7367f0; --pink:#f5a9c5;
        --pink-soft:#fff0f6; --white:#fff;
    }
    html,body,[class*="css"] { font-family:'DM Sans',sans-serif; color:var(--ink); }
    .stApp { background:#fff; }
    #MainMenu,footer,header { visibility:hidden; }
    .block-container { max-width:1240px; padding:1.2rem 2.5rem 4rem; }

    .nav { display:flex; align-items:center; gap:3rem; min-height:62px;
           border-bottom:1px solid #f1f0f5; margin-bottom:2.5rem; }
    .brand { font-family:'Manrope',sans-serif; font-size:1.45rem; font-weight:800;
             letter-spacing:-.07em; color:var(--ink); margin-right:1.5rem; }
    .nav-item { font-size:.92rem; font-weight:600; color:var(--ink); }
    .nav-item span { color:#7d7a8b; font-size:.75rem; margin-left:.25rem; }
    .nav-note { margin-left:auto; color:#77758a; font-size:.82rem; }

    .hero { padding:2.2rem 0 1.2rem; }
    .eyebrow { display:inline-flex; padding:.5rem .85rem; border-radius:999px;
               background:var(--pink-soft); color:#e66c9b; font-size:.73rem;
               font-weight:700; letter-spacing:.08em; text-transform:uppercase; margin-bottom:1.25rem; }
    .hero h1 { font-family:'Manrope',sans-serif; font-size:clamp(3rem,6vw,5.7rem);
               line-height:.98; letter-spacing:-.075em; font-weight:800; max-width:930px;
               margin:0; color:var(--ink); }
    .hero h1 .accent { color:var(--pink); }
    .hero p { color:var(--muted); max-width:650px; font-size:1.05rem; line-height:1.7; margin-top:1.4rem; }

    .section-top { display:flex; align-items:flex-end; justify-content:space-between; margin:3rem 0 1.2rem; }
    .section-kicker { color:var(--purple); font-size:.72rem; font-weight:800;
                      letter-spacing:.12em; text-transform:uppercase; margin-bottom:.35rem; }
    .section-title { font-family:'Manrope',sans-serif; font-size:2rem; line-height:1.1;
                     letter-spacing:-.05em; font-weight:800; color:var(--ink); }
    .section-description { color:var(--muted); font-size:.9rem; margin-top:.4rem; }

    .stButton > button { border-radius:999px!important; border:1px solid var(--line)!important;
                         background:#fff!important; color:var(--ink)!important;
                         font-family:'DM Sans',sans-serif!important; font-weight:700!important;
                         padding:.65rem 1.2rem!important; min-height:42px!important; }
    .stButton > button:hover { border-color:#c8c4dc!important; background:#faf9fd!important; transform:translateY(-1px); }

    div[data-testid="stExpander"] { border:1px solid var(--line)!important; border-radius:20px!important;
        background:#fff!important; box-shadow:0 8px 30px rgba(21,19,45,.035)!important;
        margin-bottom:.85rem!important; overflow:hidden!important; }
    div[data-testid="stExpander"] summary { padding:.1rem!important; }
    div[data-testid="stExpander"] summary p { font-family:'Manrope',sans-serif!important;
        font-weight:800!important; color:var(--ink)!important; font-size:.92rem!important; }

    .news-category { display:inline-block; color:#e66c9b; background:var(--pink-soft);
                     border-radius:999px; padding:.3rem .55rem; font-size:.63rem;
                     font-weight:800; letter-spacing:.07em; }
    .news-title { font-family:'Manrope',sans-serif; color:var(--ink); font-size:1.08rem;
                  line-height:1.3; letter-spacing:-.025em; font-weight:800; margin:.8rem 0 .55rem; }
    .news-summary { color:var(--muted); font-size:.82rem; line-height:1.55; margin-bottom:1rem; }
    .news-meta { color:#9996a5; font-size:.7rem; font-weight:600; }

    .research-box { background:var(--soft); border-radius:28px; padding:2rem;
                    border:1px solid #efedf5; margin-top:2rem; }
    .research-heading { font-family:'Manrope',sans-serif; font-size:2.25rem; font-weight:800;
                        letter-spacing:-.055em; color:var(--ink); margin-bottom:.35rem; }
    .research-sub { color:var(--muted); font-size:.9rem; margin-bottom:1.4rem; }
    .stTextInput > div > div > input { border:1px solid #dfdde8!important; border-radius:14px!important;
        background:#fff!important; color:var(--ink)!important; font-family:'DM Sans',sans-serif!important;
        font-size:.96rem!important; padding:.85rem 1rem!important; height:52px!important; box-shadow:none!important; }
    .stTextInput > div > div > input:focus { border-color:#b9b3d8!important;
        box-shadow:0 0 0 3px rgba(115,103,240,.08)!important; }
    .stTextInput > label { color:var(--ink)!important; font-weight:700!important; font-size:.8rem!important; }
    .primary-button > div > button { background:var(--ink)!important; color:#fff!important;
        border:1px solid var(--ink)!important; min-height:52px!important; border-radius:14px!important; font-size:.92rem!important; }
    .primary-button > div > button:hover { background:#22203d!important; border-color:#22203d!important;
        box-shadow:0 8px 24px rgba(13,13,36,.15)!important; }
    .chip { display:inline-block; padding:.42rem .72rem; border-radius:999px; border:1px solid #e4e2ec;
            background:#fff; color:#77758a; font-size:.72rem; margin:.25rem .25rem 0 0; }

    .pipeline-title { font-family:'Manrope',sans-serif; font-size:1.7rem; font-weight:800;
                      letter-spacing:-.045em; color:var(--ink); margin:.4rem 0 1rem; }
    .pipeline-card { border:1px solid var(--line); background:#fff; border-radius:17px;
                     padding:1rem 1.1rem; margin-bottom:.75rem; }
    .pipeline-number { color:var(--purple); font-size:.68rem; font-weight:800; letter-spacing:.08em; }
    .pipeline-name { color:var(--ink); font-family:'Manrope',sans-serif; font-weight:800;
                     font-size:.93rem; margin-left:.5rem; }
    .pipeline-desc { color:var(--muted); font-size:.74rem; margin-top:.45rem; line-height:1.45; }
    .waiting,.done,.running { float:right; font-size:.62rem; letter-spacing:.08em; font-weight:700; }
    .waiting { color:#aaa7b4; } .done { color:#45a97a; } .running { color:#e66c9b; }

    .result-box { border:1px solid var(--line); border-radius:22px; padding:1.6rem;
                  background:#fff; margin:1rem 0; box-shadow:0 8px 30px rgba(21,19,45,.035); }
    .result-label,.feedback-label { font-size:.68rem; font-weight:800; letter-spacing:.11em;
                                    text-transform:uppercase; margin-bottom:.8rem; }
    .result-label { color:var(--purple); }
    .feedback-box { border:1px solid #eadff0; background:#fff9fc; border-radius:22px;
                    padding:1.6rem; margin:1rem 0; }
    .feedback-label { color:#e66c9b; }
    .stDownloadButton > button { border-radius:999px!important; font-weight:700!important;
                                 border:1px solid var(--line)!important; background:#fff!important; color:var(--ink)!important; }
    .divider { height:1px; background:#efedf4; margin:3rem 0; }
    .demo-note { color:#a09dab; font-size:.7rem; margin-top:.6rem; }
    .footer { text-align:center; color:#aaa7b4; font-size:.72rem; padding:3rem 0 1rem; }

    @media (max-width:800px) {
        .block-container { padding:1rem 1.1rem 3rem; }
        .nav { gap:1rem; overflow-x:auto; }
        .nav-item,.nav-note { display:none; }
        .hero h1 { font-size:3.3rem; }
    }
    </style>
    ''',
    unsafe_allow_html=True,
)

# Navigation
st.markdown(
    '''
    <div class="nav">
        <div class="brand">ResearchMind</div>
        <div class="nav-item">Discover <span>⌄</span></div>
        <div class="nav-item">Research <span>⌄</span></div>
        <div class="nav-item">AI Agents <span>⌄</span></div>
        <div class="nav-item">About <span>⌄</span></div>
        <div class="nav-note">AI-powered research workspace</div>
    </div>
    ''',
    unsafe_allow_html=True,
)

# Hero
st.markdown(
    '''
    <section class="hero">
        <div class="eyebrow">Multi-agent AI research</div>
        <h1>Know what changed.<br><span class="accent">Understand why it matters.</span></h1>
        <p>Discover the latest stories, then turn any topic into a structured research report using specialized AI agents.</p>
    </section>
    ''',
    unsafe_allow_html=True,
)

# Latest 24 hours
st.markdown(
    '''
    <div class="section-top">
        <div>
            <div class="section-kicker">Latest 24 hours</div>
            <div class="section-title">What changed recently?</div>
            <div class="section-description">Demo stories for the homepage — click any card to expand it.</div>
        </div>
    </div>
    ''',
    unsafe_allow_html=True,
)

refresh_col, note_col = st.columns([1.5, 5])
with refresh_col:
    if st.button("↻  Refresh 24h news", use_container_width=True):
        st.session_state.news_set = (st.session_state.news_set + 1) % len(DEMO_NEWS)
        st.rerun()
with note_col:
    st.markdown(
        '<div class="demo-note">Demo mode · refresh cycles through a different set of stories.</div>',
        unsafe_allow_html=True,
    )

news_items = DEMO_NEWS[st.session_state.news_set]
for row_start in range(0, len(news_items), 3):
    cols = st.columns(3, gap="medium")
    for col, item in zip(cols, news_items[row_start:row_start + 3]):
        with col:
            with st.expander(item["title"], expanded=False):
                st.markdown(
                    f'''
                    <span class="news-category">{item["category"]}</span>
                    <div class="news-title">{item["title"]}</div>
                    <div class="news-summary">{item["summary"]}</div>
                    <div class="news-meta">{item["source"]} &nbsp;·&nbsp; {item["time"]}</div>
                    <br>
                    <div style="color:#77758a;font-size:.82rem;line-height:1.65;">{item["details"]}</div>
                    ''',
                    unsafe_allow_html=True,
                )

# Research area
st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

research_left, research_right = st.columns([5.4, 3.6], gap="large")

with research_left:
    st.markdown(
        '''
        <div class="research-box">
            <div class="section-kicker">Deep research</div>
            <div class="research-heading">Research a topic.</div>
            <div class="research-sub">Search the web, read a relevant source, generate a report, and have another AI chain critique it.</div>
        ''',
        unsafe_allow_html=True,
    )

    topic = st.text_input(
        "Research topic",
        placeholder="e.g. Quantum computing breakthroughs in 2026",
        key="topic_input",
    )

    st.markdown('<div class="primary-button">', unsafe_allow_html=True)
    run_btn = st.button("✦  Run Research Pipeline", use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown(
        '''
        <div style="margin-top:1rem;">
            <span style="color:#9996a5;font-size:.72rem;font-weight:700;">TRY</span>
            <span class="chip">AI agents</span>
            <span class="chip">CRISPR gene editing</span>
            <span class="chip">Fusion energy</span>
        </div></div>
        ''',
        unsafe_allow_html=True,
    )

with research_right:
    st.markdown('<div class="pipeline-title">Pipeline</div>', unsafe_allow_html=True)

    steps = [
        ("01", "Search Agent", "Gathers recent web information"),
        ("02", "Reader Agent", "Scrapes & extracts deep content"),
        ("03", "Writer Chain", "Drafts the full research report"),
        ("04", "Critic Chain", "Reviews & scores the report"),
    ]

    for key, (num, name, desc) in zip(
        ["search", "reader", "writer", "critic"], steps
    ):
        if key in st.session_state.results:
            status = '<span class="done">✓ DONE</span>'
        elif st.session_state.running:
            status = '<span class="running">● RUNNING</span>'
        else:
            status = '<span class="waiting">WAITING</span>'

        st.markdown(
            f'''
            <div class="pipeline-card">
                {status}
                <span class="pipeline-number">{num}</span>
                <span class="pipeline-name">{name}</span>
                <div class="pipeline-desc">{desc}</div>
            </div>
            ''',
            unsafe_allow_html=True,
        )

# Start pipeline
if run_btn:
    if not topic.strip():
        st.warning("Please enter a research topic first.")
    else:
        st.session_state.results = {}
        st.session_state.running = True
        st.session_state.done = False
        st.rerun()

# Run pipeline
if st.session_state.running and not st.session_state.done:
    topic_val = st.session_state.topic_input

    with st.spinner("ResearchMind is working through the pipeline…"):
        try:
            pipeline_result = run_research_pipeline(topic_val)
        except Exception as e:
            st.session_state.running = False
            st.error(f"Research pipeline failed: {e}")
            st.stop()

    st.session_state.results = {
        "search": pipeline_result.get("search_results", ""),
        "reader": pipeline_result.get("scraped_content", ""),
        "writer": pipeline_result.get("report", ""),
        "critic": pipeline_result.get("feedback", ""),
    }
    st.session_state.running = False
    st.session_state.done = True
    st.rerun()

# Results
r = st.session_state.results
if r:
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-kicker">Research output</div><div class="section-title">Your research report</div>',
        unsafe_allow_html=True,
    )

    if r.get("search"):
        with st.expander("🔎 View raw search results"):
            st.markdown(r["search"])

    if r.get("reader"):
        with st.expander("📄 View scraped source content"):
            st.markdown(r["reader"])

    if r.get("writer"):
        st.markdown(
            '<div class="result-box"><div class="result-label">Final research report</div>',
            unsafe_allow_html=True,
        )
        st.markdown(r["writer"])
        st.markdown("</div>", unsafe_allow_html=True)

        st.download_button(
            "↓  Download report (.md)",
            data=r["writer"],
            file_name=f"research_report_{int(time.time())}.md",
            mime="text/markdown",
        )

    if r.get("critic"):
        st.markdown(
            '<div class="feedback-box"><div class="feedback-label">Critic feedback</div>',
            unsafe_allow_html=True,
        )
        st.markdown(r["critic"])
        st.markdown("</div>", unsafe_allow_html=True)

st.markdown(
    '<div class="footer">ResearchMind · Search → Read → Write → Critique</div>',
    unsafe_allow_html=True,
)
