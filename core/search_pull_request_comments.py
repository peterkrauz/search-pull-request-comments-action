import logging
from json import loads

import requests

logger = logging.getLogger(__name__)


def search_comments(github_info, token: str, required_user):
    if isinstance(github_info, str):
        github_info = loads(github_info)

    if "event" in github_info:
        github_info = github_info["event"]

    links = github_info["pull_request"]["_links"]
    review_comments = fetch(links["review_comments"]["href"], token)

    users_that_commented = [comm["user"]["login"] for comm in review_comments]
    required_user_has_commented = str(required_user) in users_that_commented

    return {
        "comments": users_that_commented,
        "required_user_has_commented": required_user_has_commented
    }


def fetch(url: str, token: str) -> list:
    headers = {
        "Accept": "application/vnd.github+json",
        "X-Github-Api-Version": "2022-11-28",
        "Authorization": f"Bearer {token}",
    }
    print("Making a request to", url)
    print()
    response = requests.get(url, headers=headers)
    print("status:", response.status_code)
    print()
    return response.json()


if __name__ == "__main__":
    import sys

    result = search_comments(sys.argv[1], sys.argv[2], sys.argv[3])

    if result["required_user_has_commented"]:
        print(0)
    else:
        print(result["comments"])
