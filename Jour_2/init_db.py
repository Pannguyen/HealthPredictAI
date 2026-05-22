import psycopg2
import time

time.sleep(5)

conn = psycopg2.connect(
    host="db",
    database="tp_j2",
    user="admin",
    password="admin"
)

cur = conn.cursor()

cur.execute("""
DROP TABLE IF EXISTS users;
""")

cur.execute("""
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50),
    password VARCHAR(50),
    email VARCHAR(100)
)
""")

cur.execute("""
INSERT INTO users (username,password,email)
VALUES
('admin','admin123','admin@test.com'),
('alice','alice123','alice@test.com'),
('bob','bob123','bob@test.com')
""")

conn.commit()

cur.close()
conn.close()

print("Database initialized.")