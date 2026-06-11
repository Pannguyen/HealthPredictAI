import psycopg2
import bcrypt
import time

print("Waiting for database...")
time.sleep(5)

conn = psycopg2.connect(
    host="db",   
    port="5432",        # <-- Port exposé par le Docker Compose
    database="tp_j2",
    user="admin",
    password="admin"
)
cur = conn.cursor()

cur.execute("DROP TABLE IF EXISTS users;")

# password VARCHAR(255) pour accueillir le hash de sécurité
cur.execute("""
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(100)
)
""")

# Mots de passe initiaux à hacher
initial_users = [
    ('admin', 'admin123', 'admin@test.com'),
    ('alice', 'alice123', 'alice@test.com'),
    ('bob', 'bob123', 'bob@test.com')
]

for username, plain_password, email in initial_users:
    # Génération du sel et du hash bcrypt
    salt = bcrypt.gensalt(rounds=12)
    hashed_password = bcrypt.hashpw(plain_password.encode('utf-8'), salt).decode('utf-8')
    
    # Requête préparée pour l'insertion
    cur.execute(
        "INSERT INTO users (username, password, email) VALUES (%s, %s, %s);",
        (username, hashed_password, email)
    )

conn.commit()
cur.close()
conn.close()

print("Database initialized securely with Bcrypt hashes.")