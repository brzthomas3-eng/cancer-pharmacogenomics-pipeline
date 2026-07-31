@echo off
echo =======================================================
echo 🧬 Starting Cancer Pharmacogenomics Pipeline...
echo =======================================================

echo.
echo [1/3] Ingesting, Cleaning, and Winsorizing Raw Data...
python src/ingestion.py

echo.
echo [2/3] Building Star Schema and Loading to PostgreSQL...
python src/load_to_postgres.py

echo.
echo [3/3] Running Advanced Statistics and Generating Plots...
python src/advanced_analytics.py

echo.
echo =======================================================
echo ✅ Pipeline Execution Complete! All plots generated.
echo =======================================================
pause