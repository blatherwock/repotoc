# Bookshelf Engine task runner.

set shell := ["bash", "-cu"]

image := "repotoc:latest"

# True when running inside the project container (set by the Dockerfile).
in_container := `[ "${IN_CONTAINER:-}" = "1" ] && echo 1 || echo 0`

# Base docker run: mount repo, remount .git read-only, work from it, clean up on
# exit. Non-interactive so commit hooks and other no-tty callers can use it;
# recipes needing a terminal add -it themselves.
docker_run := "docker run --rm -v \"$PWD\":/workspace -v \"$PWD/.git\":/workspace/.git:ro -w /workspace"

# Command fragments selected by execution context.
container_prefix := if in_container == "1" { "" } else { docker_run + " " + image + " " }
host_only_error  := if in_container == "1" { "echo 'error: run this on the host, not inside the container' >&2; exit 1" } else { "true" }
require_image    := if in_container == "1" { "true" } else { "docker image inspect " + image + " > /dev/null 2>&1 || { echo 'error: image " + image + " not found; run `just build` first' >&2; exit 1; }" }

# The package's Python floor (requires-python), tested alongside the dev interpreter.
floor_python := "3.11"

# List available recipes.
default:
    @just --list

# Build the container image (host only).
build:
    @{{host_only_error}}
    @{{docker_run}} ghcr.io/astral-sh/uv:python3.14-trixie uv lock -U
    docker build --pull --no-cache -t {{image}} .

# Verify the image exists for use as a recipe dependency; hint to build if missing (no-op in container).
_require-image:
    @{{require_image}}

# Start the container and run pi (host only).
pi *args: _require-image
    @{{host_only_error}}
    @op run --env-file="$HOME/ai.env" -- {{docker_run}} -it -v "$HOME/.pi/agent:/root/.pi/agent" -e OPENROUTER_API_KEY -e DEEPSEEK_API_KEY -e PI_TELEMETRY {{image}} pi {{args}}

# Drop into a bash prompt in the container (host only).
shell: _require-image
    @{{host_only_error}}
    @{{docker_run}} -it -v "$HOME/.pi/agent:/root/.pi/agent" {{image}} bash || [ $? -eq 130 ]

# Run the test suite with pytest on the dev Python (coverage gate) and on the
# floor Python (pass-only; the version-guarded branch cannot be covered there).
test *args: _require-image
    @echo "== dev python (3.14): coverage gate =="
    @{{container_prefix}}uv run pytest {{args}}
    @echo "== floor python ({{floor_python}}): pass-only =="
    @{{container_prefix}}env UV_PROJECT_ENVIRONMENT=.venv-{{floor_python}} uv run --python {{floor_python}} pytest --no-cov -q {{args}}

# Apply fixes: format code, fix safe lint violations, and regenerate the docs artifact.
fix *args: _require-image
    @{{container_prefix}}uv run ruff format {{args}}
    @{{container_prefix}}uv run ruff check --fix {{args}}
    @{{container_prefix}}uv run repotoc
    @{{container_prefix}}uv run python src/tools/site_build.py refresh

# Verify: check formatting, lint, types, and doc freshness. Read-only; the definition of done gate.
check *args: _require-image
    @{{container_prefix}}uv run ruff format --check {{args}}
    @{{container_prefix}}uv run ruff check {{args}}
    @{{container_prefix}}uv run ty check {{args}}
    @{{container_prefix}}uv run repotoc --check
    @{{container_prefix}}uv run python src/tools/site_build.py check

# Remove the container image (host only).
clean:
    @{{host_only_error}}
    -docker image rm {{image}}

# Serve the showcase site on http://127.0.0.1:8000 (host only).
site: _require-image
    @{{host_only_error}}
    @{{docker_run}} -it -p 127.0.0.1:8000:8000 {{image}} python3 -m http.server 8000 --directory site

# Regenerate the site example variants and embed them in the page.
site-examples: _require-image
    @{{container_prefix}}uv run python src/tools/site_build.py refresh

# Install the git hooks via pre-commit (host only).
hooks:
    @{{host_only_error}}
    uvx pre-commit install
