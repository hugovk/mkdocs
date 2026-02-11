"""Minimal test suite for MkDocs handlers configuration."""

import pytest
from src.mkdocs.mkdocs import MkDocs, Directory, Package


def test_mkdocs_init_without_handlers():
    """Test that MkDocs can be instantiated without handlers."""
    m = MkDocs()
    assert m.handlers is None


def test_mkdocs_init_with_handlers():
    """Test that MkDocs can be instantiated with custom handlers."""
    handlers = [Directory('docs')]
    m = MkDocs(handlers=handlers)
    assert m.handlers == handlers


def test_mkdocs_init_with_multiple_handlers():
    """Test that MkDocs can be instantiated with multiple handlers."""
    handlers = [Package('mkdocs:theme'), Directory('docs')]
    m = MkDocs(handlers=handlers)
    assert m.handlers == handlers
    assert len(m.handlers) == 2
