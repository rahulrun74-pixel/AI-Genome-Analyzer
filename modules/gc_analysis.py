"""
gc_analysis.py

Calculate GC and AT content for genome assemblies.
"""

from modules.utils import success, failure


def calculate_gc(sequence):
    """
    Calculate GC percentage for a DNA sequence.
    """

    sequence = sequence.upper()

    if len(sequence) == 0:
        return 0.0

    g = sequence.count("G")
    c = sequence.count("C")

    return round(((g + c) / len(sequence)) * 100, 2)


def calculate_at(sequence):
    """
    Calculate AT percentage for a DNA sequence.
    """

    sequence = sequence.upper()

    if len(sequence) == 0:
        return 0.0

    a = sequence.count("A")
    t = sequence.count("T")

    return round(((a + t) / len(sequence)) * 100, 2)


def gc_analysis(records):
    """
    Perform GC analysis on all contigs.
    """

    try:

        if not records:
            return failure("No sequences available.")

        genome = "".join(str(r.seq).upper() for r in records)

        overall_gc = calculate_gc(genome)
        overall_at = calculate_at(genome)

        contig_gc = []

        for record in records:

            gc = calculate_gc(str(record.seq))

            contig_gc.append({

                "Contig": record.id,

                "Length": len(record.seq),

                "GC (%)": gc

            })

        # Classification

        if overall_gc < 40:
            genome_type = "AT-rich"

        elif overall_gc <= 60:
            genome_type = "Balanced"

        else:
            genome_type = "GC-rich"

        result = {

            "Overall GC (%)": overall_gc,

            "Overall AT (%)": overall_at,

            "Genome Type": genome_type,

            "Contig GC": contig_gc

        }

        return success(
            result,
            "GC analysis completed successfully."
        )

    except Exception as e:

        return failure(str(e))