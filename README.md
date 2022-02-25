# Linear Ticket Search Action

Searches a pull-request for any Linear ticket reference. Fails if it doesn't find any.

## Installation

On `.github/workflows/`, create a file `pr_comment_search.yml`:

```yml
name: <name goes here>
on: pull_request

jobs:
  search_linear_ticket:
    runs-on: ubuntu-latest
    container: python:3.7-slim

    steps:
      - name: Checkout repo
        uses: actions/checkout@v2

      - name: Search Linear ticket
        uses: peterkrauz/search-pull-request-comments@v0.0.2
        env:
          REQUIRED_COMMENT_USER: "john-doe"
          EVENT_DETAILS: ${{ toJSON(github) }}
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

The step will succeed if there's any comment written by `john-doe` in your pull-request.
Otherwise, it'll fail.