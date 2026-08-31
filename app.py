import streamlit as st
import time
from agents import build_reader_agent, build_search_agent, writer_chain, critic_chain

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="ResearchMind · AI Research Agent",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&family=Space+Grotesk:wght@500;600;700&display=swap');

/* ── Reset & base ── */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    color: #111827;
}

.stApp {
    background: #ffffff;
}

.block-container {
    padding: 0 2.5rem 4rem;
    max-width: 1400px;
}

/* ── Hide Streamlit chrome ── */
#MainMenu, footer {
    visibility: hidden;
}

header {
    background: #ffffff !important;
}

/* ── Top navigation ── */
.topbar {
    height: 72px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    border-bottom: 1px solid #e8ebf0;
    margin: 0 -2.5rem 0;
    padding: 0 2.5rem;
}

.brand {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1.05rem;
    font-weight: 700;
    letter-spacing: -0.03em;
    color: #111827;
}

.brand-accent {
    color: #4f46e5;
}

.ai-pill {
    display: inline-flex;
    align-items: center;
    padding: 0.42rem 0.8rem;
    border-radius: 999px;
    background: #eef0ff;
    color: #5961d9;
    font-size: 0.68rem;
    font-weight: 700;
    letter-spacing: 0.01em;
}

/* ── Hero ── */
.hero {
    padding: 3.2rem 0 2.4rem;
    border-bottom: 1px solid #e8ebf0;
}

.hero h1 {
    font-family: 'Space Grotesk', sans-serif;
    font-size: clamp(3.2rem, 7vw, 6.4rem);
    line-height: 0.96;
    font-weight: 700;
    letter-spacing: -0.065em;
    color: #0d1528;
    margin: 0;
    max-width: 900px;
}

.hero h1 .accent {
    color: #ed69ad;
}

.hero-sub {
    margin: 1.25rem 0 0;
    max-width: 650px;
    color: #667085;
    font-size: 1rem;
    line-height: 1.65;
}

/* ── Section labels ── */
.section-heading {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1.1rem;
    font-weight: 700;
    color: #101828;
    letter-spacing: -0.025em;
    margin: 0 0 1rem;
}

.section-kicker {
    font-size: 0.72rem;
    font-weight: 800;
    letter-spacing: 0.13em;
    text-transform: uppercase;
    color: #667085;
    margin-bottom: 0.5rem;
}

/* ── Main input area ── */
.workspace {
    padding-top: 2.4rem;
}

.input-card {
    background: #f7f8fb;
    border: 1px solid #e6e8ee;
    border-radius: 18px;
    padding: 1.5rem;
    margin-bottom: 1rem;
}

.input-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1.45rem;
    font-weight: 700;
    letter-spacing: -0.035em;
    color: #111827;
    margin-bottom: 0.25rem;
}

.input-help {
    color: #667085;
    font-size: 0.86rem;
    line-height: 1.5;
    margin-bottom: 1rem;
}

/* Streamlit text input */
.stTextInput > div > div > input {
    background: #ffffff !important;
    border: 1px solid #d9dde6 !important;
    border-radius: 11px !important;
    color: #101828 !important;
    -webkit-text-fill-color: #101828 !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.98rem !important;
    font-weight: 500 !important;
    padding: 0.78rem 0.95rem !important;
    box-shadow: 0 1px 2px rgba(16, 24, 40, 0.03) !important;
}

.stTextInput > div > div > input::placeholder {
    color: #98a2b3 !important;
    -webkit-text-fill-color: #98a2b3 !important;
}

.stTextInput > div > div > input:focus {
    border-color: #6366f1 !important;
    box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.12) !important;
}

.stTextInput > label {
    color: #344054 !important;
    font-size: 0.76rem !important;
    font-weight: 700 !important;
}

/* Run button */
.stButton > button {
    background: #111827 !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 11px !important;
    min-height: 44px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.9rem !important;
    font-weight: 700 !important;
    box-shadow: none !important;
    transition: transform 0.15s ease, background 0.15s ease !important;
}

.stButton > button:hover {
    background: #273142 !important;
    transform: translateY(-1px) !important;
}

.stButton > button:active {
    transform: translateY(0) !important;
}

/* ── Example topics ── */
.example-row {
    display: flex;
    gap: 0.5rem;
    flex-wrap: wrap;
    align-items: center;
}

.example-label {
    color: #98a2b3;
    font-size: 0.7rem;
    font-weight: 700;
    letter-spacing: 0.08em;
}

