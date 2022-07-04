FROM "python:3.8.5-slim"

WORKDIR /workdir

COPY Pipfile .

RUN pip install pipenv && \
    pipenv lock -r > requirements.txt && \
    pip install -r requirements.txt
