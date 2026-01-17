import customtkinter as ctk

from gui.vendeur_pages.dashboard_page import DashboardPage
from gui.vendeur_pages.commandes_page import CommandesPage
from gui.vendeur_pages.nouvelle_commande_page import NouvelleCommandePage
from database.db_connection import get_connection
from datetime import date
from modules.produits import get_produits_en_stock, get_produits_en_rupture


class VendeurDashboard(ctk.CTk):

    def __init__(self, user_id, username):
        super().__init__()
        self.user_id = user_id
        self.username = username

        self.title(f"Espace Vendeur - {self.username}")
        self.geometry("1200x700")
        self.configure(fg_color="#0F172A")

        self.create_layout()
        self.show_page("dashboard")
        self.refresh_dashboard()  # Met à jour les valeurs au démarrage

    def create_layout(self):
        # NAVBAR
        navbar = ctk.CTkFrame(self, width=220, fg_color="#020617")
        navbar.pack(side="left", fill="y")

        ctk.CTkLabel(
            navbar,
            text=f"👤 {self.username}",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#3B82F6"
        ).pack(pady=20)

        ctk.CTkButton(navbar, text="Dashboard",
                      command=lambda: self.show_page("dashboard")).pack(fill="x", padx=10, pady=5)
        ctk.CTkButton(navbar, text="Nouvelle commande",
                      command=lambda: self.show_page("new")).pack(fill="x", padx=10, pady=5)
        ctk.CTkButton(navbar, text="Commandes",
                      command=lambda: self.show_page("commandes")).pack(fill="x", padx=10, pady=5)

        # CONTENEUR CENTRAL
        self.container = ctk.CTkFrame(self, fg_color="#0F172A")
        self.container.pack(side="right", fill="both", expand=True)

        self.pages = {
            "dashboard": DashboardPage(self.container, self.user_id),
            "new": NouvelleCommandePage(self.container, self.user_id),
            "commandes": CommandesPage(self.container, self.user_id)
        }

        for page in self.pages.values():
            page.place(relwidth=1, relheight=1)

    def show_page(self, name):
        self.pages[name].tkraise()
        if hasattr(self.pages[name], "refresh"):
            self.pages[name].refresh()
        if name == "dashboard":
            self.refresh_dashboard()

    def refresh_dashboard(self):
        """Met à jour les compteurs du dashboard"""
        try:
            today_str = date.today().strftime("%Y-%m-%d")
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)

            # Nombre de commandes aujourd'hui
            cursor.execute("""
                SELECT COUNT(*) AS nb_commandes
                FROM commandes
                WHERE id_vendeur = %s
                  AND DATE(date_commande) = %s
            """, (self.user_id, today_str))
            nb_commandes = cursor.fetchone()['nb_commandes']

            # Total des ventes aujourd'hui
            cursor.execute("""
                SELECT COALESCE(SUM(total_par_commande), 0) AS total_ventes
                FROM (
                    SELECT SUM(dc.quantite * dc.prix) AS total_par_commande
                    FROM details_commande dc
                    JOIN commandes c ON dc.id_commande = c.id
                    WHERE c.id_vendeur = %s
                      AND DATE(c.date_commande) = %s
                    GROUP BY dc.id_commande
                ) t
            """, (self.user_id, today_str))
            total_ventes = float(cursor.fetchone()['total_ventes'])

            conn.close()

            # Met à jour les labels dans le DashboardPage
            dashboard_page = self.pages["dashboard"]
            dashboard_page.nb_commandes_label.configure(text=f"Commandes aujourd'hui: {nb_commandes}")
            dashboard_page.total_ventes_label.configure(text=f"Total ventes aujourd'hui: {total_ventes} DT")

        except Exception as e:
            print(f"Erreur refresh_dashboard: {e}")
            dashboard_page = self.pages["dashboard"]
            dashboard_page.nb_commandes_label.configure(text="Commandes aujourd'hui: erreur")
            dashboard_page.total_ventes_label.configure(text="Total ventes aujourd'hui: erreur")


        
