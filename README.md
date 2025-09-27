Remove-Item -Recurse -Force venv
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py


-
semgrep --config "p/python" --config "p/secrets" --no-git-ignore .
semgrep --config "minhas_regras_hf.yml" .