import streamlit as st
from ddgs import DDGS


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