import pandas as pd
import numpy as np
import scipy.stats as stats
import statsmodels.api as sm
from statsmodels.stats.multicomp import pairwise_tukeyhsd
import seaborn as sns
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
import os

# ⚙️ PostgreSQL Connection Configuration
DB_USER = "postgres"
DB_PASS = "admin123"  # Update if your password is different
DB_HOST = "127.0.0.1"
DB_PORT = "5432"
DB_NAME = "postgres"

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

def run_advanced_analytics():
    print("--- 1. Querying PostgreSQL Warehouse ---")
    engine = create_engine(DATABASE_URL)
    
    query = """
    SELECT 
        c.tcga_code, 
        d.drug_name, 
        d.target_pathway, 
        f.ln_ic50
    FROM oncology_dw.fact_drug_sensitivity f
    JOIN oncology_dw.dim_cell_lines c ON f.cosmic_id = c.cosmic_id
    JOIN oncology_dw.dim_drugs d ON f.drug_id = d.drug_id
    WHERE c.tcga_code = 'SKCM' AND f.ln_ic50 IS NOT NULL;
    """
    
    skcm_df = pd.read_sql(query, engine)
    print(f"Loaded {len(skcm_df):,} Melanoma (SKCM) records.")

    # Filter for top 5 pathways for clear statistical plotting
    top_pathways = skcm_df['target_pathway'].value_counts().nlargest(5).index
    filtered_df = skcm_df[skcm_df['target_pathway'].isin(top_pathways)].copy()

    # -------------------------------------------------------------
    # 1. POST-HOC TEST: Tukey's HSD
    # -------------------------------------------------------------
    print("\n" + "=" * 65)
    print("ADVANCED STATS: Tukey's Honest Significant Difference (HSD)")
    print("=" * 65)
    
    tukey_results = pairwise_tukeyhsd(
        endog=filtered_df['ln_ic50'], 
        groups=filtered_df['target_pathway'], 
        alpha=0.05
    )
    print(tukey_results)

    # -------------------------------------------------------------
    # 2. EFFECT SIZE: Cohen's d (MAPK vs Genome Integrity)
    # -------------------------------------------------------------
    print("\n" + "=" * 65)
    print("ADVANCED STATS: Cohen's d Effect Size")
    print("=" * 65)
    
    mapk = skcm_df[skcm_df['target_pathway'].astype(str).str.contains('mapk', case=False, na=False)]['ln_ic50']
    genome = skcm_df[skcm_df['target_pathway'].astype(str).str.contains('genome', case=False, na=False)]['ln_ic50']
    
    nx, ny = len(mapk), len(genome)
    dof = nx + ny - 2
    pool_sd = np.sqrt(((nx - 1) * np.var(mapk, ddof=1) + (ny - 1) * np.var(genome, ddof=1)) / dof)
    cohens_d = (mapk.mean() - genome.mean()) / pool_sd
    
    print(f"MAPK Mean LN(IC50):           {mapk.mean():.4f}")
    print(f"Genome Integrity Mean LN(IC50): {genome.mean():.4f}")
    print(f"Cohen's d Effect Size:        {cohens_d:.4f}")

    # Ensure save directory exists
    os.makedirs("dashboard/plots", exist_ok=True)
    sns.set_theme(style="whitegrid", font_scale=1.1)

    # -------------------------------------------------------------
    # 3. COMPLEX VISUALIZATION 1: Violin + Stripplot Overlay
    # -------------------------------------------------------------
    print("\n--- 3. Generating Publication-Grade Visualizations ---")
    plt.figure(figsize=(12, 7))
    
    sns.violinplot(
        x='target_pathway', y='ln_ic50', data=filtered_df, 
        inner=None, color=".9", cut=0
    )
    
    # Updated to fix the Seaborn warning (added hue & legend=False)
    sns.stripplot(
        x='target_pathway', y='ln_ic50', data=filtered_df, 
        size=3, alpha=0.5, hue='target_pathway', palette="Set2", legend=False, jitter=0.25
    )
    
    plt.title("Probability Density & Experimental Spread of Drug Potency (Melanoma SKCM)", fontsize=14, fontweight='bold', pad=15)
    plt.xlabel("Target Pathway", fontsize=12, labelpad=10)
    plt.ylabel("LN(IC50) - Lower = Higher Potency", fontsize=12)
    plt.xticks(rotation=25, ha='right')
    plt.tight_layout()
    
    violin_path = "dashboard/plots/pathway_violin_plot.png"
    plt.savefig(violin_path, dpi=300)
    print(f"✅ Violin plot saved to: {violin_path}")

    # -------------------------------------------------------------
    # 4. COMPLEX VISUALIZATION 2: Volcano Plot (Drug-Level Potency)
    # -------------------------------------------------------------
    print("\n--- 4. Generating Volcano Plot (Drug vs Significance) ---")
    
    drugs = skcm_df['drug_name'].unique()
    volcano_data = []
    overall_mean = skcm_df['ln_ic50'].mean()
    
    for drug in drugs:
        drug_data = skcm_df[skcm_df['drug_name'] == drug]['ln_ic50']
        other_data = skcm_df[skcm_df['drug_name'] != drug]['ln_ic50']
        
        # Only evaluate drugs with at least 3 experimental data points
        if len(drug_data) >= 3:
            t_stat, p_val = stats.ttest_ind(drug_data, other_data, equal_var=False)
            mean_diff = drug_data.mean() - overall_mean # Negative = More Potent
            
            volcano_data.append({
                'drug_name': drug,
                'mean_diff': mean_diff,
                'p_val': p_val
            })

    volcano_df = pd.DataFrame(volcano_data)
    
    # Calculate -log10(p-value) with a tiny buffer to prevent math errors on exactly 0
    volcano_df['-log10(p_value)'] = -np.log10(volcano_df['p_val'] + 1e-300)
    
    # Define thresholds
    p_threshold = -np.log10(0.05)
    effect_threshold = -1.5 
    
    def categorize_drug(row):
        if row['-log10(p_value)'] > p_threshold and row['mean_diff'] < effect_threshold:
            return 'Significantly High Potency'
        elif row['-log10(p_value)'] > p_threshold and row['mean_diff'] > abs(effect_threshold):
            return 'Significantly High Resistance'
        else:
            return 'Not Significant / Small Effect'
            
    volcano_df['Significance'] = volcano_df.apply(categorize_drug, axis=1)

    plt.figure(figsize=(10, 8))
    
    palette_colors = {
        'Significantly High Potency': '#2ca02c', # Green
        'Significantly High Resistance': '#d62728', # Red
        'Not Significant / Small Effect': '#cccccc' # Grey
    }
    
    sns.scatterplot(
        data=volcano_df, 
        x='mean_diff', 
        y='-log10(p_value)', 
        hue='Significance',
        palette=palette_colors,
        alpha=0.7,
        edgecolor=None
    )
    
    plt.axvline(effect_threshold, color='green', linestyle='--', alpha=0.5)
    plt.axvline(abs(effect_threshold), color='red', linestyle='--', alpha=0.5)
    plt.axhline(p_threshold, color='black', linestyle='--', alpha=0.5)
    
    plt.title("Volcano Plot: Drug Potency vs Statistical Significance (Melanoma)", fontsize=14, fontweight='bold', pad=15)
    plt.xlabel("Mean Difference in LN(IC50) [Negative = Higher Potency]", fontsize=12)
    plt.ylabel("-Log10 (p-value)", fontsize=12)
    plt.legend(title="Drug Classification", bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    
    volcano_path = "dashboard/plots/volcano_plot.png"
    plt.savefig(volcano_path, dpi=300, bbox_inches='tight')
    print(f"✅ Volcano plot saved to: {volcano_path}")

if __name__ == "__main__":
    run_advanced_analytics()