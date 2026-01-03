from workflows.state import SmartComposeState
from tools.search_tool import simple_search


def fact_checking_agent(state: SmartComposeState) -> SmartComposeState:
    """Minimal fact-checking agent using a stub search tool.

    - Reads the current styled draft.
    - Sends it to a fake search tool that returns a verdict.
    - Writes 'fact_check_result' and 'is_factually_ok' into state.
    """

    styled = state.get("styled_draft", "")

    # In a real system, you'd extract claims. Here we send the whole
    # styled draft to a simple Wikipedia-backed search tool.
    search_result = simple_search(styled)
    verdict = search_result.get("verdict", "unknown")

    is_ok = verdict in {"true", "likely_true"}

    new_state: SmartComposeState = dict(state)
    new_state["fact_check_result"] = search_result
    new_state["is_factually_ok"] = is_ok
    return new_state
