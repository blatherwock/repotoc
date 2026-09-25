FROM node:22-trixie-slim

# Install system dependencies (git, task runner, build tools, etc.)
RUN apt-get update \
    && apt-get install -y --no-install-recommends bash git just ripgrep fd-find build-essential ca-certificates curl \
    && rm -rf /var/lib/apt/lists/*

# For python development
# Copy uv and uvx binaries directly from Astral's official image
COPY --from=ghcr.io/astral-sh/uv:python3.14-trixie /usr/local/bin/uv /usr/local/bin/uvx /usr/local/bin/
# Check copy was successful
RUN uv --version

ENV PI_ASK_USER_DISPLAY_MODE=inline \
    IN_CONTAINER=1 \
    UV_COMPILE_BYTECODE=1 \
    PYTHONUNBUFFERED=1

# Install pi.dev globally via npm
RUN npm install -g --ignore-scripts @earendil-works/pi-coding-agent \
    && pi --version
# ensure pi is up to date
RUN pi update

WORKDIR /workspace

# For python development
# Install python project dependencies
COPY pyproject.toml uv.lock ./
RUN uv sync --no-install-project

# Copy the rest of the project
COPY . .

# For python development
RUN uv sync
ENV PATH="/workspace/.venv/bin:/root/.local/bin:${PATH}"

CMD ["bash"]
