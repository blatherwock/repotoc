"""Smoke test: the package is importable."""

import repotoc


def test_package_imports() -> None:
    """Importing repotoc succeeds."""
    assert repotoc.__doc__
