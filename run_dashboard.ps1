# PowerShell script to create venv and run the Dash app
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python dashboard_crudo.py
