from agents.researcher import researcher_agent
from agents.decision import demo_decision


def run_agenthive(goal):

    """
    Execute the AgentHive research and decision pipeline.

    AgentHive currently operates entirely in Demo Mode:
    live web research + local decision intelligence.
    """

    categorized_results = researcher_agent(
        goal
    )

    decision = demo_decision(
        goal,
        categorized_results
    )

    return {
        "research": categorized_results,
        "decision": decision,
        "mode": "Live Research",
        "status": "success"
    }