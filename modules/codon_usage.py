"""
codon_usage.py

Analyze codon usage and amino acid frequencies.
"""

from collections import Counter

from modules.utils import success, failure
from modules.fasta_reader import genome_sequence


GENETIC_CODE = {
    "TTT":"F","TTC":"F","TTA":"L","TTG":"L",
    "CTT":"L","CTC":"L","CTA":"L","CTG":"L",
    "ATT":"I","ATC":"I","ATA":"I","ATG":"M",
    "GTT":"V","GTC":"V","GTA":"V","GTG":"V",

    "TCT":"S","TCC":"S","TCA":"S","TCG":"S",
    "CCT":"P","CCC":"P","CCA":"P","CCG":"P",
    "ACT":"T","ACC":"T","ACA":"T","ACG":"T",
    "GCT":"A","GCC":"A","GCA":"A","GCG":"A",

    "TAT":"Y","TAC":"Y","TAA":"*","TAG":"*",
    "CAT":"H","CAC":"H","CAA":"Q","CAG":"Q",
    "AAT":"N","AAC":"N","AAA":"K","AAG":"K",
    "GAT":"D","GAC":"D","GAA":"E","GAG":"E",

    "TGT":"C","TGC":"C","TGA":"*","TGG":"W",
    "CGT":"R","CGC":"R","CGA":"R","CGG":"R",
    "AGT":"S","AGC":"S","AGA":"R","AGG":"R",
    "GGT":"G","GGC":"G","GGA":"G","GGG":"G"
}


def codon_usage(records):
    """
    Calculate codon usage statistics.
    """

    try:

        if not records:
            return failure("No sequences available.")

        genome = genome_sequence(records)

        usable_length = len(genome) - (len(genome) % 3)

        genome = genome[:usable_length]

        codons = []

        for i in range(0, len(genome), 3):

            codon = genome[i:i+3]

            if "N" in codon:
                continue

            codons.append(codon)

        codon_counter = Counter(codons)

        amino_counter = Counter()

        for codon, count in codon_counter.items():

            aa = GENETIC_CODE.get(codon, "X")

            amino_counter[aa] += count

        total_codons = sum(codon_counter.values())

        codon_frequency = []

        for codon in sorted(codon_counter):

            count = codon_counter[codon]

            codon_frequency.append({

                "Codon": codon,

                "Count": count,

                "Frequency (%)": round(
                    count * 100 / total_codons,
                    4
                )

            })

        amino_frequency = []

        total_amino = sum(amino_counter.values())

        for aa in sorted(amino_counter):

            count = amino_counter[aa]

            amino_frequency.append({

                "Amino Acid": aa,

                "Count": count,

                "Frequency (%)": round(
                    count * 100 / total_amino,
                    4
                )

            })

        most_common = codon_counter.most_common(10)

        least_common = sorted(
            codon_counter.items(),
            key=lambda x: x[1]
        )[:10]

        result = {

            "Total Codons": total_codons,

            "Unique Codons": len(codon_counter),

            "Most Common Codons": most_common,

            "Least Common Codons": least_common,

            "Codon Frequency": codon_frequency,

            "Amino Acid Frequency": amino_frequency

        }

        return success(
            result,
            "Codon usage analysis completed successfully."
        )

    except Exception as e:

        return failure(str(e))