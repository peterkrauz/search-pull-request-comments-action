import logging
from json import loads, dumps

import requests

logger = logging.getLogger(__name__)


def fetch(url: str, token: str) -> list:
    headers = {"Accept": "application/vnd.github.v3+json", "Authorization": f"token {token}"}
    return requests.get(url, headers=headers).json()


def search_comments(github_info, token: str, required_user):
    if isinstance(github_info, str):
        github_info = loads(github_info)

    if "event" in github_info:
        github_info = github_info["event"]

    links = github_info["pull_request"]["_links"]
    simple_comments = fetch(links["comments"]["href"], token)
    review_comments = fetch(links["review_comments"]["href"], token)

    users_that_left_a_comment = [c["user"]["login"] for c in (simple_comments + review_comments)]
    required_user_has_commented = str(required_user) in users_that_left_a_comment

    return {
        "comments": users_that_left_a_comment,
        "required_user_has_commented": required_user_has_commented
    }


if __name__ == "__main__":
    import sys

    result = search_comments(sys.argv[1], sys.argv[2], sys.argv[3])

    if result["required_user_has_commented"]:
        print(0)
    else:
        print(result["comments"])
