# FROM ghcr.io/astral-sh/uv:latest
FROM python:3.12-slim-bookworm
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

RUN apt-get update && apt-get install -y libpq-dev

ADD . /app
# Set the working directory
WORKDIR /app

# Copy your project files into the Docker image
# COPY . .

# RUN uv venv && \
#     uv add psycopg2-binary

RUN uv sync --locked

# Install curl and uv
# RUN apt-get update && apt-get install -y curl && \
# 	curl -LsSf https://astral.sh/uv/install.sh | sh && \
# 	. $HOME/.local/bin/env && \
# 	/root/.cargo/bin/uv venv && \
# 	. .venv/bin/activate

# # Install dependencies from pyproject.toml
# RUN /root/.cargo/bin/uv uv sync
ENV PATH="/app/.venv/bin:$PATH"

# Set the entrypoint to your Prefect flow
ENTRYPOINT ["uv", "run", "./pipeline.py"]
