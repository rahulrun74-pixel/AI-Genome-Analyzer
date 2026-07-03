"""
protein_analysis.py

Translate DNA sequences into proteins and generate
protein statistics.
"""

from Bio.Seq import Seq

from modules.utils import success, failure


def translate_sequence(sequence):
    """
    Translate a DNA sequence into protein.
    """

    sequence = sequence.upper()

    usable_length = len(sequence) - (len(sequence) % 3)

    sequence = sequence[:usable_length]

    protein = str(
        Seq(sequence).translate(
            table=1,
            stop_symbol="*",
            to_stop=False
        )
    )

    return protein


def protein_analysis(records):
    """
    Translate all contigs and calculate statistics.
    """

    try:

        if not records:
            return failure("No sequences available.")

        proteins = []

        total_dna = 0
        total_protein = 0
        total_stop = 0

        for record in records:

            dna = str(record.seq)

            protein = translate_sequence(dna)

            stop_codons = protein.count("*")

            proteins.append({

                "Contig": record.id,

                "DNA Length": len(dna),

                "Protein Length": len(protein),

                "Stop Codons": stop_codons,

                "Protein Sequence": protein

            })

            total_dna += len(dna)
            total_protein += len(protein)
            total_stop += stop_codons

        result = {

            "Number of Proteins": len(proteins),

            "Total DNA Length": total_dna,

            "Total Protein Length": total_protein,

            "Total Stop Codons": total_stop,

            "Proteins": proteins

        }

        return success(
            result,
            "Protein analysis completed successfully."
        )

    except Exception as e:

        return failure(str(e))