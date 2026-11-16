"""Parsers turn raw config files into the normalized model."""


class ParseError(Exception):
    """Raised when a discovered file cannot be read as its expected format."""
