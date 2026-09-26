"""Smoke test: the package is importable."""

import repodoc


def test_package_imports() -> None:
    """Importing repodoc succeeds."""
    assert repodoc.__doc__
