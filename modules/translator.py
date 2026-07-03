from Bio.Seq import Seq


def translate_contigs(records, table=1, stop_symbol="*"):
    """
    Translate each DNA contig into a protein sequence.

    Parameters
    ----------
    records : list
        List of SeqRecord objects.
    table : int
        NCBI genetic code table (default=1).
    stop_symbol : str
        Symbol used for stop codons.

    Returns
    -------
    list
        Translation results for each contig.
    """

    proteins = []

    for record in records:

        dna = Seq(str(record.seq))

        protein = str(
            dna.translate(
                table=table,
                stop_symbol=stop_symbol,
                to_stop=False
            )
        )

        proteins.append({

            "Contig": record.id,

            "DNA Length": len(dna),

            "Protein Length": len(protein),

            "Protein Sequence": protein,

            "Stop Codons": protein.count(stop_symbol)

        })

    return proteins


def translate_genome(records):
    """
    Translate the complete concatenated genome.
    """

    genome = ""

    for record in records:
        genome += str(record.seq)

    protein = str(Seq(genome).translate())

    return protein