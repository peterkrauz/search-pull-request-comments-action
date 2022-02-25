#!/bin/bash

result=$(python3 /search_pull_request_comments.py "$EVENT_DETAILS" "$GITHUB_TOKEN" "$REQUIRED_COMMENT_USER")

if [ "$result" = "0" ]; then
    echo "User that was required to comment did leave a comment - all good!"
else
    echo "Couldn't find any comment from the required user"
    exit 1
fi