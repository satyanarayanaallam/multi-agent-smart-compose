from typing import TypedDict


class SmartComposeState(TypedDict, total=False):
    """Typed view of the shared graph state.

    Using a TypedDict makes it clearer which keys exist and helps
    keep agents and routing logic in sync.
    """

    # User input and preferences
    user_input: str
    tone: str
    # Optional flags for automation / testing
    auto_approve: bool

    # Drafting iterations and outputs
    iteration: int
    draft: str
    styled_draft: str

    # Feedback / supervision signals
    feedback_score: float
    needs_revision: bool

    # Fact-checking signals
    fact_check_result: dict
    is_factually_ok: bool

    # Human review
    review_decision: str
