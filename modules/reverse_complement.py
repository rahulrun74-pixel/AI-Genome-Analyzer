from Bio.Seq import Seq


def reverse_complement(records):
    """
    Generate reverse complement sequences for all contigs.

    Parameters
    ----------
    records : list
        List of SeqRecord objects.

    Returns
    -------
    list
        List containing reverse complement information.
    """

    reverse_sequences = []

    for record in records:

        rc_seq = str(Seq(str(record.seq)).reverse_complement())

        reverse_sequences.append({

            "Contig": record.id,

            "Length": len(record.seq),

            "Reverse Complement": rc_seq

        })

    return reverse_sequences


def genome_reverse_complement(records):
    """
    Generate reverse complement of the complete genome.
    """

    genome = "".join(str(record.seq) for record in records)

    rc = str(Seq(genome).reverse_complement())

    return rc