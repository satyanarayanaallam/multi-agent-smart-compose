from typing import Dict

from langgraph.graph import StateGraph, END

from agents.drafting_agent import drafting_agent
from agents.style_agent import style_agent
from agents.feedback_agent import feedback_agent
from agents.fact_checking_agent import fact_checking_agent
from agents.human_review_agent import human_review_agent
from agents.supervisor_agent import supervisor_agent
from workflows.state import SmartComposeState


def create_app():
    """Create a LangGraph app with drafting, style, and supervisor nodes.

    State is represented as a SmartComposeState TypedDict with keys like:
    - "user_input": str
    - "iteration": int (how many drafting iterations we've done)
    - "draft": str (added by the drafting agent)
    - "styled_draft": str (added by the style agent)
    - "feedback_score": float (added by the feedback agent)
    - "needs_revision": bool (added by the feedback agent)
    """
    builder = StateGraph(SmartComposeState)

    # Register nodes
    builder.add_node("drafting_agent", drafting_agent)
    builder.add_node("style_agent", style_agent)
    builder.add_node("feedback_agent", feedback_agent)
    builder.add_node("fact_checking_agent", fact_checking_agent)
    builder.add_node("human_review_agent", human_review_agent)
    builder.add_node("supervisor_agent", supervisor_agent)

    # Linear part:
    # user_input -> drafting_agent -> style_agent -> feedback_agent
    # -> fact_checking_agent -> human_review_agent -> supervisor_agent
    builder.set_entry_point("drafting_agent")
    builder.add_edge("drafting_agent", "style_agent")
    builder.add_edge("style_agent", "feedback_agent")
    builder.add_edge("feedback_agent", "fact_checking_agent")
    builder.add_edge("fact_checking_agent", "human_review_agent")
    builder.add_edge("human_review_agent", "supervisor_agent")

    # Simple control logic: supervisor can either request a revision (loop
    # back to drafting) or finish.

    def route_from_supervisor(state: SmartComposeState) -> str:
        iteration = state.get("iteration", 0)
        needs_revision = state.get("needs_revision", False)
        is_factually_ok = state.get("is_factually_ok", True)
        review_decision = state.get("review_decision", "approve")

        # If human wants a revision, or feedback/facts look bad, and
        # we haven't exceeded a small iteration cap, loop once more.
        if (review_decision == "revise" or needs_revision or not is_factually_ok) and iteration < 2:
            return "revise"
        return "finish"

    builder.add_conditional_edges(
        "supervisor_agent",
        route_from_supervisor,
        {
            "revise": "drafting_agent",
            "finish": END,
        },
    )

    # Compile the graph into an executable app
    return builder.compile()


if __name__ == "__main__":
    app = create_app()

    user_input = input("Enter a prompt for the drafting + style agents: ")
    initial_state = {"user_input": user_input}

    result = app.invoke(initial_state)

    print("\n=== Resulting state ===")
    print(result)
