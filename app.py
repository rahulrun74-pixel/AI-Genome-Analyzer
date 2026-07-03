import streamlit as st
import pandas as pd
import plotly.express as px
import json

# -------------------------------
# Import Modules
# -------------------------------

from modules.fasta_reader import read_fasta
from modules.genome_stats import genome_statistics
from modules.gc_analysis import gc_analysis
from modules.genome_compare import compare_genomes
from modules.mutation_analysis import mutation_analysis
from modules.protein_analysis import protein_analysis
from modules.codon_usage import codon_usage
from modules.ai_interpreter import generate_ai_report
from modules.report_generator import generate_report

# -------------------------------
# Page Configuration
# -------------------------------

st.set_page_config(
    page_title="AI Genome Comparative Analyzer",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------------------------
# Custom CSS
# -------------------------------

st.markdown("""
<style>

.main{
    padding-top:20px;
}

.metric-container{
    background:#f7f7f7;
    padding:15px;
    border-radius:10px;
}

h1,h2,h3{
    color:#2E86C1;
}

</style>
""", unsafe_allow_html=True)

# -------------------------------
# Sidebar
# -------------------------------

st.sidebar.title("🧬 AI Genome Analyzer")

st.sidebar.info("""
Upload two genome FASTA/FNA files.

The application will perform:

• Genome Statistics

• GC Analysis

• Genome Comparison

• Mutation Detection

• Protein Translation

• Codon Usage

• AI Interpretation

• PDF Report Generation
""")

st.sidebar.success("Version 2.0")

# -------------------------------
# Title
# -------------------------------

st.title("🧬 AI Genome Comparative Analyzer")

st.write(
    "Compare two genomes using integrated bioinformatics "
    "analysis and AI-assisted biological interpretation."
)

# -------------------------------
# Upload Section
# -------------------------------

col1, col2 = st.columns(2)

with col1:

    genome_file1 = st.file_uploader(
        "Upload Genome A",
        type=["fna", "fa", "fasta"],
        key="genomeA"
    )

with col2:

    genome_file2 = st.file_uploader(
        "Upload Genome B",
        type=["fna", "fa", "fasta"],
        key="genomeB"
    )

# -------------------------------
# Wait for Files
# -------------------------------

if genome_file1 is None or genome_file2 is None:

    st.warning("Please upload both genome files.")

    st.stop()

# -------------------------------
# Load Files
# -------------------------------

with st.spinner("Reading genome files..."):

    result1 = read_fasta(genome_file1)
    result2 = read_fasta(genome_file2)

if not result1["success"]:

    st.error(result1["message"])

    st.stop()

if not result2["success"]:

    st.error(result2["message"])

    st.stop()

records1 = result1["data"]
records2 = result2["data"]

st.success("✅ Both genome files loaded successfully.")

# -------------------------------
# Placeholder
# -------------------------------

st.info(
    "Files loaded successfully.\n\n"
    "Next we will perform genome analysis."
)


st.success("✅ Both genome files loaded successfully.")

# ==========================================
# Run Analysis Pipeline
# ==========================================

with st.spinner("Running genome analysis..."):

    # Genome Statistics
    stats1 = genome_statistics(records1)
    stats2 = genome_statistics(records2)

    # GC Analysis
    gc1 = gc_analysis(records1)
    gc2 = gc_analysis(records2)

    # Genome Comparison
    comparison = compare_genomes(records1, records2)

    # Mutation Analysis
    mutations = mutation_analysis(records1, records2)

    # Protein Analysis
    protein1 = protein_analysis(records1)

    # Codon Usage
    codons1 = codon_usage(records1)

    # AI Interpretation
    ai_report = generate_ai_report(
        stats1,
        gc1,
        comparison,
        mutations,
        protein1,
        codons1
    )

st.success("✅ Analysis completed successfully!")

st.header("Genome Summary")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Genome Size",
        f"{stats1['data']['Genome Size']:,} bp"
    )

with col2:
    st.metric(
        "GC %",
        f"{gc1['data']['Overall GC (%)']} %"
    )

with col3:
    st.metric(
        "Similarity",
        f"{comparison['data']['Similarity (%)']} %"
    )

