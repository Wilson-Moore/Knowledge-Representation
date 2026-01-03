virtual enviroment (optinal)
    python -m venv .venv
    .venv\Script\activate.ps1 (Windows)
    source .venv/Script/activate (Linux)
if not working you can install dependencies directly

install dependencies
    pip install -r requirements.txt

run app
    python -m Ui.main

run tests
    python -m test.Test_Modal
    python -m test.Test_Fuzzy
    python -m test.Test_Belief
    python -m test.Test_Default