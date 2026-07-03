"""
genome_stats.py

Calculate assembly statistics for a genome.
"""

from modules.utils import (
    success,
    failure,
    calculate_n50,
)


def genome_statistics(records):
    """
    Calculate genome assembly statistics.

    Parameters
    ----------
    records : list of SeqRecord

    Returns
    -------
    dict
    """

    try:

        if not records:
            return failure("No sequences available.")

        lengths = [len(record.seq) for record in records]

        genome_size = sum(lengths)

        contigs = len(lengths)

        largest = max(lengths)

        smallest = min(lengths)

        average = round(genome_size / contigs, 2)

        n50 = calculate_n50(lengths)

        # -----------------------------
        # Simple Assembly Quality
        # -----------------------------

        if contigs == 1:
            quality = "Complete Genome"

        elif contigs <= 10:
            quality = "High-quality Draft"

        elif contigs <= 100:
            quality = "Draft Genome"

        else:
            quality = "Fragmented Assembly"

        result = {

            "Genome Size": genome_size,

            "Contigs": contigs,

            "Largest Contig": largest,

            "Smallest Contig": smallest,

            "Average Contig Length": average,

            "N50": n50,

            "Assembly Quality": quality

        }

        return success(
            result,
            "Genome statistics calculated successfully."
        )

    except Exception as e:

        return failure(str(e))