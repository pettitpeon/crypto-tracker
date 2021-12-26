# blockchain-explorer

download python
https://www.python.org/downloads/
python -m venv .venv
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt

streamlit run .\crypto-tracker.py