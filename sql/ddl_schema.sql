-- Create database schema
CREATE SCHEMA IF NOT EXISTS oncology_dw;

-- Dimension: Cancer Cell Lines
CREATE TABLE IF NOT EXISTS oncology_dw.dim_cell_lines (
    cosmic_id INT PRIMARY KEY,
    cell_line_name VARCHAR(100) NOT NULL,
    tissue_descriptor VARCHAR(150),
    tcga_code VARCHAR(50),
    msi_status VARCHAR(50)
);

-- Dimension: Anti-Cancer Compounds
CREATE TABLE IF NOT EXISTS oncology_dw.dim_drugs (
    drug_id INT PRIMARY KEY,
    drug_name VARCHAR(150) NOT NULL,
    target_gene VARCHAR(250),
    target_pathway VARCHAR(150)
);

-- Fact: Pharmacogenomic Sensitivity Screening Experiments
CREATE TABLE IF NOT EXISTS oncology_dw.fact_drug_sensitivity (
    cosmic_id INT,
    drug_id INT,
    ln_ic50 NUMERIC(10, 4) NOT NULL,
    auc NUMERIC(10, 4),
    z_score NUMERIC(10, 4),
    dataset_version VARCHAR(20) NOT NULL
);

-- Analytical Cohort Query: Drug Sensitivity Percentile Stratification
WITH cohort_sensitivity AS (
    SELECT 
        c.tcga_code,
        c.cell_line_name,
        d.drug_name,
        d.target_pathway,
        f.dataset_version,
        f.ln_ic50,
        PERCENT_RANK() OVER (
            PARTITION BY c.tcga_code, d.drug_id, f.dataset_version 
            ORDER BY f.ln_ic50 ASC
        ) AS sensitivity_percentile
    FROM oncology_dw.fact_drug_sensitivity f
    JOIN oncology_dw.dim_cell_lines c ON f.cosmic_id = c.cosmic_id
    JOIN oncology_dw.dim_drugs d ON f.drug_id = d.drug_id
    WHERE c.tcga_code IN ('LUAD', 'BRCA', 'SKCM', 'COAD/READ')
)
SELECT 
    tcga_code AS cancer_type,
    drug_name,
    target_pathway,
    cell_line_name,
    dataset_version,
    ln_ic50,
    ROUND(sensitivity_percentile::numeric, 4) AS response_percentile,
    CASE 
        WHEN sensitivity_percentile <= 0.15 THEN 'Responder (High Sensitivity)'
        WHEN sensitivity_percentile >= 0.85 THEN 'Non-Responder (Resistant)'
        ELSE 'Intermediate Sensitivity'
    END AS clinical_response_tier
FROM cohort_sensitivity
ORDER BY tcga_code, drug_name, sensitivity_percentile;