.example-chip {
    display: inline-flex;
    align-items: center;
    background: #ffffff;
    border: 1px solid #e3e6ec;
    color: #667085;
    border-radius: 999px;
    padding: 0.38rem 0.7rem;
    font-size: 0.73rem;
    font-weight: 600;
}

/* ── Pipeline ── */
.pipeline-wrap {
    background: #ffffff;
    border: 1px solid #e6e8ee;
    border-radius: 18px;
    padding: 1.35rem;
}

.step-card {
    background: #ffffff;
    border: 1px solid #e6e8ee;
    border-radius: 13px;
    padding: 1rem 1.05rem;
    margin-bottom: 0.65rem;
    position: relative;
    overflow: hidden;
    transition: border-color 0.2s ease, background 0.2s ease;
}

.step-card.active {
    border-color: #a5b4fc;
    background: #f7f7ff;
}

.step-card.done {
    border-color: #b8e0ca;
    background: #f7fcf9;
}

.step-card::before {
    content: '';
    position: absolute;
    left: 0;
    top: 0;
    bottom: 0;
    width: 3px;
    background: #e6e8ee;
}

.step-card.active::before {
    background: #6366f1;
}

.step-card.done::before {
    background: #22a06b;
}

.step-header {
    display: flex;
    align-items: center;
    gap: 0.7rem;
}

.step-num {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 0.7rem;
    font-weight: 700;
    color: #667085;
}

.step-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 0.9rem;
    font-weight: 700;
    color: #101828;
}

.step-status {
    margin-left: auto;
    font-size: 0.64rem;
    font-weight: 800;
    letter-spacing: 0.07em;
}

