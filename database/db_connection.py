import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="mini_market"
    )

# TEST DE CONNEXION
try:
    conn = get_connection()
    print("✅ Connexion à MySQL réussie !")
    conn.close()
except mysql.connector.Error as err:
    print("❌ Erreur de connexion :", err)