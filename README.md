# 🧬 Cancer Pharmacogenomics Pipeline & Clinical Analytics

An end-to-end automated data pipeline, relational data warehouse, and advanced statistical analysis system designed to evaluate drug sensitivity and genomic biomarkers in oncology research.

---

## 🚀 Project Overview
This project builds an automated data workflow using public pharmacogenomics datasets (GDSC). It handles raw data cleaning, missing value handling, outliers treatment (Winsorization), star schema database loading, and rigorous statistical modeling (such as Mann-Whitney U tests and Cohen's d effect sizes) to identify significant drug-gene response patterns.

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