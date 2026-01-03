import os
from typing import Optional

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI


# Load environment variables from a .env file if present
load_dotenv()

_model: Optional[ChatGoogleGenerativeAI] = None


def _get_model() -> Optional[ChatGoogleGenerativeAI]:
    """Return a cached Gemini chat model if GEMINI_API_KEY is set.

    If no API key is available, return None so callers can fall back
    to a deterministic, offline-friendly behavior (useful for tests
    or when you just want to play with graph structure).
    """
    global _model

    if _model is not None:
        return _model

    # Support both custom GEMINI_API_KEY and the more common
    # GOOGLE_API_KEY used by Gemini tooling.
    api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    if not api_key:
        return None

    _model = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash-lite",
        api_key=api_key,
        temperature=0.7,
    )
    return _model


def generate_draft(user_input: str, iteration: int) -> str:
    """Generate a draft using Gemini when configured, else fallback.

    - If GEMINI_API_KEY is set, call the real Gemini model.
    - Otherwise, return a simple deterministic draft so the graph and
      tests continue to work without external calls.
    """
    model = _get_model()

    prompt = (
        "You are a helpful writing assistant. "
        "Write a clear, concise draft for the user request below. "
        "Respond with just the draft text, no explanations.\n\n"
        f"Draft version: {iteration}\n"
        f"User request: {user_input}"
    )

    if model is None:
        return f"[Fallback draft v{iteration}] {user_input}"

    try:
        response = model.invoke(prompt)
    except Exception as exc:  # pragma: no cover - defensive fallback
        # If we hit quota / rate limits or any transient error, fall back
        # to a local deterministic draft so the app keeps working.
        return f"[Fallback draft v{iteration} after error: {type(exc).__name__}] {user_input}"

    # LangChain ChatModels typically return an object with a .content attribute.
    return getattr(response, "content", str(response))
