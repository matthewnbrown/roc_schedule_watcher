FROM python:3.11.4-bookworm AS base

RUN python -m pip install --upgrade pip
RUN pip install flake8 pytest

WORKDIR /app/

COPY ./ .

RUN pip install .
RUN flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
RUN pytest

ENTRYPOINT python3 run.py $WATCHERARGS

