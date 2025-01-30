FROM python:3.11-slim as packages

RUN apt-get update && apt-get install -y curl

RUN curl -sSL https://install.python-poetry.org | \
    POETRY_HOME=/home/challenge/.local python3 -
ENV PATH="/home/challenge/.local/bin:${PATH}"

WORKDIR /home/challenge

COPY pyproject.toml poetry.lock ./

RUN poetry self add poetry-plugin-export

RUN poetry export -f requirements.txt --output requirements.txt --only dev --without-hashes

FROM python:3.11-slim

WORKDIR /app

COPY --from=packages /home/challenge/requirements.txt ./

RUN pip install --no-cache-dir -r /app/requirements.txt

COPY ./app /app

EXPOSE 5000

CMD ["sh", "-c", "flask db init || true && flask db migrate -m 'Auto migration' || true && flask db upgrade && python run.py"]