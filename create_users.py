import sys
import os

# Ajouter le dossier modules pour password_utils
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'modules')))
from password_utils import check_password, hash_password

# Ajouter le dossier database pour db_connection
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'database')))

from db_connection import get_connection

# Connexion MySQL
conn = get_connection()
cursor = conn.cursor()

# Hasher les mots de passe
admin_hashed = hash_password("admin123")
vendeur_hashed = hash_password("vendeur123")

cursor.execute(
    "INSERT INTO utilisateur (username, password, role) VALUES (%s, %s, %s)",
    ("admin", admin_hashed, "admin")
)

cursor.execute(
    "INSERT INTO utilisateur (username, password, role) VALUES (%s, %s, %s)",
    ("vendeur1", vendeur_hashed, "vendeur")
)

conn.commit()
conn.close()

print("Utilisateurs créés !")
