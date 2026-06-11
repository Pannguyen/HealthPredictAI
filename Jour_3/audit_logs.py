import psycopg2
import subprocess
from datetime import datetime

# ─────────────────────────────────────────────
# CONFIGURATION
# ─────────────────────────────────────────────
DB_CONFIG = {
    "host":     "localhost",
    "port":     5432,
    "database": "tp_j2",
    "user":     "admin",
    "password": "admin"
}

FLASK_CONTAINER    = "flask_app"
POSTGRES_CONTAINER = "postgres_db"

print("\n" + "="*60)
print("  AUDIT LOGS — PostgreSQL & Docker")
print("  Auteur : Anh")
print(f"  Date   : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("="*60)


# ─────────────────────────────────────────────
# 1. CONNEXIONS ACTIVES (pg_stat_activity)
# ─────────────────────────────────────────────
print("\n[1] CONNEXIONS ACTIVES — pg_stat_activity")
print("-"*60)

try:
    conn = psycopg2.connect(**DB_CONFIG)
    cur  = conn.cursor()

    cur.execute("""
        SELECT pid, usename, application_name, client_addr,
               state, query_start,
               LEFT(query, 80) AS query_preview
        FROM pg_stat_activity
        WHERE datname = 'tp_j2'
        ORDER BY query_start DESC NULLS LAST;
    """)
    rows = cur.fetchall()

    if rows:
        print(f"{'PID':<8} {'User':<10} {'App':<20} {'Client':<16} {'State':<12} {'Query'}")
        print("-"*90)
        for r in rows:
            pid, user, app, client, state, qstart, query = r
            print(f"{str(pid):<8} {str(user):<10} {str(app):<20} {str(client):<16} {str(state):<12} {query or ''}")
    else:
        print("Aucune connexion active.")

    cur.close()
    conn.close()

except Exception as e:
    print(f"Erreur connexion PostgreSQL : {e}")


# ─────────────────────────────────────────────
# 2. STATISTIQUES DES REQUÊTES (pg_stat_statements)
# ─────────────────────────────────────────────
print("\n[2] TOP REQUÊTES — pg_stat_statements")
print("-"*60)

try:
    conn = psycopg2.connect(**DB_CONFIG)
    cur  = conn.cursor()

    # Vérifie si l'extension est disponible
    cur.execute("SELECT 1 FROM pg_extension WHERE extname = 'pg_stat_statements';")
    ext = cur.fetchone()

    if ext:
        cur.execute("""
            SELECT calls, total_exec_time::int, mean_exec_time::int,
                   LEFT(query, 100) AS query
            FROM pg_stat_statements
            WHERE dbid = (SELECT oid FROM pg_database WHERE datname = 'tp_j2')
            ORDER BY calls DESC
            LIMIT 10;
        """)
        rows = cur.fetchall()
        if rows:
            print(f"{'Appels':<8} {'Temps total(ms)':<18} {'Moy(ms)':<10} Query")
            print("-"*80)
            for r in rows:
                print(f"{r[0]:<8} {r[1]:<18} {r[2]:<10} {r[3]}")
        else:
            print("Aucune donnée disponible.")
    else:
        print("Extension pg_stat_statements non activée.")
        print("→ Ajoutez shared_preload_libraries='pg_stat_statements' dans postgresql.conf")

    cur.close()
    conn.close()

except Exception as e:
    print(f"Erreur : {e}")


# ─────────────────────────────────────────────
# 3. STATISTIQUES TABLE USERS
# ─────────────────────────────────────────────
print("\n[3] STATISTIQUES TABLE users — pg_stat_user_tables")
print("-"*60)

try:
    conn = psycopg2.connect(**DB_CONFIG)
    cur  = conn.cursor()

    cur.execute("""
        SELECT relname, seq_scan, idx_scan,
               n_tup_ins, n_tup_upd, n_tup_del,
               n_live_tup, n_dead_tup
        FROM pg_stat_user_tables
        WHERE relname = 'users';
    """)
    row = cur.fetchone()

    if row:
        labels = ["Table","Seq scans","Index scans","Insertions","Mises à jour","Suppressions","Lignes actives","Lignes mortes"]
        for label, val in zip(labels, row):
            print(f"  {label:<20} : {val}")
    else:
        print("Table 'users' introuvable dans les stats.")

    cur.close()
    conn.close()

except Exception as e:
    print(f"Erreur : {e}")


# ─────────────────────────────────────────────
# 4. LOGS DOCKER — Flask (tentatives connexion)
# ─────────────────────────────────────────────
print(f"\n[4] LOGS FLASK — {FLASK_CONTAINER}")
print("-"*60)

try:
    result = subprocess.run(
        ["docker", "logs", "--tail", "50", FLASK_CONTAINER],
        capture_output=True, text=True
    )
    logs = (result.stdout + result.stderr).split("\n")

    connexions_reussies  = []
    connexions_echouees  = []
    tentatives           = []

    for line in logs:
        if "CONNEXION_REUSSIE" in line:
            connexions_reussies.append(line.strip())
        elif "ECHEC_CONNEXION" in line:
            connexions_echouees.append(line.strip())
        elif "Tentative de connexion" in line:
            tentatives.append(line.strip())

    print(f"  Tentatives totales   : {len(tentatives)}")
    print(f"  Connexions réussies  : {len(connexions_reussies)}")
    print(f"  Échecs de connexion  : {len(connexions_echouees)}")

    # Détection brute force : >3 échecs
    if len(connexions_echouees) > 3:
        print(f"\n  ⚠️  ALERTE : {len(connexions_echouees)} échecs détectés — possible brute force !")

    if connexions_echouees:
        print("\n  Derniers échecs :")
        for l in connexions_echouees[-5:]:
            print(f"    {l}")

    if connexions_reussies:
        print("\n  Dernières connexions réussies :")
        for l in connexions_reussies[-3:]:
            print(f"    {l}")

except Exception as e:
    print(f"Erreur lecture logs Docker Flask : {e}")


# ─────────────────────────────────────────────
# 5. LOGS DOCKER — PostgreSQL (erreurs & requêtes)
# ─────────────────────────────────────────────
print(f"\n[5] LOGS PostgreSQL — {POSTGRES_CONTAINER}")
print("-"*60)

try:
    result = subprocess.run(
        ["docker", "logs", "--tail", "100", POSTGRES_CONTAINER],
        capture_output=True, text=True
    )
    logs = (result.stdout + result.stderr).split("\n")

    erreurs      = [l for l in logs if "ERROR" in l or "FATAL" in l]
    connexions   = [l for l in logs if "connection received" in l.lower()]
    deconnexions = [l for l in logs if "disconnection" in l.lower()]
    requetes     = [l for l in logs if "statement:" in l.lower() or "execute" in l.lower()]

    print(f"  Connexions reçues    : {len(connexions)}")
    print(f"  Déconnexions         : {len(deconnexions)}")
    print(f"  Requêtes loguées     : {len(requetes)}")
    print(f"  Erreurs / Fatales    : {len(erreurs)}")

    if erreurs:
        print("\n  ERREURS DÉTECTÉES :")
        for e in erreurs[-5:]:
            print(f"    {e.strip()}")

    # Détection d'injection : mots-clés suspects dans les requêtes
    suspects = [l for l in requetes if any(k in l.upper() for k in ["OR '1'='1", "DROP ", "UNION ", "-- ", "/*", "SLEEP(", "BENCHMARK("])]
    if suspects:
        print(f"\n   TENTATIVES D'INJECTION DÉTECTÉES ({len(suspects)}) :")
        for s in suspects:
            print(f"    {s.strip()}")
    else:
        print("\n  Aucune tentative d'injection dans les logs PostgreSQL.")

    if requetes:
        print("\n  Dernières requêtes SQL :")
        for r in requetes[-5:]:
            print(f"    {r.strip()[:120]}")

except Exception as e:
    print(f"Erreur lecture logs Docker PostgreSQL : {e}")


# ─────────────────────────────────────────────
# SYNTHÈSE
# ─────────────────────────────────────────────
print("\n" + "="*60)
print("  SYNTHÈSE DE L'AUDIT")
print("="*60)
print("  [1] Connexions actives PostgreSQL  → voir ci-dessus")
print("  [2] Top requêtes pg_stat_statements → voir ci-dessus")
print("  [3] Stats table users              → voir ci-dessus")
print("  [4] Logs Flask (tentatives/échecs) → voir ci-dessus")
print("  [5] Logs PostgreSQL (erreurs/SQL)  → voir ci-dessus")
print("="*60 + "\n")