FROM python:latest

COPY . /opt/
WORKDIR /opt/

COPY pyproject.toml poetry.lock /opt/
RUN python3 -m pip install poetry
RUN poetry config virtualenvs.create false \
    && poetry install --no-dev -n

RUN chmod +x entrypoint.sh
ENTRYPOINT ["/opt/entrypoint.sh"]