from workflows.langgraph_workflow import create_app


def main() -> None:
    app = create_app()

    user_input = input("Enter a prompt for Smart Compose: ")
    tone = input("Preferred tone (formal/casual/neutral) [neutral]: ") or "neutral"

    state = {"user_input": user_input, "tone": tone}

    result = app.invoke(state)

    print("\n=== Smart Compose Result ===")
    print(f"Tone: {result.get('tone')}")
    print(f"Iterations: {result.get('iteration')} ")
    print(f"Draft: {result.get('draft')}")
    print(f"Styled draft: {result.get('styled_draft')}")
    print(f"Feedback score: {result.get('feedback_score')}")
    print(f"Needs revision: {result.get('needs_revision')}")
    print(f"Is factually OK: {result.get('is_factually_ok')}")


if __name__ == "__main__":
    main()
