from __future__ import annotations

import sys
from json import loads
from typing import Any
import requests

MAX_PAGES = 10
PER_PAGE = 100


def fetch_all_pages(url: str, token: str) -> list[dict[str, Any]]:
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "Authorization": f"token {token}",
    }

    separator = "&" if "?" in url else "?"
    paginated_url = f"{url}{separator}per_page={PER_PAGE}"

    accumulated: list[dict[str, Any]] = []
    for _ in range(MAX_PAGES):
        response = requests.get(paginated_url, headers=headers, timeout=30)
        if response.status_code != 200:
            raise RuntimeError(
                f"GitHub API returned {response.status_code} for {paginated_url}: "
                f"{response.text[:200]}"
            )

        page_data = response.json()
        if not isinstance(page_data, list):
            raise TypeError(
                f"Expected list from GitHub API, got {type(page_data).__name__}"
            )

        accumulated.extend(page_data)

        next_url = _parse_next_link(response.headers.get("Link", ""))
        if next_url is None:
            break
        paginated_url = next_url

    return accumulated


def _parse_next_link(link_header: str) -> str | None:
    for part in link_header.split(","):
        if 'rel="next"' in part:
            start = part.index("<") + 1
            end = part.index(">")
            return part[start:end]
    return None


def extract_commenters(event_json: str, token: str, required_user_csv: str) -> int:
    event = _parse_event(event_json)
    links = event["pull_request"]["_links"]

    issue_comments = fetch_all_pages(links["comments"]["href"], token)
    review_comments = fetch_all_pages(links["review_comments"]["href"], token)

    commenters = {
        comment["user"]["login"]
        for comment in (*issue_comments, *review_comments)
    }

    required_users = [u.strip() for u in required_user_csv.split(",")]
    if any(user in commenters for user in required_users):
        return 0

    print(
        f"Required: {required_users}. "
        f"Found: {sorted(commenters) if commenters else '(none)'}",
        file=sys.stderr,
    )
    return 1


def _parse_event(raw: str) -> dict[str, Any]:
    parsed = loads(raw)
    if not isinstance(parsed, dict):
        raise TypeError(f"Expected dict from event JSON, got {type(parsed).__name__}")
    if "event" in parsed:
        return parsed["event"]
    return parsed


if __name__ == "__main__":
    if len(sys.argv) != 4:
        raise SystemExit(
            f"Usage: {sys.argv[0]} <event_json> <github_token> <required_users>"
        )

    raise SystemExit(
        extract_commenters(sys.argv[1], sys.argv[2], sys.argv[3])
    )
