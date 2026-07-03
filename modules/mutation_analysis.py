"""
mutation_analysis.py

Detect SNPs, insertions, deletions and ambiguous bases
between two genome assemblies.
"""

from modules.utils import success, failure
from modules.fasta_reader import genome_sequence


def mutation_analysis(records_a, records_b):
    """
    Compare two genomes and summarize mutations.
    """

    try:

        if not records_a or not records_b:
            return failure("One or both genome datasets are empty.")

        genome_a = genome_sequence(records_a)
        genome_b = genome_sequence(records_b)

        len_a = len(genome_a)
        len_b = len(genome_b)

        compare_length = min(len_a, len_b)

        snps = 0
        ambiguous = 0

        mutation_positions = []

        for i in range(compare_length):

            base_a = genome_a[i]
            base_b = genome_b[i]

            if base_a == base_b:
                continue

            if base_a == "N" or base_b == "N":
                ambiguous += 1
            else:
                snps += 1

            mutation_positions.append({
                "Position": i + 1,
                "Genome A": base_a,
                "Genome B": base_b
            })

        if len_a > len_b:

            deletions = len_a - len_b
            insertions = 0

        elif len_b > len_a:

            insertions = len_b - len_a
            deletions = 0

        else:

            insertions = 0
            deletions = 0

        total = snps + insertions + deletions + ambiguous

        result = {

            "Genome A Length": len_a,

            "Genome B Length": len_b,

            "Compared Bases": compare_length,

            "SNPs": snps,

            "Insertions": insertions,

            "Deletions": deletions,

            "Ambiguous Bases": ambiguous,

            "Total Mutations": total,

            "Mutation Positions": mutation_positions

        }

        return success(
            result,
            "Mutation analysis completed successfully."
        )

    except Exception as e:

        return failure(str(e))