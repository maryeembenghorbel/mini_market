import sys
import os
# Ajouter le dossier parent pour que Python trouve password_utils
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
from password_utils import check_password
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'database')))
from db_conection import get_connection


def login(username, password):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, password, role FROM utilisateur WHERE username=%s",
        (username,)
    )
    result = cursor.fetchone()
    conn.close()

    if result:
        user_id, hashed_pw, role = result
        if check_password(password, hashed_pw):
            return role, user_id   # ← on garde les deux
    return None, None
