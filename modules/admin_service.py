import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# ---- STATISTIQUES ----

def total_produits():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM produits")
    result = cur.fetchone()[0]
    conn.close()
    return result

def produits_en_rupture():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM produits WHERE quantite = 0")
    result = cur.fetchone()[0]
    conn.close()
    return result

def commandes_aujourdhui():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT COUNT(*) FROM commandes
        WHERE DATE(date_commande) = CURDATE()
    """)
    result = cur.fetchone()[0]
    conn.close()
    return result

def chiffre_affaires_jour():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT IFNULL(SUM(total), 0)
        FROM factures
        WHERE DATE(date_facture) = CURDATE()
    """)
    result = cur.fetchone()[0]
    conn.close()
    return result
