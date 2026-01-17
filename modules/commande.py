from database.db_connection import get_connection

def creer_commande(id_vendeur):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO commandes (id_vendeur) VALUES (%s)", (id_vendeur,))
    id_commande = cursor.lastrowid
    conn.commit()
    conn.close()
    return id_commande

def ajouter_detail_commande(id_commande, id_produit, quantite, prix):
    conn = get_connection()
    cursor = conn.cursor()
    # Vérifier le stock
    cursor.execute("SELECT quantite FROM produits WHERE id=%s", (id_produit,))
    stock = cursor.fetchone()[0]
    if stock < quantite:
        conn.close()
        return False, stock
    # Ajouter detail
    cursor.execute("""
        INSERT INTO details_commande (id_commande, id_produit, quantite, prix)
        VALUES (%s, %s, %s, %s)
    """, (id_commande, id_produit, quantite, prix))
    # Mettre à jour stock
    cursor.execute("UPDATE produits SET quantite = quantite - %s WHERE id=%s", (quantite, id_produit))
    conn.commit()
    conn.close()
    return True, stock - quantite

def get_commandes_du_vendeur(id_vendeur):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM commandes WHERE id_vendeur=%s ORDER BY date_commande DESC", (id_vendeur,))
    commandes = cursor.fetchall()
    conn.close()
    return commandes


def supprimer_commande_et_restituer_stock(id_commande):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        conn.start_transaction()

        # 1. Produits et quantités
        cursor.execute("""
            SELECT id_produit, quantite
            FROM details_commande
            WHERE id_commande = %s
        """, (id_commande,))
        lignes = cursor.fetchall()

        if not lignes:
            raise Exception("Commande introuvable.")

        # 2. Restituer le stock
        for ligne in lignes:
            cursor.execute("""
                UPDATE produits
                SET quantite = quantite + %s
                WHERE id = %s
            """, (ligne['quantite'], ligne['id_produit']))

        # 3. Supprimer la facture liée
        cursor.execute("""
            DELETE FROM factures
            WHERE id_commande = %s
        """, (id_commande,))

        # 4. Supprimer les détails de commande
        cursor.execute("""
            DELETE FROM details_commande
            WHERE id_commande = %s
        """, (id_commande,))

        # 5. Supprimer la commande
        cursor.execute("""
            DELETE FROM commandes
            WHERE id = %s
        """, (id_commande,))

        conn.commit()

    except Exception as e:
        conn.rollback()
        raise e

    finally:
        cursor.close()
        conn.close()