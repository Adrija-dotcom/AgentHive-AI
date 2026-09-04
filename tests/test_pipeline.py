import sys
from pathlib import Path

sys.path.insert(
    0,
    str(Path(__file__).resolve().parents[1])
)

from agents.decision import (
    local_evidence_analysis,
    build_evidence_digest,
)
from agents.researcher import number_sources


def sample_research():
    return {
        "Market": [
            {
                "title": "Market Source",
                "url": "https://example.com/market",
                "snippet": "Market evidence."
            }
        ],
        "Competitors": [
            {
                "title": "Competitor Source",
                "url": "https://example.com/competitor",
                "snippet": "Competitor evidence."
            }
        ],
        "Technology": [],
        "Funding": [],
        "Risks": [
            {
                "title": "Risk Source",
                "url": "https://example.com/risk",
                "snippet": "Risk evidence."
            }
        ]
    }


def test_number_sources():
    research = sample_research()

    numbered = number_sources(research)

    assert numbered["Market"][0]["source_id"] == "Market Source 1"
    assert numbered["Competitors"][0]["source_id"] == "Competitors Source 1"
    assert numbered["Risks"][0]["source_id"] == "Risks Source 1"


def test_evidence_analysis():
    research = sample_research()

    result = local_evidence_analysis(
        "Test goal",
        research
    )

    assert result["total_sources"] == 3
    assert result["categories_found"] == 3


def test_evidence_digest():
    research = sample_research()

    digest = build_evidence_digest(research)

    assert "[Market Source 1]" in digest
    assert "[Competitors Source 1]" in digest
    assert "[Risks Source 1]" in digest