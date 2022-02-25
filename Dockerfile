FROM python:3.7-slim

USER root

RUN apt-get update
RUN apt-get install -y curl jq

COPY core/requirements.txt /requirements.txt
RUN pip3 install -r /requirements.txt

COPY core/search_pull_request_comments.py /search_pull_request_comments.py
COPY entrypoint.sh /entrypoint.sh

RUN chmod +x entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]