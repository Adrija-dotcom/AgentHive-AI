import os

import streamlit as st
from dotenv import load_dotenv

from agents.orchestrator import run_agenthive
from agents.researcher import number_sources
from services.gemini import configure_gemini


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="AgentHive AI",
    page_icon="🤖",
    layout="wide"
)


# =========================================================
# CONFIGURATION
# =========================================================

load_dotenv()

try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
except Exception:
    API_KEY = os.getenv("GEMINI_API_KEY")


MODEL_NAME = "gemini-3.7-flash"

model = configure_gemini(
    API_KEY,
    MODEL_NAME
)


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.header("⚙️ AgentHive Configuration")

    execution_mode = st.radio(
        "Execution Mode",
        [
            "Demo Mode",
            "Gemini AI"
        ],
        index=0
    )

    st.markdown("---")

    st.markdown("### 🧠 Agent Pipeline")

    st.write("🔎 Research Agent")
    st.write("📚 Evidence Aggregator")
    st.write("🧠 Decision Intelligence")
    st.write("🛡️ Risk Auditor")
    st.write("📋 Strategic Planner")

    st.markdown("---")

    if execution_mode == "Demo Mode":

        st.info(
            "Demo Mode performs live web research "
            "without using Gemini API requests."
        )

    else:

        if API_KEY:

            st.success(
                "Gemini API configured."
            )

        else:

            st.warning(
                "Gemini API unavailable. "
                "AgentHive will automatically use Demo Mode."
            )


# =========================================================
# HEADER
# =========================================================

st.title("🤖 AgentHive AI")

st.caption(
    "Multi-Agent Decision Intelligence & Research System"
)

st.markdown(
    """
AgentHive transforms complex goals into structured decisions
using **live web research, evidence traceability, opportunity
analysis, risk auditing, and strategic planning**.
"""
)

st.markdown("---")


# =========================================================
# USER INPUT
# =========================================================

goal = st.text_input(
    "🎯 Enter a complex goal or decision",
    placeholder=(
        "e.g. Should I build an AI cybersecurity startup in India?"
    )
)


# =========================================================
# EXECUTION
# =========================================================

if st.button(
    "🚀 Activate AgentHive",
    use_container_width=True
):

    if not goal.strip():

        st.warning(
            "Please enter a goal first."
        )

        st.stop()


    with st.status(
        "AgentHive is working...",
        expanded=True
    ) as status:

        try:

            st.write(
                "🔎 Research Agent: analyzing research dimensions..."
            )

            st.write(
                "🌐 Gathering market evidence..."
            )

            st.write(
                "🏢 Investigating competitors..."
            )

            st.write(
                "⚙️ Analyzing technology trends..."
            )

            st.write(
                "💰 Investigating funding environment..."
            )

            st.write(
                "⚠️ Identifying potential risks..."
            )


            results = run_agenthive(
                goal,
                execution_mode,
                model
            )


            st.write(
                "📚 Evidence Aggregator: mapping source IDs..."
            )

            st.write(
                "🧠 Decision Intelligence: synthesizing evidence..."
            )

            st.write(
                "🛡️ Risk Auditor: challenging assumptions..."
            )

            st.write(
                "📋 Strategic Planner: generating roadmap..."
            )


            status.update(
                label="✅ Decision process complete",
                state="complete",
                expanded=False
            )


        except Exception as error:

            status.update(
                label="❌ Agent execution failed",
                state="error"
            )

            st.error(
                f"AgentHive encountered an unexpected error: {error}"
            )

            st.stop()


    # =====================================================
    # STATUS
    # =====================================================

    if results["mode"] == "Gemini AI":

        st.success(
            "🧠 Gemini AI analysis completed "
            "with evidence traceability."
        )

    elif results["mode"] == "Demo Mode (Automatic Fallback)":

        if results["status"] == "quota":

            st.warning(
                "⚠️ Gemini quota unavailable. "
                "AgentHive automatically switched to Demo Mode."
            )

        else:

            st.warning(
                "⚠️ Gemini unavailable. "
                "AgentHive automatically switched to Demo Mode."
            )

    else:

        st.info(
            "🧪 Demo Mode — live research was performed; "
            "Gemini API was not used."
        )


    # =====================================================
    # RESEARCH METRICS
    # =====================================================

    research = results["research"]

    total_sources = sum(
        len(sources)
        for sources in research.values()
    )

    categories_found = sum(
        1
        for sources in research.values()
        if sources
    )


    col1, col2, col3 = st.columns(3)


    with col1:

        st.metric(
            "Research Sources",
            total_sources
        )


    with col2:

        st.metric(
            "Research Dimensions",
            f"{categories_found}/5"
        )


    with col3:

        st.metric(
            "Execution Mode",
            results["mode"].replace(
                " (Automatic Fallback)",
                ""
            )
        )


    st.markdown("---")


    # =====================================================
    # STRATEGIC DECISION
    # =====================================================

    st.subheader(
        "🏁 Strategic Recommendation"
    )

    st.markdown(
        results["decision"]
    )


    # =====================================================
    # EVIDENCE TRACEABILITY
    # =====================================================

    st.markdown("---")

    st.subheader(
        "🔗 Evidence Traceability"
    )

    st.caption(
        "Every research source receives a stable identifier "
        "so analytical claims can be traced back to evidence."
    )


    numbered_research = number_sources(
        research
    )


    for category, sources in numbered_research.items():

        with st.expander(
            f"📚 {category} Evidence — {len(sources)} sources"
        ):

            if not sources:

                st.warning(
                    "No usable evidence found."
                )

            else:

                for source in sources:

                    st.markdown(
                        f"### {source['source_id']}"
                    )

                    st.markdown(
                        f"**{source['title']}**"
                    )

                    st.markdown(
                        f"[🔗 Open Source]({source['url']})"
                    )

                    if source["snippet"]:

                        st.write(
                            source["snippet"]
                        )

                    st.markdown("---")


# =========================================================
# FOOTER
# =========================================================

st.markdown("---")

st.caption(
    "AgentHive AI • Research → Evidence → Analyze → Audit → Plan"
)