import pandas as pd
import scipy.stats as stats
from sqlalchemy import create_engine

# ⚙️ PostgreSQL Connection Configuration
DB_USER = "postgres"
DB_PASS = "admin123"  # Update if your password is different
DB_HOST = "127.0.0.1"
DB_PORT = "5432"
DB_NAME = "postgres"

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

def run_hypothesis_tests():
    print("--- 1. Querying PostgreSQL Warehouse ---")
    engine = create_engine(DATABASE_URL)

    query = """
    SELECT 
        c.tcga_code,
        c.cell_line_name,
        d.drug_name,
        d.target_pathway,
        f.ln_ic50
    FROM oncology_dw.fact_drug_sensitivity f
    JOIN oncology_dw.dim_cell_lines c ON f.cosmic_id = c.cosmic_id
    JOIN oncology_dw.dim_drugs d ON f.drug_id = d.drug_id
    WHERE c.tcga_code IN ('SKCM', 'BRCA', 'LUAD')
      AND f.ln_ic50 IS NOT NULL;
    """
    
    df = pd.read_sql(query, engine)
    print(f"Loaded {len(df):,} records into Pandas DataFrame.\n")

    # Filter specifically for Melanoma (SKCM) cohort
    skcm_df = df[df['tcga_code'] == 'SKCM']

    # -------------------------------------------------------------
    # TEST 1: One-Way ANOVA (Pathway Sensitivity in Melanoma - SKCM)
    # -------------------------------------------------------------
    print("=" * 65)
    print("TEST 1: One-Way ANOVA (Pathway Sensitivity in Melanoma - SKCM)")
    print("=" * 65)
    
    # Filter for pathways with at least 30 samples for statistical validity
    valid_pathways = skcm_df['target_pathway'].value_counts()
    valid_pathways = valid_pathways[valid_pathways >= 30].index.tolist()
    
    pathway_groups = [
        skcm_df[skcm_df['target_pathway'] == pathway]['ln_ic50'].values 
        for pathway in valid_pathways
    ]

    f_stat, p_val_anova = stats.f_oneway(*pathway_groups)
    
    print(f"Pathways Evaluated: {len(valid_pathways)}")
    print(f"F-Statistic:         {f_stat:.4f}")
    print(f"p-value:             {p_val_anova:.4e}")
    
    if p_val_anova < 0.05:
        print("✅ CONCLUSION: Reject H0! Drug sensitivity varies significantly across target pathways (p < 0.05).")
    else:
        print("❌ CONCLUSION: Fail to reject H0. No significant variance detected across pathways.")

    # -------------------------------------------------------------
    # TEST 2: Two-Sample Welch's T-Test (MAPK vs Genome Integrity)
    # -------------------------------------------------------------
    print("\n" + "=" * 65)
    print("TEST 2: Two-Sample T-Test (MAPK Pathway vs Genome Integrity in SKCM)")
    print("=" * 65)

    # Partial string matching to catch variations like 'MAPK', 'MAPK/ERK', etc.
    mapk = skcm_df[skcm_df['target_pathway'].astype(str).str.contains('mapk', case=False, na=False)]['ln_ic50']
    genome = skcm_df[skcm_df['target_pathway'].astype(str).str.contains('genome', case=False, na=False)]['ln_ic50']

    if len(mapk) > 0 and len(genome) > 0:
        t_stat, p_val_t = stats.ttest_ind(mapk, genome, equal_var=False)
        
        print(f"MAPK Signaling Mean LN(IC50):     {mapk.mean():.4f}  (n={len(mapk):,})")
        print(f"Genome Integrity Mean LN(IC50):   {genome.mean():.4f}  (n={len(genome):,})")
        print(f"T-Statistic:                      {t_stat:.4f}")
        print(f"p-value:                          {p_val_t:.4e}")

        if p_val_t < 0.05:
            print("✅ CONCLUSION: Reject H0! Statistically significant difference in drug potency (p < 0.05).")
        else:
            print("❌ CONCLUSION: Fail to reject H0. No significant difference in drug potency.")
    else:
        print(f"⚠️ Could not find matching records (MAPK n={len(mapk)}, Genome n={len(genome)}).")

    print("\n✅ PHASE 4 COMPLETE: Hypothesis testing successfully executed!")

if __name__ == "__main__":
    run_hypothesis_tests()