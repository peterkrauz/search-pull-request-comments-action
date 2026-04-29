#!/bin/bash
set -euo pipefail

echo "User(s) to search: $REQUIRED_COMMENT_USER"

python3 /search_pull_request_comments.py \
    "$EVENT_DETAILS" \
    "$GITHUB_TOKEN" \
    "$REQUIRED_COMMENT_USER"
