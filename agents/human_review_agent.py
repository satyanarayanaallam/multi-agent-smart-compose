from workflows.state import SmartComposeState


def human_review_agent(state: SmartComposeState) -> SmartComposeState:
    """Human-in-the-loop review step.

    - If state["auto_approve"] is True, we auto-approve without
      prompting (useful for tests and non-interactive runs).
    - Otherwise, we show a brief summary and ask the user whether to
      approve or request another revision.
    """

    # Auto-approve path (e.g., tests)
    if state.get("auto_approve"):
        new_state: SmartComposeState = dict(state)
        new_state["review_decision"] = "approve"
        return new_state

    draft = state.get("draft", "")
    styled = state.get("styled_draft", "")
    feedback_score = state.get("feedback_score")
    is_factually_ok = state.get("is_factually_ok")

    print("\n--- Human Review ---")
    print(f"Draft (truncated): {draft[:200]}")
    print(f"Styled (truncated): {styled[:200]}")
    print(f"Feedback score: {feedback_score}")
    print(f"Is factually OK: {is_factually_ok}")

    while True:
        choice = input("Approve this suggestion? (a = approve, r = revise) [a]: ").strip().lower() or "a"
        if choice in {"a", "approve"}:
            decision = "approve"
            break
        if choice in {"r", "revise"}:
            decision = "revise"
            break
        print("Please enter 'a' to approve or 'r' to revise.")

    new_state = dict(state)
    new_state["review_decision"] = decision
    return new_state
