"""
fasta_reader.py

Reads FASTA/FA/FNA genome files.
Supports Streamlit uploads and local files.
"""

from io import StringIO
from Bio import SeqIO

from modules.utils import (
    success,
    failure,
    validate_dna,
)


def read_fasta(file):
    """
    Read a FASTA/FNA/FA file.

    Parameters
    ----------
    file : UploadedFile or str

    Returns
    -------
    dict
    """

    try:

        # -------------------------
        # Streamlit Uploaded File
        # -------------------------
        if hasattr(file, "getvalue"):

            content = file.getvalue().decode("utf-8")

            handle = StringIO(content)

        # -------------------------
        # Local File
        # -------------------------
        else:

            handle = open(file, "r", encoding="utf-8")

        records = list(SeqIO.parse(handle, "fasta"))

        handle.close()

        if len(records) == 0:

            return failure("No sequences found.")

        # Validate DNA

        for record in records:

            if not validate_dna(str(record.seq)):

                return failure(
                    f"Invalid DNA bases detected in {record.id}"
                )

        return success(
            records,
            f"{len(records)} sequences loaded successfully."
        )

    except Exception as e:

        return failure(str(e))


def genome_sequence(records):
    """
    Concatenate all contigs.
    """

    return "".join(str(r.seq).upper() for r in records)


def sequence_lengths(records):

    return [len(r.seq) for r in records]


def sequence_headers(records):

    return [r.id for r in records]


def number_of_contigs(records):

    return len(records)