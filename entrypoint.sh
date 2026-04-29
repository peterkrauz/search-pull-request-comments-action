#!/bin/bash

echo "User(s) to search: $REQUIRED_COMMENT_USER"

result=$(python3 /search_pull_request_comments.py "$EVENT_DETAILS" "$GITHUB_TOKEN" "$REQUIRED_COMMENT_USER")

echo "Result: $result"

if [ "$result" = "0" ]; then
    echo "User that was required to comment did leave a comment - all good!"
else
    echo "Couldn't find any comment from any of the required users"
    echo "Here's everyone that did comment: $result"
    exit 1
fi