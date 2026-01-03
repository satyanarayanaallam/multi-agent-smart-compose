from typing import Dict

import requests


WIKIPEDIA_SEARCH_URL = "https://en.wikipedia.org/w/api.php"


def simple_search(query: str) -> Dict:
    """A minimal real search tool using Wikipedia's public API.

    - Sends the query to the Wikipedia search endpoint.
    - Returns a small dict with the top result snippet (if any).
    - This is *not* a full fact-checker but demonstrates calling an
      external HTTP API and feeding the result back into the graph.
    """

    try:
        resp = requests.get(
            WIKIPEDIA_SEARCH_URL,
            params={
                "action": "query",
                "list": "search",
                "srsearch": query,
                "format": "json",
            },
            timeout=5,
        )
        resp.raise_for_status()
        data = resp.json()
        search_results = data.get("query", {}).get("search", [])

        if not search_results:
            return {
                "query": query,
                "verdict": "unknown",
                "snippet": None,
                "source": "wikipedia",
            }

        top = search_results[0]
        snippet = top.get("snippet")

        # Very rough heuristic: if we find any result at all, we say
        # "likely_true"; otherwise "unknown".
        verdict = "likely_true" if snippet else "unknown"

        return {
            "query": query,
            "verdict": verdict,
            "snippet": snippet,
            "source": "wikipedia",
        }
    except Exception as exc:  # pragma: no cover - defensive network handling
        return {
            "query": query,
            "verdict": "error",
            "snippet": None,
            "source": "wikipedia",
            "error_type": type(exc).__name__,
        }
