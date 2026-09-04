from agents.researcher import researcher_agent
from agents.decision import demo_decision, decision_agent


def run_agenthive(
    goal,
    execution_mode,
    model
):

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
        model,
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