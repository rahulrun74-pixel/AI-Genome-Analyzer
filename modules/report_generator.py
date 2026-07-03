"""
report_generator.py

Generate a professional PDF report for the
AI Genome Analyzer.
"""

import os
from datetime import datetime

from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)
from reportlab.lib import colors

from modules.utils import success, failure


def generate_report(
    filename,
    genome_stats,
    gc_analysis,
    genome_compare,
    mutation_analysis,
    protein_analysis,
    codon_usage,
    ai_report
):
    """
    Generate a PDF report.
    """

    try:

        os.makedirs("reports", exist_ok=True)

        filepath = os.path.join("reports", filename)

        doc = SimpleDocTemplate(filepath)

        styles = getSampleStyleSheet()

        story = []

        # ==========================================
        # Title
        # ==========================================

        story.append(
            Paragraph(
                "<b><font size=22>AI Genome Analysis Report</font></b>",
                styles["Title"]
            )
        )

        story.append(Spacer(1, 0.3 * inch))

        story.append(
            Paragraph(
                f"Generated on: {datetime.now()}",
                styles["Normal"]
            )
        )

        story.append(Spacer(1, 0.3 * inch))

        # ==========================================
        # Genome Statistics
        # ==========================================

        story.append(
            Paragraph("<b>Genome Statistics</b>", styles["Heading2"])
        )

        stats = genome_stats["data"]

        table = Table([
            ["Parameter", "Value"],
            ["Genome Size", str(stats["Genome Size"])],
            ["Contigs", str(stats["Contigs"])],
            ["Largest Contig", str(stats["Largest Contig"])],
            ["Smallest Contig", str(stats["Smallest Contig"])],
            ["Average Length", str(stats["Average Contig Length"])],
            ["N50", str(stats["N50"])],
            ["Assembly", stats["Assembly Quality"]]
        ])

        table.setStyle(TableStyle([

            ("BACKGROUND", (0,0), (-1,0), colors.darkblue),

            ("TEXTCOLOR", (0,0), (-1,0), colors.white),

            ("GRID", (0,0), (-1,-1), 1, colors.black),

            ("BACKGROUND", (0,1), (-1,-1), colors.beige),

            ("BOTTOMPADDING", (0,0), (-1,0), 10)

        ]))

        story.append(table)

        story.append(Spacer(1, 0.3 * inch))

        # ==========================================
        # GC Analysis
        # ==========================================

        gc = gc_analysis["data"]

        story.append(
            Paragraph("<b>GC Analysis</b>", styles["Heading2"])
        )

        story.append(
            Paragraph(
                f"GC Content : {gc['Overall GC (%)']} %",
                styles["Normal"]
            )
        )

        story.append(
            Paragraph(
                f"AT Content : {gc['Overall AT (%)']} %",
                styles["Normal"]
            )
        )

        story.append(
            Paragraph(
                f"Genome Type : {gc['Genome Type']}",
                styles["Normal"]
            )
        )

        story.append(Spacer(1, 0.2 * inch))

        # ==========================================
        # Genome Comparison
        # ==========================================

        cmp = genome_compare["data"]

        story.append(
            Paragraph("<b>Genome Comparison</b>", styles["Heading2"])
        )

        story.append(
            Paragraph(
                f"Similarity : {cmp['Similarity (%)']} %",
                styles["Normal"]
            )
        )

        story.append(
            Paragraph(
                f"Relationship : {cmp['Relationship']}",
                styles["Normal"]
            )
        )

        story.append(Spacer(1, 0.2 * inch))

        # ==========================================
        # Mutation Summary
        # ==========================================

        mut = mutation_analysis["data"]

        story.append(
            Paragraph("<b>Mutation Summary</b>", styles["Heading2"])
        )

        mutation_table = Table([
            ["Type", "Count"],
            ["SNPs", mut["SNPs"]],
            ["Insertions", mut["Insertions"]],
            ["Deletions", mut["Deletions"]],
            ["Ambiguous", mut["Ambiguous Bases"]],
            ["Total", mut["Total Mutations"]]
        ])

        mutation_table.setStyle(TableStyle([

            ("BACKGROUND", (0,0), (-1,0), colors.green),

            ("TEXTCOLOR", (0,0), (-1,0), colors.white),

            ("GRID", (0,0), (-1,-1), 1, colors.black),

            ("BACKGROUND", (0,1), (-1,-1), colors.whitesmoke)

        ]))

        story.append(mutation_table)

        story.append(Spacer(1, 0.3 * inch))

        # ==========================================
        # Protein
        # ==========================================

        protein = protein_analysis["data"]

        story.append(
            Paragraph("<b>Protein Summary</b>", styles["Heading2"])
        )

        story.append(
            Paragraph(
                f"Translated Proteins : {protein['Number of Proteins']}",
                styles["Normal"]
            )
        )

        story.append(
            Paragraph(
                f"Protein Length : {protein['Total Protein Length']}",
                styles["Normal"]
            )
        )

        story.append(Spacer(1, 0.3 * inch))

        # ==========================================
        # Codon Usage
        # ==========================================

        codon = codon_usage["data"]

        story.append(
            Paragraph("<b>Codon Usage</b>", styles["Heading2"])
        )

        story.append(
            Paragraph(
                f"Total Codons : {codon['Total Codons']}",
                styles["Normal"]
            )
        )

        story.append(
            Paragraph(
                f"Unique Codons : {codon['Unique Codons']}",
                styles["Normal"]
            )
        )

        story.append(Spacer(1, 0.3 * inch))

        # ==========================================
        # AI Report
        # ==========================================

        story.append(
            Paragraph("<b>AI Interpretation</b>", styles["Heading2"])
        )

        paragraphs = ai_report["data"].split("\n")

        for p in paragraphs:

            if p.strip():

                story.append(
                    Paragraph(p, styles["Normal"])
                )

        doc.build(story)

        return success(
            filepath,
            "PDF report generated successfully."
        )

    except Exception as e:

        return failure(str(e))