from typing import Dict

from llm.gemini_client import generate_draft
from workflows.state import SmartComposeState


def drafting_agent(state: SmartComposeState) -> SmartComposeState:
        """Drafting agent backed by Gemini when available.

        - Reads "user_input" and an optional "iteration" counter from state.
        - Calls a Gemini-backed generator (with a safe fallback if no API
            key is configured).
        - Writes updated "iteration" and "draft" fields back to state.
        """
        user_input = state.get("user_input", "")

        # Track how many drafting iterations we've done.
        iteration = state.get("iteration", 0) + 1

        draft = generate_draft(user_input=user_input, iteration=iteration)

        new_state: SmartComposeState = dict(state)
        new_state["iteration"] = iteration
        new_state["draft"] = draft
        return new_state