st.divider()

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Genome Statistics",
    "🧬 GC Analysis",
    "🔬 Genome Comparison",
    "🧬 Protein & Codons",
    "🤖 AI Report"
])

with tab1:

    st.subheader("Genome A Statistics")

    st.dataframe(pd.DataFrame(
        stats1["data"].items(),
        columns=["Parameter", "Value"]
    ))

    st.subheader("Genome B Statistics")

    st.dataframe(pd.DataFrame(
        stats2["data"].items(),
        columns=["Parameter", "Value"]
    ))

with tab2:

    st.subheader("GC Content")

    gc_df = pd.DataFrame({
        "Genome": ["Genome A", "Genome B"],
        "GC %": [
            gc1["data"]["Overall GC (%)"],
            gc2["data"]["Overall GC (%)"]
        ]
    })

    fig = px.bar(
        gc_df,
        x="Genome",
        y="GC %",
        text="GC %",
        title="GC Content Comparison"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.dataframe(gc_df)

with tab3:

    st.subheader("Comparison Summary")

    st.dataframe(pd.DataFrame(
        comparison["data"].items(),
        columns=["Metric", "Value"]
    ))

    st.subheader("Mutation Summary")

    mutation_df = pd.DataFrame({
        "Type": [
            "SNPs",
            "Insertions",
            "Deletions",
            "Ambiguous"
        ],
        "Count": [
            mutations["data"]["SNPs"],
            mutations["data"]["Insertions"],
            mutations["data"]["Deletions"],
            mutations["data"]["Ambiguous Bases"]
        ]
    })

    fig = px.pie(
        mutation_df,
        names="Type",
        values="Count",
        title="Mutation Distribution"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.dataframe(mutation_df)

with tab4:

    st.subheader("Protein Summary")

    st.write(
        f"Translated Proteins: {protein1['data']['Number of Proteins']}"
    )

    st.write(
        f"Protein Length: {protein1['data']['Total Protein Length']:,}"
    )

    st.subheader("Top Codons")

    codon_df = pd.DataFrame(
        codons1["data"]["Most Common Codons"],
        columns=["Codon", "Count"]
    )

    fig = px.bar(
        codon_df,
        x="Codon",
        y="Count",
        text="Count",
        title="Top 10 Codons"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.dataframe(codon_df)

with tab5:

    st.subheader("AI Biological Interpretation")

    st.markdown(ai_report["data"])


st.divider()

st.header("📄 Generate Report")

if st.button("Generate PDF Report"):

    report = generate_report(
        filename="genome_report.pdf",
        genome_stats=stats1,
        gc_analysis=gc1,
        genome_compare=comparison,
        mutation_analysis=mutations,
        protein_analysis=protein1,
        codon_usage=codons1,
        ai_report=ai_report
    )

    if report["success"]:

        st.success("PDF generated successfully!")

        with open(report["data"], "rb") as f:

            st.download_button(
                label="📥 Download PDF",
                data=f,
                file_name="Genome_Report.pdf",
                mime="application/pdf"
            )

    else:

        st.error(report["message"])



st.subheader("Export Analysis")

json_data = json.dumps({

    "Genome Statistics": stats1["data"],

    "GC Analysis": gc1["data"],

    "Genome Comparison": comparison["data"],

    "Mutation Analysis": mutations["data"],

    "Protein Analysis": protein1["data"],

    "Codon Usage": codons1["data"]

}, indent=4)

st.download_button(

    "📥 Download JSON",

    json_data,

    file_name="analysis.json",

    mime="application/json"

)

summary = pd.DataFrame({

    "Metric":[

        "Genome Size",

        "GC %",

        "Similarity",

        "Mutations"

    ],

    "Value":[

        stats1["data"]["Genome Size"],

        gc1["data"]["Overall GC (%)"],

        comparison["data"]["Similarity (%)"],

        mutations["data"]["Total Mutations"]

    ]

})

csv = summary.to_csv(index=False)

st.download_button(

    "📥 Download CSV",

    csv,

    file_name="summary.csv",

    mime="text/csv"

)

st.divider()

st.markdown("""

---
### 🧬 AI Genome Comparative Analyzer

Developed using

- Python
- Streamlit
- Biopython
- Plotly
- ReportLab

Version **2.0**

""")

