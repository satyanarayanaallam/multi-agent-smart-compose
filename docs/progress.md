# LangGraph Learning Progress

This document summarizes what we have built so far in the `multi-agent-smart-compose` project and how it all fits together.

---

## 1. High-Level Goal

Build a **multi-agent Smart Compose system** using LangGraph that:

- Drafts text suggestions
- Applies user-preferred style
- Collects feedback
- Performs basic fact-checking via an external tool
- Optionally asks a human reviewer before finalizing

All of this is orchestrated through a LangGraph workflow operating on a shared state object.

---

## 2. Current Graph Architecture

The main graph is defined in:

- workflows: `workflows/langgraph_workflow.py`
- state schema: `workflows/state.py`

Execution flow:

```text
user_input → drafting_agent → style_agent → feedback_agent
           → fact_checking_agent → human_review_agent → supervisor_agent
                                     ↘ (maybe loop back to drafting_agent)
```

Nodes (agents):

- `drafting_agent`: generates or updates the draft text
- `style_agent`: applies tone-based styling
- `feedback_agent`: scores the suggestion and decides if it needs revision
- `fact_checking_agent`: calls a search tool and estimates factuality
- `human_review_agent`: optional human-in-the-loop approval
- `supervisor_agent`: decides whether to loop or finish

Supervisor logic uses:

- `review_decision` (human review)
- `needs_revision` (feedback)
- `is_factually_ok` (fact-check)
- `iteration` (how many times drafting has run)

If any signal suggests a revision and the iteration cap is not exceeded, the graph loops back to `drafting_agent`; otherwise it finishes.

---

## 3. Shared State Model

File:

- `workflows/state.py`

We use a `TypedDict` to define `SmartComposeState`, making state keys explicit:

- User input & preferences
  - `user_input: str`
  - `tone: str` ("formal", "casual", "neutral", etc.)
  - `auto_approve: bool` (skip human prompt in tests)

- Drafting & styling
  - `iteration: int` (drafting version counter)
  - `draft: str` (LLM or fallback-generated text)
  - `styled_draft: str` (tone-aware variant)

- Feedback
  - `feedback_score: float` (simple length-based score)
  - `needs_revision: bool` (True if suggestion seems too short)

- Fact-checking
  - `fact_check_result: dict` (raw tool output)
  - `is_factually_ok: bool` (derived verdict)

- Human review
  - `review_decision: str` ("approve" or "revise")

Each agent reads some of these keys and writes new/updated values back into the shared state.

---

## 4. Agents Implemented

### 4.1 Drafting Agent

File:

- `agents/drafting_agent.py`

Behavior:

- Reads `user_input` and optional `iteration`.
- Increments `iteration` each time it runs.
- Calls `llm.gemini_client.generate_draft(...)` to get the draft text.
- Writes:
  - `iteration`
  - `draft`

`generate_draft` tries to use Google Gemini via LangChain and falls back to a deterministic string when:

- No API key is configured, or
- The Gemini API returns an error (e.g., quota exceeded).

### 4.2 Style Agent

File:

- `agents/style_agent.py`

Behavior:

- Reads `draft` and `tone`.
- Produces a styled version:
  - `[Formal tone]\n...`
  - `[Casual tone]\n...`
  - `[Neutral tone]\n...`
- Writes:
  - `styled_draft`

This is currently deterministic and label-based, focusing on showing how preferences flow through state.

### 4.3 Feedback Agent

File:

- `agents/feedback_agent.py`

Behavior:

- Reads `styled_draft`.
- Computes:
  - `feedback_score` = min(1.0, len(styled_draft) / 80.0)
  - `needs_revision` = True if `len(styled_draft) < 40` else False
- Writes:
  - `feedback_score`
  - `needs_revision`

This is a toy scoring function meant to illustrate a numeric signal that the supervisor can use.

### 4.4 Fact-Checking Agent

File:

- `agents/fact_checking_agent.py`

Behavior:

