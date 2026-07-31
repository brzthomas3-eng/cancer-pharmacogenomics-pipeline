import pandas as pd
from sqlalchemy import create_engine, text

# ⚙️ PostgreSQL Connection Configuration
DB_USER = "postgres"
DB_PASS = "admin123"
DB_HOST = "127.0.0.1"
DB_PORT = "5432"
DB_NAME = "postgres"

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

def load_warehouse():
    print("--- 1. Connecting to PostgreSQL ---")
    engine = create_engine(DATABASE_URL)

    print("--- 2. Building Schema & Tables ---")
    with engine.begin() as conn:
        conn.execute(text("CREATE SCHEMA IF NOT EXISTS oncology_dw;"))
        
        # Create Dimension: Cell Lines
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS oncology_dw.dim_cell_lines (
                cosmic_id INT PRIMARY KEY,
                cell_line_name VARCHAR(255),
                tcga_code VARCHAR(50),
                tissue_type VARCHAR(255)
            );
        """))

        # Create Dimension: Drugs
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS oncology_dw.dim_drugs (
                drug_id INT PRIMARY KEY,
                drug_name VARCHAR(255),
                target_pathway VARCHAR(255)
            );
        """))

        # Create Fact Table: Drug Sensitivity
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS oncology_dw.fact_drug_sensitivity (
                experiment_id SERIAL PRIMARY KEY,
                cosmic_id INT REFERENCES oncology_dw.dim_cell_lines(cosmic_id),
                drug_id INT REFERENCES oncology_dw.dim_drugs(drug_id),
                dataset_version VARCHAR(20),
                ln_ic50 NUMERIC(10, 4),
                auc NUMERIC(10, 4)
            );
        """))
    print("Schema 'oncology_dw' and tables verified/created successfully.")

if __name__ == "__main__":
    load_warehouse()