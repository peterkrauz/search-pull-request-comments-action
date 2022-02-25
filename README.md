# Search pull-request comments Action

Searches a pull-request for any comment left by a specific user. If no comment is found, the step fails.
Searches through both simple and review comments.

## Installation

On `.github/workflows/`, create a file `pr_comment_search.yml`:

```yml
name: <name goes here>
on: pull_request

jobs:
  search_pull_request_comments:
    runs-on: ubuntu-latest
    container: python:3.7-slim

    steps:
      - name: Search pull-request comments
        uses: peterkrauz/search-pull-request-comments@v0.0.2
        env:
          REQUIRED_COMMENT_USER: "john-doe"
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          EVENT_DETAILS: ${{ toJSON(github.event) }}
```

In this setup, the step will succeed if there's any comment written by `john-doe` in your pull-request.
If `john-doe` did not comment in this pull-request, the job will fail.