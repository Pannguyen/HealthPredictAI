#!/bin/sh
echo "Attente de PostgreSQL..."
until python -c "import socket; s=socket.socket(); exit(s.connect_ex(('db', 5432)))"; do
  sleep 1
done
echo "PostgreSQL prêt."
python init_db.py
python app.py