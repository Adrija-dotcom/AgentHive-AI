import os
import time

import streamlit as st
from dotenv import load_dotenv
import google.generativeai as genai
from ddgs import DDGS


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

if API_KEY:
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel(MODEL_NAME)
else:
    model = None


# =========================================================
# RESEARCH CATEGORIES
# =========================================================

RESEARCH_CATEGORIES = {
    "Market": (
        "market size trends growth demand opportunities "
        "industry landscape customer needs"
    ),

    "Competitors": (
        "competitors companies startups products "
        "market leaders alternatives differentiation"
    ),

    "Technology": (
        "technology trends tools platforms technical developments "
        "AI innovation architecture implementation"
    ),

    "Funding": (
        "startup funding investment venture capital grants "
        "accelerators partnerships business opportunities"
    ),

    "Risks": (
        "risks challenges regulations cybersecurity legal "
        "technical barriers failures adoption obstacles"
    )
}


# =========================================================
# WEB SEARCH
# =========================================================

@st.cache_data(ttl=600)
def search_web(query, max_results=5):
    """
    Search the web and return structured sources.
    """

    try:

        with DDGS() as ddgs:

            results = list(
                ddgs.text(
                    query,
                    max_results=max_results
                )
            )

        sources = []

        for result in results:

            title = result.get("title", "").strip()
            url = result.get("href", "").strip()
            snippet = result.get("body", "").strip()

            if title and url.startswith("http"):

                sources.append({
                    "title": title,
                    "url": url,
                    "snippet": snippet
                })

        return sources

    except Exception:

        return []


# =========================================================
# RESEARCH AGENT
# =========================================================

def researcher_agent(goal):
    """
    Break the goal into five research dimensions and
    collect external evidence for each dimension.
    """

    categorized_results = {}

    for category, research_focus in RESEARCH_CATEGORIES.items():

        query = f"{goal} {research_focus}"

        results = search_web(
            query,
            max_results=5
        )

        categorized_results[category] = results

        time.sleep(0.3)

    return categorized_results


# =========================================================
# SOURCE NUMBERING
# =========================================================

def number_sources(categorized_results):
    """
    Assign stable source IDs such as:
    Market Source 1
    Competitors Source 3
    """

    numbered = {}

    for category, sources in categorized_results.items():

        numbered[category] = []

        for index, source in enumerate(
            sources,
            start=1
        ):

            numbered[category].append({
                **source,
                "source_id": f"{category} Source {index}"
            })

    return numbered


# =========================================================
# EVIDENCE DIGEST
# =========================================================

def build_evidence_digest(categorized_results):
    """
    Convert research into a source-labelled evidence package.
    """

    numbered_results = number_sources(
        categorized_results
    )

    digest = []

    for category, sources in numbered_results.items():

        digest.append(
            f"\n===== {category.upper()} EVIDENCE ====="
        )

        if not sources:

            digest.append(
                "No usable evidence found."
            )

            continue

        for source in sources:

            digest.append(
                f"""
[{source["source_id"]}]
Title: {source["title"]}
URL: {source["url"]}
Evidence snippet: {source["snippet"]}
"""
            )

    return "\n".join(digest)


# =========================================================
# LOCAL EVIDENCE ANALYZER
# =========================================================

def local_evidence_analysis(goal, categorized_results):

    category_stats = {}

    for category, sources in categorized_results.items():

        category_stats[category] = len(sources)

    total_sources = sum(
        category_stats.values()
    )

    categories_found = sum(
        1
        for count in category_stats.values()
        if count > 0
    )

    strongest_category = (
        max(
            category_stats,
            key=category_stats.get
        )
        if total_sources
        else "None"
    )

    return {
        "total_sources": total_sources,
        "categories_found": categories_found,
        "category_stats": category_stats,
        "strongest_category": strongest_category
    }


# =========================================================
# DEMO DECISION ENGINE
# =========================================================