- Reads `styled_draft`.
- Calls `tools.simple_search(styled_draft)`.
- Interprets `search_result["verdict"]` as:
  - Acceptable if in {`"true"`, `"likely_true"`}.
- Writes:
  - `fact_check_result` (tool output)
  - `is_factually_ok` (boolean)

### 4.5 Human Review Agent

File:

- `agents/human_review_agent.py`

Behavior:

- If `auto_approve` is True:
  - Sets `review_decision = "approve"` with no user prompt.
- Otherwise (interactive runs):
  - Prints truncated `draft`, `styled_draft`, `feedback_score`, and `is_factually_ok`.
  - Prompts the user: approve (`a`) or revise (`r`).
  - Writes `review_decision` = `"approve"` or `"revise"`.

This shows a basic human-in-the-loop pattern inside a LangGraph workflow.

### 4.6 Supervisor Agent

File:

- `agents/supervisor_agent.py` (currently just passes state through)

The real routing logic is defined in `create_app()` inside:

- `workflows/langgraph_workflow.py`

Function `route_from_supervisor(state)` decides:

- If any of these are true:
  - `review_decision == "revise"`
  - `needs_revision is True`
  - `is_factually_ok is False`
  - and `iteration < 2` (iteration cap)

  → route = `"revise"` → go back to `drafting_agent`.

- Otherwise:

  → route = `"finish"` → `END`.

---

## 5. Tools and LLM Integration

### 5.1 Gemini Client

File:

- `llm/gemini_client.py`

Behavior:

- Loads environment variables using `python-dotenv`.
- Looks for API keys:
  - `GEMINI_API_KEY` or `GOOGLE_API_KEY`.
- If a key is available:
  - Constructs a `ChatGoogleGenerativeAI` model (`gemini-2.5-pro` by default).
  - Calls `model.invoke(prompt)`.
- On error (e.g., quota exceeded) or missing key:
  - Returns a deterministic fallback draft string.

This keeps the graph usable even when external LLM calls fail.

### 5.2 Search Tool (Wikipedia-based)

File:

- `tools/search_tool.py`

Behavior:

- Uses `requests` to call the Wikipedia search API.
- Returns a dict with:
  - `query`
  - `verdict` = `"likely_true"`, `"unknown"`, or `"error"`
  - `snippet` (top result snippet, if any)
  - `source` ("wikipedia")
  - optional `error_type` on failure

The fact-checking agent consumes this and converts it into `is_factually_ok`.

---

## 6. CLI Entry Point and Testing

### 6.1 Running the Workflow

File:

- `run.py`

Flow:

1. Builds the app via `create_app()`.
2. Prompts the user for:
   - `user_input` (prompt for Smart Compose)
   - `tone` (formal/casual/neutral)
3. Constructs initial state:
   - `{"user_input": ..., "tone": ...}`
4. Invokes the app and prints:
   - `Tone`
   - `Iterations`
   - `Draft`
   - `Styled draft`
   - `Feedback score`
   - `Needs revision`
   - `Is factually OK`

### 6.2 Smoke Test

File:

- `tests/test_workflow_smoke.py`

Behavior:

- Imports `create_app()`.
- Uses initial state:
  - `{"user_input": "Hello", "auto_approve": True}`
- Asserts that the resulting state contains a `"draft"` key.

This ensures the end-to-end graph runs without requiring human input.

---

## 7. What You’ve Learned (Conceptually)

- **Stateful design**: thinking in terms of a shared `SmartComposeState` dict that flows through the graph.
- **Nodes as pure transformers**: each agent is a function `state_in -> state_out` that reads/writes specific keys.
- **Control flow via supervisor**: using `add_conditional_edges` and simple rules to loop or finish.
- **Preferences and tools in the state**: tone, feedback scores, fact-check results, and human review decisions all live in the state and influence behavior.
- **Graceful degradation**: both the Gemini-backed drafting and external search tool fail gracefully, falling back to deterministic behavior so the LangGraph structure remains testable.

This file should help you quickly recall how the project is structured and why each piece exists as you continue experimenting with LangGraph.
