# 🧬 Cancer Pharmacogenomics Pipeline & Clinical Analytics

An end-to-end automated data pipeline, relational data warehouse, and advanced statistical analysis system designed to evaluate drug sensitivity and genomic biomarkers in oncology research.

---

## 🚀 Project Overview
This project builds an automated data workflow using public pharmacogenomics datasets (GDSC). It handles raw data cleaning, missing value handling, outliers treatment (Winsorization), star schema database loading, and rigorous statistical modeling (such as Mann-Whitney U tests and Cohen's d effect sizes) to identify significant drug-gene response patterns.

### 1. Executive Overview Dashboard (Power BI - Page 1)
![Executive Overview](Page%201%20executive_overview.png.png)

### 2. Cohort Progression Matrix (Power BI - Page 2)
![Cohort Progression Matrix](Page%202%20cohort_progression_matrix.png.png)

### 3. Differential Drug Sensitivity (Volcano Plot)
![Volcano Plot](dashboard/plots/volcano_plot.png)

### 4. Pathway Sensitivity Distribution (Violin Plot)
![Violin Plot](dashboard/plots/pathway_violin_plot.png)

---

## 🛠️ Project Structure
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
├── Oncology Pharmacology Dashboard.pbix  # Power BI interactive dashboard
└── run_pipeline.bat          # Master automation orchestrator script





