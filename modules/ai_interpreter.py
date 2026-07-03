"""
ai_interpreter.py

Generate a scientific interpretation of genome analysis results.
Works offline (rule-based) and can later be replaced by an LLM.
"""

from modules.utils import success, failure


def generate_ai_report(
    genome_stats,
    gc_analysis,
    genome_compare,
    mutation_analysis,
    protein_analysis,
    codon_usage
):
    """
    Generate a biological interpretation.
    """

    try:

        report = []

        # ============================================
        # Genome Statistics
        # ============================================

        stats = genome_stats["data"]

        report.append("# Genome Statistics\n")

        report.append(
            f"The uploaded genome assembly contains "
            f"{stats['Genome Size']:,} base pairs distributed across "
            f"{stats['Contigs']} contig(s). "
            f"The calculated N50 is {stats['N50']:,} bp, "
            f"indicating an assembly quality classified as "
            f"{stats['Assembly Quality']}."
        )

        # ============================================
        # GC Content
        # ============================================

        gc = gc_analysis["data"]

        report.append("\n# GC Content\n")

        report.append(
            f"The overall GC content is "
            f"{gc['Overall GC (%)']}%, while "
            f"AT content is {gc['Overall AT (%)']}%. "
            f"The genome is classified as "
            f"{gc['Genome Type']}."
        )

        # ============================================
        # Genome Comparison
        # ============================================

        cmp = genome_compare["data"]

        report.append("\n# Comparative Analysis\n")

        report.append(
            f"The two genomes share "
            f"{cmp['Similarity (%)']}% sequence identity "
            f"and are classified as "
            f"{cmp['Relationship']}."
        )

        # ============================================
        # Mutation Analysis
        # ============================================

        mut = mutation_analysis["data"]

        report.append("\n# Mutation Analysis\n")

        report.append(
            f"The comparison detected "
            f"{mut['SNPs']:,} SNPs, "
            f"{mut['Insertions']} insertions, "
            f"{mut['Deletions']} deletions and "
            f"{mut['Ambiguous Bases']} ambiguous positions."
        )

        if mut["Total Mutations"] < 100:

            report.append(
                "Very few mutations were observed, suggesting a highly conserved genome."
            )

        elif mut["Total Mutations"] < 10000:

            report.append(
                "The mutation profile is consistent with normal strain-level variation."
            )

        else:

            report.append(
                "The genomes show substantial divergence with a large number of detected mutations."
            )

        # ============================================
        # Protein Analysis
        # ============================================

        protein = protein_analysis["data"]

        report.append("\n# Protein Translation\n")

        report.append(
            f"The translated genome produced "
            f"{protein['Number of Proteins']} protein sequence(s) "
            f"with a combined protein length of "
            f"{protein['Total Protein Length']:,} amino acids."
        )

        # ============================================
        # Codon Usage
        # ============================================

        codon = codon_usage["data"]

        common = ", ".join(
            [c for c, n in codon["Most Common Codons"][:5]]
        )

        report.append("\n# Codon Usage\n")

        report.append(
            f"The genome contains "
            f"{codon['Total Codons']:,} codons. "
            f"The most abundant codons are "
            f"{common}, indicating codon usage bias."
        )

        # ============================================
        # Biological Summary
        # ============================================

        report.append("\n# Biological Interpretation\n")

        if cmp["Similarity (%)"] >= 99:

            relation = (
                "The genomes are almost identical and "
                "likely represent closely related isolates."
            )

        elif cmp["Similarity (%)"] >= 95:

            relation = (
                "The genomes are highly related but "
                "contain measurable evolutionary differences."
            )

        else:

            relation = (
                "The genomes display substantial evolutionary divergence."
            )

        report.append(relation)

        report.append(
            "Overall, the assembly quality, GC content, mutation profile, "
            "protein translation and codon usage collectively indicate "
            "a biologically consistent genome suitable for downstream "
            "comparative genomics and functional annotation."
        )

        report.append(
            "Future analyses such as gene prediction, BLAST annotation, "
            "KEGG pathway mapping and phylogenetic reconstruction would "
            "provide deeper biological insight."
        )

        return success(
            "\n\n".join(report),
            "AI interpretation generated successfully."
        )

    except Exception as e:

        return failure(str(e))