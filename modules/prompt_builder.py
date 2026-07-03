import json


def build_prompt(
    genome_stats,
    gc_summary,
    alignment,
    mutation_summary,
    codon_summary
):
    """
    Convert analysis results into an LLM prompt.
    """

    analysis = {

        "Genome Statistics": genome_stats,

        "GC Analysis": gc_summary,

        "Alignment": alignment,

        "Mutation Summary": mutation_summary,

        "Codon Usage": codon_summary

    }

    prompt = f"""
You are a professional computational biologist.

Below is the result of a comparative genome analysis.

{json.dumps(analysis, indent=4)}

Write a scientific report including:

1. Genome overview
2. Assembly quality
3. GC analysis
4. Comparative genomics
5. Mutation significance
6. Codon usage interpretation
7. Biological implications
8. Research conclusion

Write in professional publication style.
"""

    return prompt