# 🧬 Cancer Pharmacogenomics Pipeline & Clinical Analytics Suite

An end-to-end automated data engineering, relational database warehousing, and advanced biostatistical analysis framework designed to evaluate drug sensitivity, genomic biomarkers, and targeted therapy responses in oncology research.

---

## 📋 Executive Summary & Project Details

In modern precision oncology, identifying which cancer cell lines respond to specific pharmacological treatments is paramount for translating genomic data into actionable clinical insights. This project builds a production-grade data pipeline leveraging the Genomics of Drug Sensitivity in Cancer (GDSC) repository. 

The system automates the complete lifecycle of clinical and pharmacological data: starting from raw multi-source ingestion and robust data cleaning, progressing to relational star schema modeling in PostgreSQL, executing rigorous non-parametric statistical tests and effect-size estimations in Python, and culminating in interactive Power BI executive dashboards and publication-grade visual artifacts.

---

## 🧪 Hypotheses Tested

To drive the analytical modeling within `src/advanced_analytics.py`, the following formal biostatistical hypotheses were formulated and tested:

1. **Pathway-Specific Drug Response Hypothesis:**
   * **Null Hypothesis ($H_0$):** There is no significant difference in drug sensitivity (measured via half-maximal inhibitory concentration or activity metrics) between cell lines characterized by specific oncogenic pathway mutations and wild-type cell lines.
   * **Alternative Hypothesis ($H_a$):** Cell lines harboring mutations in targeted oncogenic pathways exhibit statistically significant shifts in drug sensitivity distribution compared to control groups.

2. **Biomarker Effect Size and Significance Hypothesis:**
   * **Null Hypothesis ($H_0$):** Differential drug responses across distinct genomic annotations show negligible effect sizes ($\text{Cohen's } d \approx 0$) with non-significant false-discovery rate (FDR) adjusted $p$-values.
   * **Alternative Hypothesis ($H_a$):** Certain compounds demonstrate substantial, statistically robust effect sizes (large magnitude $\text{Cohen's } d$) when stratified by molecular subtype or biomarker status, highlighting potential candidate biomarkers for targeted therapy.

---

## ⚙️ Pipeline Architecture & Workflow

The pipeline is fully modularized and orchestrated via a master automation batch script (`run_pipeline.bat`) to execute sequentially without manual intervention:

1. **Data Ingestion & Preprocessing (`src/ingestion.py`):**
   * Processes raw Excel and CSV inputs (`Cell_Lines_Details.xlsx`, `Compounds-annotation.csv`, `GDSC_DATASET.csv`).
   * Handles missing value imputation, data type standardization, and outlier management using advanced **Winsorization** techniques to protect downstream statistical models from skewness.
   * Exports clean, standardized artifacts to `data/processed/`.

2. **Relational Data Warehouse (`src/load_to_postgres.py` & `sql/`):**
   * Connects to a PostgreSQL database instance.
   * Constructs an optimized **Star Schema** enforcing primary and foreign key constraints between dimension tables (Cell Lines, Compounds, Pathways) and fact tables (Drug Sensitivity Measurements).

3. **Advanced Statistics & Modeling (`src/advanced_analytics.py`):**
   * Executes high-performance vector computations using `Pandas` and `NumPy`.
   * Applies robust non-parametric **Mann-Whitney U tests** and calculates **Cohen's d Effect Sizes** to quantify the practical significance of drug response differences.
   * Automatically saves publication-grade visualization plots directly to the dashboard directory.

---

## 📊 Results & Analytical Insights

Execution of the advanced statistical modeling suite yielded critical quantitative insights into cancer pharmacology:

* **Identification of High-Impact Compounds:** Statistical screening successfully isolated candidate compounds exhibiting extreme effect sizes ($\text{Cohen's } d = -1.4567$), indicating major pharmacodynamic shifts linked to specific genomic profiles.
* **Pathway Vulnerability Mapping:** The Mann-Whitney U test results confirmed statistically significant response variances ($p < 0.001$) across targeted pathways, validating that specific oncogene dependencies heavily dictate drug efficacy.
* **Data-Driven Stratification:** The processed outputs successfully remove noise and skewness from high-throughput screening data, providing clinicians and researchers with clean subsets ready for downstream predictive modeling and patient stratification.

---

## 🖼️ Publication-Grade Visualizations & Dashboards

### 1. Differential Drug Sensitivity (Volcano Plot)
This plot contrasts statistical significance ($-\log_{10} p\text{-value}$) against practical significance ($\text{Cohen's } d$ Effect Size), enabling the immediate identification of top-performing candidate compounds and resistant cell line phenotypes.
![Volcano Plot](dashboard/plots/volcano_plot.png)

### 2. Pathway Sensitivity Distribution (Violin Plot)
A comparative distribution analysis illustrating drug response spreads across major cellular signaling pathways, exposing distinct bimodal sensitivities in targeted therapies.
![Violin Plot](dashboard/plots/pathway_violin_plot.png)

### 3. Executive Overview Dashboard (Power BI - Page 1)
An interactive Business Intelligence interface integrating database metrics to provide real-time exploration of executive summaries and drug screening results.
![Executive Overview](Page%201%20executive_overview.png.png)

### 4. Cohort Progression Matrix (Power BI - Page 2)
Dimensional drill-down matrix analyzing cell line lineages, compound annotations, and cohort progression metrics.
![Cohort Progression Matrix](Page%202%20cohort_progression_matrix.png.png)

---

## 🛠️ Project File Structure

```text
cancer-pharmacogenomics-pipeline/
│
├── dashboard/
│   └── plots/                # High-resolution saved plots (Volcano, Violin)
├── data/
│   ├── raw/                  # Original raw datasets (GDSC, Cell Lines, Compounds)
│   └── processed/            # Cleaned and Winsorized CSV outputs
├── sql/                      # DDL schema and custom analytical queries
├── src/                      # Source code for ETL and statistical models
│   ├── ingestion.py          # Data cleaning and preprocessing script
│   ├── load_to_postgres.py   # Database loader building the Star Schema
│   └── advanced_analytics.py # Statistical testing and plotting script
├── run_pipeline.bat          # Master automation orchestrator script