.status-waiting { color: #98a2b3; }
.status-running { color: #5b61d6; }
.status-done { color: #16855a; }

/* ── Result panels ── */
.results-divider {
    height: 1px;
    background: #e8ebf0;
    margin: 2.7rem 0 2rem;
}

.result-panel,
.report-panel,
.feedback-panel,
.st-key-report_panel,
.st-key-feedback_panel {
    background: #ffffff;
    border: 1px solid #e2e6ed;
    border-radius: 16px;
    padding: 1.5rem;
    margin-top: 0.8rem;
    margin-bottom: 1.1rem;
    box-shadow: 0 2px 10px rgba(16, 24, 40, 0.025);
}

.result-panel-title,
.panel-label {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 0.78rem;
    font-weight: 700;
    letter-spacing: 0.03em;
    color: #475467;
    margin-bottom: 1rem;
    padding-bottom: 0.7rem;
    border-bottom: 1px solid #edf0f4;
}

.panel-label.orange {
    color: #c94f91;
}

.panel-label.green {
    color: #16855a;
}

/*
   IMPORTANT: generated content is deliberately dark and uses a strong,
   block-style sans font so it remains readable on the white UI.

   NOTE: the selectors below are intentionally duplicated for both the
   legacy ".report-panel/.feedback-panel" wrapper divs AND the
   ".st-key-report_panel/.st-key-feedback_panel" classes that
   st.container(key=...) attaches directly to the real DOM wrapper.
   Relying on a single selector caused text to silently fall back to
   Streamlit's default (faded) markdown color on some deployments,
   because the exact DOM nesting of consecutive st.markdown() calls
   can differ slightly between Streamlit versions.
*/
.result-content,
.report-panel,
.feedback-panel,
.st-key-report_panel,
.st-key-feedback_panel {
    color: #172033 !important;
    font-family: 'DM Sans', sans-serif !important;
}

.result-content {
    font-size: 0.92rem;
    font-weight: 600;
    line-height: 1.75;
    white-space: pre-wrap;
    overflow-wrap: anywhere;
}

/* Native markdown rendered by Streamlit */
.report-panel > div:not(.panel-label),
.feedback-panel > div:not(.panel-label),
.st-key-report_panel [data-testid="stMarkdownContainer"],
.st-key-feedback_panel [data-testid="stMarkdownContainer"] {
    color: #172033 !important;
    font-family: 'DM Sans', sans-serif !important;
}

.report-panel h1,
.report-panel h2,
.report-panel h3,
.feedback-panel h1,
.feedback-panel h2,
.feedback-panel h3,
.st-key-report_panel [data-testid="stMarkdownContainer"] h1,
.st-key-report_panel [data-testid="stMarkdownContainer"] h2,
.st-key-report_panel [data-testid="stMarkdownContainer"] h3,
.st-key-feedback_panel [data-testid="stMarkdownContainer"] h1,
.st-key-feedback_panel [data-testid="stMarkdownContainer"] h2,
.st-key-feedback_panel [data-testid="stMarkdownContainer"] h3 {
    font-family: 'Space Grotesk', sans-serif !important;
    color: #0d1528 !important;
    font-weight: 700 !important;
    letter-spacing: -0.035em;
}

.report-panel p,
.report-panel li,
.report-panel blockquote,
.feedback-panel p,
.feedback-panel li,
.feedback-panel blockquote,
.st-key-report_panel [data-testid="stMarkdownContainer"] p,
.st-key-report_panel [data-testid="stMarkdownContainer"] li,
.st-key-report_panel [data-testid="stMarkdownContainer"] blockquote,
.st-key-feedback_panel [data-testid="stMarkdownContainer"] p,
.st-key-feedback_panel [data-testid="stMarkdownContainer"] li,
.st-key-feedback_panel [data-testid="stMarkdownContainer"] blockquote {
    color: #172033 !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 600 !important;
    line-height: 1.75 !important;
}

.report-panel strong,
.feedback-panel strong,
.st-key-report_panel [data-testid="stMarkdownContainer"] strong,
.st-key-feedback_panel [data-testid="stMarkdownContainer"] strong {
    color: #0d1528 !important;
    font-weight: 800 !important;
}

.report-panel code,
.feedback-panel code,
.st-key-report_panel [data-testid="stMarkdownContainer"] code,
.st-key-feedback_panel [data-testid="stMarkdownContainer"] code {
    color: #26324a !important;
    background: #f2f4f7 !important;
}

/* Expander */
details summary {
    color: #475467 !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.8rem !important;
    font-weight: 700 !important;
}

details summary:hover {
    color: #4f46e5 !important;
}

/* Download button */
.stDownloadButton > button {
    background: #ffffff !important;
    color: #344054 !important;
    border: 1px solid #d9dde6 !important;
    border-radius: 10px !important;
    font-weight: 700 !important;
}

.stDownloadButton > button:hover {
    border-color: #98a2b3 !important;
    color: #111827 !important;
}

/* Alerts / spinner */
.stSpinner > div {
    color: #4f46e5 !important;
}

[data-testid="stAlert"] {
    border-radius: 11px;
}

/* Footer */
.notice {
    color: #98a2b3;
    text-align: center;
    margin-top: 3rem;
    font-size: 0.7rem;
    font-weight: 600;
    letter-spacing: 0.02em;
}
</style>
""", unsafe_allow_html=True)


# ── Helper: render a step card ────────────────────────────────────────────────
def step_card(num: str, title: str, state: str, desc: str = ""):
    status_map = {
        "waiting": ("WAITING", "status-waiting"),
        "running": ("● RUNNING", "status-running"),
        "done":    ("✓ DONE",   "status-done"),
    }
    label, cls = status_map.get(state, ("", ""))
    card_cls = {"running": "active", "done": "done"}.get(state, "")
    st.markdown(f"""
    <div class="step-card {card_cls}">
        <div class="step-header">
            <span class="step-num">{num}</span>
            <span class="step-title">{title}</span>
            <span class="step-status {cls}">{label}</span>
        </div>
        {"<div style='font-size:0.82rem;color:#706860;margin-top:0.3rem;'>"+desc+"</div>" if desc else ""}
    </div>
    """, unsafe_allow_html=True)


# ── Session state init ────────────────────────────────────────────────────────
for key in ("results", "running", "done"):
    if key not in st.session_state:
        st.session_state[key] = {} if key == "results" else False


# ── Header / Hero ─────────────────────────────────────────────────────────────
st.markdown("""

<div class="hero">
    <h1>
        Know what changed.<br>
        <span class="accent">Understand why it matters.</span>
    </h1>
    <p class="hero-sub">
        Four specialized AI agents search, read, write, and critique
        to turn a topic into a clear, research-backed report.
    </p>
</div>
""", unsafe_allow_html=True)


# ── Layout: input left, pipeline right ───────────────────────────────────────
col_input, col_spacer, col_pipeline = st.columns([5.2, 0.5, 4])

with col_input:
    st.markdown("""
    <div class="workspace">
        <div class="section-kicker">Research any topic</div>
        <div class="input-card">
            <div class="input-title">What do you want to understand?</div>
            <div class="input-help">
                Enter a topic and let the research pipeline gather,
                analyze, write, and review the information for you.
            </div>
    """, unsafe_allow_html=True)

    topic = st.text_input(
        "Research Topic",
        placeholder="e.g. How AI agents are changing software development",
        key="topic_input",
        label_visibility="visible",
    )
    run_btn = st.button("Run research →", use_container_width=True)
    st.markdown('</div></div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="example-row">
        <span class="example-label">TRY</span>
    """, unsafe_allow_html=True)

    examples = ["LLM agents 2025", "CRISPR gene editing", "Fusion energy progress"]
    for ex in examples:
        st.markdown(f'<span class="example-chip">{ex}</span>', unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)


with col_pipeline:
    st.markdown('<div class="workspace">', unsafe_allow_html=True)
    st.markdown('<div class="section-kicker">How it works</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-heading">Four specialized stages</div>', unsafe_allow_html=True)
    st.markdown('<div class="pipeline-wrap">', unsafe_allow_html=True)

    r = st.session_state.results
    done = st.session_state.done

    def s(step):
        if not r:
            return "waiting"
        steps = ["search", "reader", "writer", "critic"]
        idx = steps.index(step)
        completed = list(r.keys())
        if step in r:
            return "done"
        if st.session_state.running:
            for i, k in enumerate(steps):
                if k not in r:
                    return "running" if k == step else "waiting"
        return "waiting"

    step_card("01", "Search Agent",  s("search"), "Gathers recent web information")
    step_card("02", "Reader Agent",  s("reader"), "Scrapes & extracts deep content")
    step_card("03", "Writer Chain",  s("writer"), "Drafts the full research report")
    step_card("04", "Critic Chain",  s("critic"), "Reviews & scores the report")

    st.markdown('</div></div>', unsafe_allow_html=True)


# ── Run pipeline ──────────────────────────────────────────────────────────────
if run_btn:
    if not topic.strip():
        st.warning("Please enter a research topic first.")
    else:
        st.session_state.results = {}
        st.session_state.running = True
        st.session_state.done = False
        st.rerun()

if st.session_state.running and not st.session_state.done:
    results = {}
    topic_val = st.session_state.topic_input

    # ── Step 1: Search ──
    with st.spinner("  Search Agent is working…"):
        search_agent = build_search_agent()
        sr = search_agent.invoke({
            "messages": [("user", f"Find recent, reliable and detailed information about: {topic_val}")]
        })
        results["search"] = sr["messages"][-1].content
        st.session_state.results = dict(results)
    st.rerun() if False else None   # keep inline for now

    # ── Step 2: Reader ──
    with st.spinner("  Reader Agent is scraping top resources…"):
        reader_agent = build_reader_agent()
        rr = reader_agent.invoke({
            "messages": [("user",
                f"Based on the following search results about '{topic_val}', "
                f"pick the most relevant URL and scrape it for deeper content.\n\n"
                f"Search Results:\n{results['search'][:800]}"
            )]
        })
        results["reader"] = rr["messages"][-1].content
        st.session_state.results = dict(results)

    # ── Step 3: Writer ──
    with st.spinner("  Writer is drafting the report…"):
        research_combined = (
            f"SEARCH RESULTS:\n{results['search']}\n\n"
            f"DETAILED SCRAPED CONTENT:\n{results['reader']}"
        )
        results["writer"] = writer_chain.invoke({
            "topic": topic_val,
            "research": research_combined
        })
        st.session_state.results = dict(results)

    # ── Step 4: Critic ──
    with st.spinner("  Critic is reviewing the report…"):
        results["critic"] = critic_chain.invoke({
            "report": results["writer"]
        })
        st.session_state.results = dict(results)

    st.session_state.running = False
    st.session_state.done = True
    st.rerun()


# ── Results display ───────────────────────────────────────────────────────────
r = st.session_state.results

if r:
    st.markdown('<div class="results-divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-heading">Results</div>', unsafe_allow_html=True)

    # Final report
    if "writer" in r:
        with st.container(key="report_panel"):
            st.markdown('<div class="panel-label orange">Final Research Report</div>', unsafe_allow_html=True)
            st.markdown(r["writer"])   # render markdown natively

        # Download
        st.download_button(
            label="⬇  Download Report (.md)",
            data=r["writer"],
            file_name=f"research_report_{int(time.time())}.md",
            mime="text/markdown",
        )

    # Critic feedback
    if "critic" in r:
        with st.container(key="feedback_panel"):
            st.markdown('<div class="panel-label green">Critic Feedback</div>', unsafe_allow_html=True)
            st.markdown(r["critic"])


# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="notice">
    ResearchMind · Powered by LangChain multi-agent pipeline · Built with Streamlit
</div>
""", unsafe_allow_html=True)