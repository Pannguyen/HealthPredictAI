from flask import Flask, request, render_template_string
import psycopg2
import bcrypt
import logging

app = Flask(__name__)

# CONFIGURATION DE LA JOURNALISATION (LOGS)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] [APP-AUTH] %(message)s',
    handlers=[
        logging.FileHandler("/var/log/flask/app.log"),
        logging.StreamHandler() # Permet à Docker de collecter les logs
    ]
)

def get_connection():
    return psycopg2.connect(
        host="db",          
        port="5432",        
        database="tp_j2",
        user="admin",
        password="admin"
    )

@app.route("/", methods=["GET", "POST"])
def login():
    message = ""

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        logging.info(f"Tentative de connexion initiée pour l'utilisateur : {username}")

        conn = get_connection()
        cur = conn.cursor()

        # VERSION SÉCURISÉE : Requête préparée (séparation stricte code/donnée)
        # On ne sélectionne que par username pour récupérer le hash
        query = "SELECT id, username, password, email FROM users WHERE username = %s;"
        
        cur.execute(query, (username,))
        user = cur.fetchone()

        cur.close()
        conn.close()

        # Vérification du mot de passe haché
        if user and bcrypt.checkpw(password.encode('utf-8'), user[2].encode('utf-8')):
            logging.info(f"CONNEXION_REUSSIE - Utilisateur : {username}")
            return f"""
            <h2>Connexion réussie</h2>
            <p>ID : {user[0]}</p>
            <p>Utilisateur : {user[1]}</p>
            <p>Email : {user[3]}</p>
            <a href="/">Retour</a>
            """
        else:
            logging.warning(f"ECHEC_CONNEXION - Tentative invalide pour l'utilisateur : {username}")
            message = "Identifiant ou mot de passe incorrect"

    return render_template_string("""
        <h1>Connexion Sécurisée</h1>
        <form method="POST">
            <label>Username :</label><br>
            <input type="text" name="username"><br><br>
            <label>Password :</label><br>
            <input type="password" name="password"><br><br>
            <button type="submit">Se connecter</button>
        </form>
        <p style="color:red;">{{ message }}</p>
    """, message=message)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)