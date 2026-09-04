import streamlit as st

from agents.orchestrator import run_agenthive
from agents.researcher import number_sources


st.set_page_config(
    page_title="AgentHive AI",
    page_icon="🤖",
    layout="wide"
)


# ---------------------------------------------------------
# PAGE HEADER
# ---------------------------------------------------------

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


# ---------------------------------------------------------
# SIDEBAR
# ---------------------------------------------------------

with st.sidebar:

    st.header("⚙️ AgentHive Configuration")

    st.success(
        "🧪 Demo Mode — Live Research"
    )

    st.markdown("---")

    st.markdown("### 🧠 Agent Pipeline")

    st.write("🔎 Research Agent")
    st.write("📚 Evidence Aggregator")
    st.write("🧠 Decision Intelligence")
    st.write("🛡️ Risk Auditor")
    st.write("📋 Strategic Planner")

    st.markdown("---")

    st.info(
        "AgentHive performs live web research and generates "
        "strategic analysis locally without requiring an AI API key."
    )


# ---------------------------------------------------------
# USER INPUT
# ---------------------------------------------------------

goal = st.text_input(
    "🎯 Enter a complex goal or decision",
    placeholder=(
        "e.g. Should I build an AI cybersecurity startup in India?"
    )
)


# ---------------------------------------------------------
# EXECUTION
# ---------------------------------------------------------

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
                goal
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


# ---------------------------------------------------------
# EXECUTION STATUS
# ---------------------------------------------------------

    st.success(
        "🧪 AgentHive completed live research and "
        "generated the decision analysis."
    )


# ---------------------------------------------------------
# RESEARCH METRICS
# ---------------------------------------------------------

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
            "Live Research"
        )


# ---------------------------------------------------------
# STRATEGIC RECOMMENDATION
# ---------------------------------------------------------

    st.markdown("---")

    st.subheader(
        "🏁 Strategic Recommendation"
    )

    st.markdown(
        results["decision"]
    )


# ---------------------------------------------------------
# EVIDENCE TRACEABILITY
# ---------------------------------------------------------

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


# ---------------------------------------------------------
# FOOTER
# ---------------------------------------------------------

st.markdown("---")

st.caption(
    "AgentHive AI • Research → Evidence → Analyze → Audit → Plan"
)