def demo_decision(goal, categorized_results):

    analysis = local_evidence_analysis(
        goal,
        categorized_results
    )

    total_sources = analysis["total_sources"]
    categories_found = analysis["categories_found"]
    strongest_category = analysis["strongest_category"]

    evidence_summary = []

    for category, sources in categorized_results.items():

        if sources:

            evidence_summary.append(
                f"- **{category}:** {len(sources)} sources collected"
            )

        else:

            evidence_summary.append(
                f"- **{category}:** No usable sources found"
            )

    evidence_text = "\n".join(
        evidence_summary
    )

    return f"""
## 🎯 Recommendation

**Validate before scaling:**

> {goal}

AgentHive analyzed the goal across **{categories_found}/5
research dimensions** and collected **{total_sources} external
research sources**.

The strongest research coverage currently comes from:

**{strongest_category}**

The collected sources provide an initial evidence base. They do
not automatically prove that the goal will succeed.

---

## 🔎 Evidence Coverage

{evidence_text}

---

## 🚀 Opportunity Analysis

### Market

Evaluate demand, customer pain, market growth, and target-user
needs before committing significant resources.

**Evidence status:** See the Market sources below.

### Competitors

Existing companies and products should be compared to identify
gaps and differentiation opportunities.

**Evidence status:** See the Competitors sources below.

### Technology

Current technology trends can create opportunities, but technical
complexity and implementation constraints must be evaluated.

**Evidence status:** See the Technology sources below.

### Funding

Funding, accelerator, partnership, and investment signals can
help determine whether the business environment is favorable.

**Evidence status:** See the Funding sources below.

---

## 🛡️ Risk Audit

### Technical Risk

Implementation may require more infrastructure or engineering
effort than initially expected.

**Mitigation:** Build a small proof-of-concept.

**Evidence:** See Risks sources.

### Market Risk

Research signals do not guarantee customer demand.

**Mitigation:** Validate the problem directly with potential users.

**Evidence:** See Market sources.

### Competitive Risk

Existing companies may already have stronger technology,
distribution, funding, or customer relationships.

**Mitigation:** Identify a narrow underserved segment.

**Evidence:** See Competitors sources.

### Regulatory Risk

Privacy and regulatory requirements may affect implementation.

**Mitigation:** Identify applicable regulations before launch.

**Evidence:** See Risks sources.

---

## 🧠 Assumption Audit

The most important assumptions to validate are:

1. Target users actually experience the problem.
2. Existing solutions do not completely solve it.
3. Users are willing to adopt the proposed solution.

These are **assumptions**, not established facts.

---

## 📋 Priority Actions

### 1. Validate the Problem

Interview potential users and determine whether the problem is
frequent and important.

### 2. Analyze the Competition

Compare products, features, pricing, target users, and weaknesses.

### 3. Build a Minimum Viable Prototype

Build the smallest implementation capable of testing the core
assumption.

---

## 🗓️ 30-Day Roadmap

### Week 1 — Research & Validation

- Review collected evidence.
- Validate assumptions.
- Identify target users.
- Analyze competitors.

### Week 2 — Prototype

- Define MVP.
- Select technology stack.
- Build the core workflow.

### Week 3 — Testing

- Test with users.
- Collect feedback.
- Measure failures and success rates.

### Week 4 — Evaluation

- Analyze results.
- Reassess risks.
- Improve the prototype.
- Decide whether to continue, pivot, or stop.

---

## 📊 Success Metrics

Track:

- Number of validated assumptions
- Number of users interviewed
- Prototype completion
- Task success rate
- User feedback
- Technical failure rate
- Development time
- Estimated operating cost

---

## 🔐 Decision Framework

**Research → Validate → Prototype → Test → Measure → Scale**

The next decision should be based on evidence rather than
assumptions.

---

> 🧪 **Demo Mode:** Live web research was performed. Strategic
> reasoning was generated locally without using Gemini.
"""


