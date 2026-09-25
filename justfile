# Bookshelf Engine task runner.

set shell := ["bash", "-cu"]

image := "repodoc:latest"

# True when running inside the project container (set by the Dockerfile).
in_container := `[ "${IN_CONTAINER:-}" = "1" ] && echo 1 || echo 0`

# Base docker run: mount repo, remount .git read-only, work from it, clean up on exit.
docker_run := "docker run --rm -it -v \"$PWD\":/workspace -v \"$PWD/.git\":/workspace/.git:ro -w /workspace"

# Command fragments selected by execution context.
container_prefix := if in_container == "1" { "" } else { docker_run + " " + image + " " }
host_only_error  := if in_container == "1" { "echo 'error: run this on the host, not inside the container' >&2; exit 1" } else { "true" }
quiet_build_cmd  := if in_container == "1" { "true" } else { "docker build --quiet -t " + image + " . > /dev/null" }

# List available recipes.
default:
    @just --list

# Build the container image (host only).
build:
    @{{host_only_error}}
    @{{docker_run}} ghcr.io/astral-sh/uv:python3.14-trixie uv lock -U
    docker build -t {{image}} .

# Build the image quietly for use as a recipe dependency, don't build if already in the container.
_quiet-build:
    @{{quiet_build_cmd}}

# Start the container and run pi (host only).
pi *args: _quiet-build
    @{{host_only_error}}
    @op run --env-file="$HOME/ai.env" -- {{docker_run}} -v "$HOME/.pi/agent:/root/.pi/agent" -e OPENROUTER_API_KEY -e DEEPSEEK_API_KEY -e PI_TELEMETRY {{image}} pi {{args}}

# Drop into a bash prompt in the container (host only).
shell: _quiet-build
    @{{host_only_error}}
    @{{docker_run}} -v "$HOME/.pi/agent:/root/.pi/agent" {{image}} bash || [ $? -eq 130 ]

# Run the test suite with pytest.
test *args: _quiet-build
    @{{container_prefix}}uv run pytest {{args}}

# Apply fixes: format code and fix safe lint violations.
fix *args: _quiet-build
    @{{container_prefix}}uv run ruff format {{args}}
    @{{container_prefix}}uv run ruff check --fix {{args}}

# Verify: check formatting, lint, and types. Read-only; the definition of done gate.
check *args: _quiet-build
    @{{container_prefix}}uv run ruff format --check {{args}}
    @{{container_prefix}}uv run ruff check {{args}}
    @{{container_prefix}}uv run ty check {{args}}

# Remove the container image (host only).
clean:
    @{{host_only_error}}
    -docker image rm {{image}}
