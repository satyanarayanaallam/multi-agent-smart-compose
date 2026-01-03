from typing import Dict

from workflows.state import SmartComposeState


def style_agent(state: SmartComposeState) -> SmartComposeState:
    """Minimal style agent with tone awareness.

    Reads the existing "draft" from state plus an optional "tone"
    preference (e.g., "formal" or "casual") and produces a
    "styled_draft". Still deterministic so you can focus on how
    preferences flow through the graph.
    """
    draft = state.get("draft", "")
    tone = (state.get("tone") or "neutral").lower()

    if tone == "formal":
        styled_draft = f"[Formal tone]\n{draft}"
    elif tone == "casual":
        styled_draft = f"[Casual tone]\n{draft}"
    else:
        styled_draft = f"[Neutral tone]\n{draft}"

    new_state: SmartComposeState = dict(state)
    new_state["styled_draft"] = styled_draft
    return new_state
