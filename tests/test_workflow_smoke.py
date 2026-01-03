import sys
from pathlib import Path


# Ensure project root is on sys.path so "workflows" can be imported
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from workflows.langgraph_workflow import create_app


def test_workflow_runs_minimally():
    app = create_app()
    state = {"user_input": "Hello", "auto_approve": True}
    result = app.invoke(state)
    assert "draft" in result
