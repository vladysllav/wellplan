FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /app/

COPY poetry.lock pyproject.toml ./

RUN apt-get update \
    && apt-get install -y build-essential \
    && apt-get install -y libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Add local non-root user to avoid issue with files
ARG USERNAME=code
ARG USER_UID=1000
ARG USER_GID=$USER_UID
RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME -s /bin/bash

RUN pip install --upgrade pip \
    && pip install --upgrade setuptools \
    && pip install poetry \
    && poetry config virtualenvs.create false

RUN poetry install $POETRY_INSTALL_ARGS

COPY . .

# Run the entrypoint script directly
COPY --chown=code:code entrypoint.sh /fastapi-start
RUN sed -i 's/\r$//g' /fastapi-start && chmod +x /fastapi-start


# Select internal user
USER code

CMD ["/app/entrypoint.sh"]
