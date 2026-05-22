import requests

URL = "http://localhost:5001/"

def tester_connexion_normale():
    print("--- Test 1 : connexion avec mauvais mot de passe ---")

    donnees = {
        "username": "admin",
        "password": "mauvais_password"
    }

    response = requests.post(URL, data=donnees)

    if "Identifiant ou mot de passe incorrect" in response.text:
        print("Résultat : Échec de connexion OK\n")
    else:
        print("Résultat inattendu\n")
        print(response.text)


def tester_injection_sql():
    print("--- Test 2 : SQL Injection ---")

    donnees = {
        "username": "admin' OR '1'='1' -- ",
        "password": "ignored"
    }

    response = requests.post(URL, data=donnees)

    print(response.text)

    if "Connexion réussie" in response.text:
        print("Résultat : INJECTION RÉUSSIE !")
    else:
        print("Résultat : Injection échouée")


if __name__ == "__main__":
    try:
        tester_connexion_normale()
        tester_injection_sql()
    except requests.exceptions.ConnectionError:
        print("Erreur : impossible de se connecter à l'application.")
        print("Vérifie que Docker tourne et que l'app est sur http://localhost:5001/")