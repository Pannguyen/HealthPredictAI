from flask import Flask, request, render_template_string
import psycopg2

app = Flask(__name__)

def get_connection():
    return psycopg2.connect(
        host="db",
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

        conn = get_connection()
        cur = conn.cursor()

        # VERSION VOLONTAIREMENT VULNÉRABLE
        query = f"""
        SELECT id, username, email
        FROM users
        WHERE username = '{username}'
        AND password = '{password}'
        """

        print("SQL exécutée :", flush=True)
        print(query, flush=True)

        cur.execute(query)

        user = cur.fetchone()

        cur.close()
        conn.close()

        if user:
            return f"""
            <h2>Connexion réussie</h2>
            <p>ID : {user[0]}</p>
            <p>Utilisateur : {user[1]}</p>
            <p>Email : {user[2]}</p>
            """

        else:
            message = "Identifiant ou mot de passe incorrect"

    return render_template_string("""
        <h1>Connexion</h1>

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
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )