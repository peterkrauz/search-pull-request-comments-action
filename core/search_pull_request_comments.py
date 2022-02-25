import logging
from json import loads, dumps

import requests

logger = logging.getLogger(__name__)


def fetch(url: str, token: str) -> list:
    headers = {"Accept": "application/vnd.github.v3+json", "Authorization": f"token {token}"}
    return requests.get(url, headers=headers).json()


def search_comments(github_info, token: str, required_user: str):

    if isinstance(github_info, str):
        github_info = loads(github_info)

    pr_details = github_info["event"]["pull_request"]
    links = pr_details["_links"]

    simple_comments = fetch(links["comments"]["href"], token)
    review_comments = fetch(links["review_comments"]["href"], token)

    users_that_left_a_comment = [c["user"]["login"] for c in (simple_comments + review_comments)]
    required_user_has_commented = required_user in users_that_left_a_comment

    if required_user_has_commented:
        return 0

    return 1


if __name__ == "__main__":
    import sys

    print(search_comments(sys.argv[1], sys.argv[2], sys.argv[3]))
