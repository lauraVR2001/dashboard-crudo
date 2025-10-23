# KuenKa - Crudo Production Executive Dashboard

This repository contains a Dash app that visualizes annual crude oil production.

Files:
- `dashboard_crudo.py`: Main Dash app.

Quick start
1. Create a virtual environment and install dependencies:

```powershell
python -m venv .venv; .\.venv\Scripts\Activate.ps1; pip install -r requirements.txt
```

2. Run the app:

```powershell
python dashboard_crudo.py
```

Notes
- The app expects an Excel file named `produccion_crudo_anual.xlsx` in the same folder or in `D:\Analisis producción de gas 2025\Bases_produccion_crudo`.
- If you publish to GitHub, consider storing the Excel data outside the repo and use environment-specific loading.

License: MIT
