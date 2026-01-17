import customtkinter as ctk
from database.db_connection import get_connection
from datetime import date

class DashboardPage(ctk.CTkFrame):
    def __init__(self, parent, user_id):
        super().__init__(parent, fg_color="#0F172A")
        self.user_id = user_id

        # Titre
        ctk.CTkLabel(
            self,
            text="📊 Dashboard Vendeur",
            font=ctk.CTkFont(size=26, weight="bold"),
            text_color="#3B82F6"
        ).pack(pady=20)

        # Conteneur des stats
        self.stats_frame = ctk.CTkFrame(self, fg_color="#1E293B", corner_radius=15)
        self.stats_frame.pack(padx=40, pady=20, fill="both", expand=True)

        # Création des cartes pour chaque stat
        self.cards = {}
        stat_info = [
            ("Commandes aujourd'hui", "nb_commandes_label", "🛒"),
            ("Total ventes aujourd'hui", "total_ventes_label", "💰"),
            ("Total produits", "total_produits_label", "📦"),
            ("Produits en stock", "stock_label", "✅"),
            ("Produits en rupture", "rupture_label", "⚠️")
        ]

        for i, (title, attr_name, emoji) in enumerate(stat_info):
            card = ctk.CTkFrame(self.stats_frame, fg_color="#111827", corner_radius=10)
            card.grid(row=i//2, column=i%2, padx=20, pady=15, sticky="nsew")

            # Configure expansion
            self.stats_frame.grid_columnconfigure(i%2, weight=1)
            self.stats_frame.grid_rowconfigure(i//2, weight=1)

            label_title = ctk.CTkLabel(card, text=f"{emoji} {title}", font=ctk.CTkFont(size=14))
            label_title.pack(pady=(10,5))

            label_value = ctk.CTkLabel(card, text="0", font=ctk.CTkFont(size=20, weight="bold"), text_color="#FACC15")
            label_value.pack(pady=(0,10))

            setattr(self, attr_name, label_value)
            self.cards[attr_name] = card

        self.refresh()

    def refresh(self):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        # Statistiques commandes / ventes (filtrées par vendeur)
        cursor.execute("""
            SELECT COUNT(c.id) AS nb, SUM(f.total) AS total
            FROM commandes c
            LEFT JOIN factures f ON f.id_commande = c.id
            WHERE c.id_vendeur = %s AND DATE(c.date_commande) = %s
        """, (self.user_id, date.today()))
        row = cursor.fetchone()

        self.nb_commandes_label.configure(text=f"{row['nb'] or 0}")
        self.total_ventes_label.configure(text=f"{row['total'] or 0} DT")

        # Statistiques produits (globales, pas de filtre vendeur)
        cursor.execute("SELECT COUNT(*) AS total_produits FROM produits")
        total = cursor.fetchone()
        self.total_produits_label.configure(text=f"{total['total_produits'] or 0}")

        cursor.execute("SELECT COUNT(*) AS nb_stock FROM produits WHERE quantite > 0")
        stock = cursor.fetchone()
        self.stock_label.configure(text=f"{stock['nb_stock'] or 0}")

        cursor.execute("SELECT COUNT(*) AS nb_rupture FROM produits WHERE quantite = 0")
        rupture = cursor.fetchone()
        self.rupture_label.configure(text=f"{rupture['nb_rupture'] or 0}")

        conn.close()

