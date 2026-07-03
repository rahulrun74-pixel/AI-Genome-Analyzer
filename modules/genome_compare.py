"""
genome_compare.py

Simple comparative analysis between two genomes.
"""

from modules.utils import success, failure
from modules.fasta_reader import genome_sequence


def compare_genomes(records_a, records_b):
    """
    Compare two genome assemblies.

    Parameters
    ----------
    records_a : list of SeqRecord
    records_b : list of SeqRecord

    Returns
    -------
    dict
    """

    try:

        if not records_a or not records_b:
            return failure("One or both genome datasets are empty.")

        genome_a = genome_sequence(records_a)
        genome_b = genome_sequence(records_b)

        len_a = len(genome_a)
        len_b = len(genome_b)

        compare_length = min(len_a, len_b)

        matches = 0
        mismatches = 0

        for i in range(compare_length):

            if genome_a[i] == genome_b[i]:
                matches += 1
            else:
                mismatches += 1

        similarity = round((matches / compare_length) * 100, 2)

        length_difference = abs(len_a - len_b)

        if similarity >= 99:
            relation = "Nearly Identical"

        elif similarity >= 95:
            relation = "Highly Similar"

        elif similarity >= 90:
            relation = "Closely Related"

        elif similarity >= 80:
            relation = "Moderately Similar"

        else:
            relation = "Distantly Related"

        result = {

            "Genome A Length": len_a,

            "Genome B Length": len_b,

            "Compared Bases": compare_length,

            "Matches": matches,

            "Mismatches": mismatches,

            "Similarity (%)": similarity,

            "Length Difference": length_difference,

            "Relationship": relation

        }

        return success(
            result,
            "Genome comparison completed successfully."
        )

    except Exception as e:

        return failure(str(e))