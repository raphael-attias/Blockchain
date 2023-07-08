from trilio import Trilio
import datetime
import subprocess

def execute_python_script(script_path):
    try:
        with open(script_path, 'r') as file:
            script_code = file.read()
        exec(script_code)
        print("Le script s'est exécuté avec succès.")
    except Exception as e:
        print("Une erreur s'est produite lors de l'exécution du script.")
        print(str(e))

execute_python_script("votre_script.py")


blockchain = Trilio()
print('Welcome to LPF Blockchain')
entr = int(input('What is your name? '))

if entr == 0:
    print('Creating an account')
    username = input('Enter your username: ')
    execute_python_script("C:\Users\Raphael\Desktop\projet\bc\wallet3.py")

