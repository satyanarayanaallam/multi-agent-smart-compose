from typing import Dict

from workflows.state import SmartComposeState


def feedback_agent(state: SmartComposeState) -> SmartComposeState:
    """Minimal feedback agent.

    For now, we compute a trivial "score" based on length of the
    styled draft and decide if it "needs_revision". This is purely
    deterministic and just demonstrates how one agent can annotate
    state for the supervisor to use.
    """

    styled = state.get("styled_draft", "")
    length = len(styled)

    # Toy scoring: longer than 40 chars is "good enough".
    score = min(1.0, length / 80.0)
    needs_revision = length < 40

    new_state: SmartComposeState = dict(state)
    new_state["feedback_score"] = score
    new_state["needs_revision"] = needs_revision
    return new_state