# =========================================================
# GEMINI DECISION INTELLIGENCE
# =========================================================

def decision_agent(goal, categorized_results):

    if not model:

        return None, "no_api_key"

    evidence_digest = build_evidence_digest(
        categorized_results
    )

    prompt = f"""
You are the Decision Intelligence Engine inside AgentHive.

Transform external research evidence into an evidence-traceable
decision report.

USER GOAL:
{goal}

EXTERNAL RESEARCH:
{evidence_digest}

IMPORTANT:

Every important factual claim MUST reference one or more supplied
sources.

Use the exact source labels:

[Market Source 1]
[Market Source 2]
[Competitors Source 1]
[Technology Source 1]
[Funding Source 1]
[Risks Source 1]

Never invent a source.

Never create a citation for information that is not supported by
the supplied evidence.

Do not invent statistics.

Distinguish:

1. Evidence-backed findings
2. Reasonable interpretation
3. Assumptions requiring validation

If the evidence is weak, conflicting, or insufficient, explicitly
say so.

Return this structure:

## 🎯 Recommendation

Give one clear recommendation:

- Proceed
- Proceed cautiously
- Validate further
- Avoid

Explain the recommendation using source labels.

## 🔎 Evidence Summary

### Market

Summarize the strongest evidence.

### Competitors

Summarize the strongest evidence.

### Technology

Summarize the strongest evidence.

### Funding

Summarize the strongest evidence.

### Risks

Summarize the strongest evidence.

Every factual claim should include a source label.

## 🚀 Opportunity Analysis

Separate:

### Evidence-backed opportunities

Use source labels.

### Potential opportunities requiring validation

Clearly mark these as assumptions.

## 🛡️ Risk Audit

Analyze:

- Technical risk
- Market risk
- Competitive risk
- Regulatory risk
- Execution risk

For every major risk:

**Risk → Evidence → Why it matters → Mitigation**

Use source labels for evidence.

## 🧠 Assumption Audit

Identify the 3 most important assumptions.

For each:

**Assumption → Existing evidence → Validation method**

## 📋 Priority Actions

Give exactly 3 specific actions.

## 🗓️ 30-Day Roadmap

### Week 1 — Research & Validation

### Week 2 — Prototype

### Week 3 — Testing

### Week 4 — Evaluation & Decision

## 📊 Success Metrics

Give measurable indicators.

## 🔐 Final Decision Framework

Finish with:

**Research → Validate → Prototype → Test → Measure → Scale**

Keep the report professional and concise.
"""

    try:

        response = model.generate_content(
            prompt
        )

        if not response or not response.text:

            return None, "empty_response"

        return response.text, "success"

    except Exception as error:

        error_text = str(error).lower()

        if "429" in error_text or "quota" in error_text:

            return None, "quota"

        return None, "error"


# =========================================================
# ORCHESTRATOR
# =========================================================

def run_agenthive(goal, execution_mode):

    categorized_results = researcher_agent(
        goal
    )

    if execution_mode == "Demo Mode":

        decision = demo_decision(
            goal,
            categorized_results
        )

        return {
            "research": categorized_results,
            "decision": decision,
            "mode": "Demo Mode",
            "status": "success"
        }

    decision, status = decision_agent(
        goal,
        categorized_results
    )

    if status != "success":

        decision = demo_decision(
            goal,
            categorized_results
        )

        return {
            "research": categorized_results,
            "decision": decision,
            "mode": "Demo Mode (Automatic Fallback)",
            "status": status
        }

    return {
        "research": categorized_results,
        "decision": decision,
        "mode": "Gemini AI",
        "status": "success"
    }


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
            "Demo Mode performs live web research but does not "
            "use Gemini API requests."
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
                execution_mode
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
            "🧠 Gemini AI analysis completed with evidence traceability."
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
        "Every research source receives a stable identifier so "
        "analytical claims can be traced back to the evidence."
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