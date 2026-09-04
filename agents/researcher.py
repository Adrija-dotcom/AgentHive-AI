import time

from services.search import search_web


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


def researcher_agent(goal):
    """
    Break the goal into five research dimensions and
    collect external evidence.
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


def number_sources(categorized_results):
    """
    Assign stable IDs such as:
    Market Source 1
    Competitors Source 2
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