


from database.db_connection import get_connection

def get_all_products():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, nom, categorie, prix, quantite, image, date_creation
        FROM produits
        ORDER BY id DESC
    """)
    rows = cursor.fetchall()
    conn.close()
    return rows

def create_product(nom, categorie, prix, quantite, image):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO produits (nom, categorie, prix, quantite, image, date_creation)
        VALUES (%s, %s, %s, %s, %s, NOW())
    """, (nom, categorie, prix, quantite, image))
    conn.commit()
    conn.close()

def update_product(prod_id, nom, categorie, prix, quantite, image):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE produits
        SET nom=%s, categorie=%s, prix=%s, quantite=%s, image=%s
        WHERE id=%s
    """, (nom, categorie, prix, quantite, image, prod_id))
    conn.commit()
    conn.close()

def delete_product(prod_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM produits WHERE id=%s", (prod_id,))
    conn.commit()
    conn.close()
    
def product_exists_by_name(nom):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id FROM produits WHERE nom = %s",
        (nom,)
    )
    row = cursor.fetchone()
    conn.close()
    return row is not None


def get_produits_en_stock():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM produits WHERE quantite > 0")
    result = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    return result


def get_produits_en_rupture():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM produits WHERE quantite = 0")
    result = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    return result
