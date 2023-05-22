Environment requirement: have python3 installed on your computer
Method1: use the venv we provide
    1. activate the `myvenv` in the folder
        * MacOS: source myvenv/bin/activate
        * Windows powershell: myvenv\bin\Activate.ps1
    2. `flask run` in the terminal
    3. click on the link to open it in browser (should be http://127.0.0.1:5000 in default)

Method2: create your own venv:
    1. python3 -m venv newvenv (try python if not python3)
    2. follow the step1 in Method1 to activate the venv 
    3. pip3 install -r requirements.txt (try pip if not pip3)
    4. follow the step2 and step3 in method1.
