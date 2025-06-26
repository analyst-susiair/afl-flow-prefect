# FROM ghcr.io/astral-sh/uv:latest
# FROM python:3.12-slim-bookworm
# COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

RUN apt-get update && apt-get install -y libpq-dev

ADD . /app
# Set the working directory
WORKDIR /app

# Copy your project files into the Docker image
# COPY . .

VOLUME /var/run/docker.sock:/var/run/docker.sock
# RUN uv venv && \
#     uv add psycopg2-binary

RUN uv sync --locked --no-cache --no-install-project --no-dev


# # Install dependencies from pyproject.toml
# RUN /root/.cargo/bin/uv uv sync
ENV PATH="/app/.venv/bin:$PATH"

# Set the entrypoint to your Prefect flow
ENTRYPOINT ["uv", "run", "./pipeline.py"]
