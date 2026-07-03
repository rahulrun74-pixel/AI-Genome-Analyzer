from itertools import zip_longest


def get_genome_sequence(records):
    """
    Combine all contigs into a single uppercase genome sequence.
    """

    return "".join(str(record.seq).upper() for record in records)


def compare_genomes(records1, records2):
    """
    Compare two genome sequences and calculate alignment statistics.

    Parameters
    ----------
    records1 : list
    records2 : list

    Returns
    -------
    dict
    """

    seq1 = get_genome_sequence(records1)
    seq2 = get_genome_sequence(records2)

    matches = 0
    mismatches = 0
    ambiguous = 0

    for a, b in zip_longest(seq1, seq2, fillvalue="-"):

        if a == "-" or b == "-":
            continue

        if a == "N" or b == "N":
            ambiguous += 1
            continue

        if a == b:
            matches += 1
        else:
            mismatches += 1

    compared = matches + mismatches

    similarity = (
        round(matches / compared * 100, 2)
        if compared > 0 else 0
    )

    insertions_deletions = abs(len(seq1) - len(seq2))

    return {

        "Genome A Length": len(seq1),

        "Genome B Length": len(seq2),

        "Compared Bases": compared,

        "Matches": matches,

        "Mismatches": mismatches,

        "Ambiguous Bases": ambiguous,

        "Similarity (%)": similarity,

        "Estimated Indels": insertions_deletions

    }