def local_evidence_analysis(
    goal,
    categorized_results
):
    category_stats = {
        category: len(sources)
        for category, sources in categorized_results.items()
    }

    total_sources = sum(category_stats.values())

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


def build_evidence_digest(categorized_results):
    digest = []

    for category, sources in categorized_results.items():

        digest.append(
            f"\n===== {category.upper()} EVIDENCE ====="
        )

        if not sources:
            digest.append("No usable evidence found.")
            continue

        for index, source in enumerate(sources, start=1):

            # Keep Gemini's input compact.
            snippet = source.get("snippet", "").strip()

            if len(snippet) > 500:
                snippet = snippet[:500] + "..."

            digest.append(
                f"""
[{category} Source {index}]
Title: {source.get("title", "")}
URL: {source.get("url", "")}
Evidence: {snippet}
"""
            )

    return "\n".join(digest)


def demo_decision(
    goal,
    categorized_results
):
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

    evidence_text = "\n".join(evidence_summary)

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

**Evidence:** See Market sources.

### Competitors

Compare existing companies, products, features, pricing, and
target users to identify potential gaps.

**Evidence:** See Competitors sources.

### Technology

Evaluate technical maturity, implementation complexity,
infrastructure requirements, and potential differentiation.

**Evidence:** See Technology sources.

### Funding

Investigate funding, accelerators, grants, partnerships,
investment activity, and capital requirements.

**Evidence:** See Funding sources.

---

## 🛡️ Risk Audit

### Technical Risk

Implementation may require more infrastructure or engineering
effort than initially expected.

**Mitigation:** Build a small proof-of-concept.

**Evidence:** See Technology and Risks sources.

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

Interview potential users.

### 2. Analyze the Competition

Compare existing solutions and identify differentiation.

### 3. Build an MVP

Build the smallest implementation capable of testing the core
assumption.

---

## 🗓️ 30-Day Roadmap

### Week 1 — Research & Validation

- Review evidence.
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

---

> 🧪 **Demo Mode:** Live web research was performed. Strategic
> reasoning was generated locally without using Gemini.
"""


def decision_agent(
    model,
    goal,
    categorized_results
):
    if not model:
        return None, "no_api_key"

    evidence_digest = build_evidence_digest(
        categorized_results
    )

    prompt = f"""
You are the Decision Intelligence Engine inside AgentHive.

Analyze the user's goal using ONLY the supplied research evidence.

USER GOAL:
{goal}

RESEARCH EVIDENCE:
{evidence_digest}

Rules:

- Do not invent facts.
- Do not invent statistics.
- Do not invent sources.
- Every factual claim must reference the supplied source label.
- Clearly distinguish evidence from interpretation and assumptions.
- If evidence is weak, say so.

Return a concise professional report with:

## 🎯 Recommendation

Choose:
- Proceed
- Proceed cautiously
- Validate further
- Avoid

Explain why.

## 🔎 Evidence Summary

Cover:
- Market
- Competitors
- Technology
- Funding
- Risks

Use source labels.

## 🚀 Opportunity Analysis

Identify evidence-backed opportunities.

## 🛡️ Risk Audit

Cover:
- Technical
- Market
- Competitive
- Regulatory
- Execution

Use:
Risk → Evidence → Mitigation

## 🧠 Assumption Audit

Identify the 3 most important assumptions.

## 📋 Priority Actions

Give exactly 3 actions.

## 🗓️ 30-Day Roadmap

Give one focus for each week.

## 📊 Success Metrics

Give measurable indicators.

## 🔐 Final Decision Framework

Research → Validate → Prototype → Test → Measure → Scale
"""

    try:
        response = model.generate_content(prompt)

        if not response or not response.text:
            return None, "empty_response"

        return response.text, "success"

    except Exception as error:

        error_text = str(error).lower()

        if "429" in error_text or "quota" in error_text:
            return None, "quota"

        return None, "error"