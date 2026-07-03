from Bio.SeqUtils import gc_fraction


def overall_gc(records):
    """
    Calculate overall GC content of the genome.
    """

    sequence = "".join(str(record.seq).upper() for record in records)

    return round(gc_fraction(sequence) * 100, 2)


def contig_gc(records):
    """
    Calculate GC content for each contig.
    """

    results = []

    for record in records:

        gc = round(gc_fraction(record.seq) * 100, 2)

        results.append({
            "Contig": record.id,
            "Length": len(record.seq),
            "GC": gc
        })

    return results


def sliding_window_gc(sequence, window_size=1000):
    """
    Calculate GC content in sliding windows.

    Parameters
    ----------
    sequence : str
    window_size : int

    Returns
    -------
    list
    """

    sequence = str(sequence).upper()

    windows = []

    for i in range(0, len(sequence), window_size):

        fragment = sequence[i:i + window_size]

        if len(fragment) == 0:
            continue

        gc = round(gc_fraction(fragment) * 100, 2)

        windows.append({

            "Start": i + 1,

            "End": i + len(fragment),

            "GC": gc

        })

    return windows


def gc_summary(records):
    """
    Generate complete GC analysis.
    """

    overall = overall_gc(records)

    contigs = contig_gc(records)

    genome = "".join(str(r.seq) for r in records)

    windows = sliding_window_gc(genome)

    highest = max(windows, key=lambda x: x["GC"])

    lowest = min(windows, key=lambda x: x["GC"])

    return {

        "Overall GC": overall,

        "Contigs": contigs,

        "Sliding Windows": windows,

        "Highest GC Region": highest,

        "Lowest GC Region": lowest

    }