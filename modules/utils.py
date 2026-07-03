"""
utils.py

Common helper functions used throughout the
AI Genome Comparative Analyzer.
"""

from datetime import datetime
from pathlib import Path


SUPPORTED_EXTENSIONS = {".fna", ".fa", ".fasta"}


def success(data, message="Success"):
    """
    Standard success response.
    """
    return {
        "success": True,
        "message": message,
        "data": data
    }


def failure(message):
    """
    Standard error response.
    """
    return {
        "success": False,
        "message": message,
        "data": None
    }


def format_number(number):
    """
    Format integers with commas.
    """

    try:
        return f"{int(number):,}"
    except Exception:
        return str(number)


def genome_size(size):
    """
    Convert bp into human readable units.
    """

    if size >= 1_000_000_000:
        return f"{size/1_000_000_000:.2f} Gb"

    if size >= 1_000_000:
        return f"{size/1_000_000:.2f} Mb"

    if size >= 1_000:
        return f"{size/1_000:.2f} Kb"

    return f"{size} bp"


def percentage(value, total):
    """
    Calculate percentage.
    """

    if total == 0:
        return 0.0

    return round((value / total) * 100, 2)


def current_timestamp():
    """
    Current date and time.
    """

    return datetime.now().strftime("%d-%m-%Y %H:%M:%S")


def validate_extension(filename):
    """
    Check supported FASTA extension.
    """

    extension = Path(filename).suffix.lower()

    return extension in SUPPORTED_EXTENSIONS


def validate_dna(sequence):
    """
    Check DNA contains valid bases.
    """

    valid = set("ATGCN")

    sequence = sequence.upper()

    return all(base in valid for base in sequence)


def safe_division(a, b):
    """
    Divide safely.
    """

    if b == 0:
        return 0

    return a / b


def calculate_n50(lengths):
    """
    Calculate assembly N50.
    """

    if not lengths:
        return 0

    lengths = sorted(lengths, reverse=True)

    total = sum(lengths)

    cumulative = 0

    for length in lengths:

        cumulative += length

        if cumulative >= total / 2:
            return length

    return 0