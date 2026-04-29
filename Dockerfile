FROM python:3.13-slim

COPY core/requirements.txt /requirements.txt
RUN pip3 install --no-cache-dir -r /requirements.txt

COPY core/search_pull_request_comments.py /search_pull_request_comments.py
COPY entrypoint.sh /entrypoint.sh

RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
