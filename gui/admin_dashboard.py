
import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime
from modules.admin_service import (
    total_produits,
    produits_en_rupture,
    commandes_aujourdhui,
    chiffre_affaires_jour
)


COULEURS = {
    "fond": "#0F172A",
    "sidebar": "#020617",
    "topbar": "#020617",
    "carte": "#111827",
    "texte": "#F8FAFC",
    "accent": "#3B82F6",
    "rouge": "#8B0000"
}

class AdminDashboard(ctk.CTkToplevel):
    def __init__(self, user_id=None):
        super().__init__()
        self.title("Dashboard Administrateur - Mini-Market")
        self.geometry("1200x700")
        self.configure(fg_color=COULEURS["fond"])
        self.user_id = user_id

        # === TOPBAR ===
        self.topbar = ctk.CTkFrame(self, height=60, fg_color=COULEURS["topbar"])
        self.topbar.pack(side="top", fill="x")

        ctk.CTkLabel(
            self.topbar,
            text="🛒 Dashboard Administrateur",
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color=COULEURS["texte"]
        ).pack(side="left", padx=20)

        self.date_label = ctk.CTkLabel(
            self.topbar,
            text=self._get_date_text(),
            font=ctk.CTkFont(size=14),
            text_color=COULEURS["texte"]
        )
        self.date_label.pack(side="right", padx=20)

        self.logout_btn = ctk.CTkButton(
            self.topbar,
            text="⏻ Déconnexion",
            fg_color=COULEURS["rouge"],
            hover_color="#b91c1c",
            width=130,
            command=self.on_logout
        )
        self.logout_btn.pack(side="right", padx=10, pady=10)

        # === SIDEBAR (NAVBAR GAUCHE) ===
        self.sidebar = ctk.CTkFrame(self, width=220, fg_color=COULEURS["sidebar"])
        self.sidebar.pack(side="left", fill="y")

        ctk.CTkLabel(
            self.sidebar,
            text="ADMIN",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=COULEURS["accent"]
        ).pack(pady=(20, 10))

        self._add_nav_button("🏠 Tableau de bord", self.show_dashboard)
        self._add_nav_button("📦 Produits", self.show_produits)
        self._add_nav_button("🧾 Factures", self.show_factures)
        self._add_nav_button("🛍️ Commandes", self.show_commandes)
        self._add_nav_button("📊 Statistiques", self.show_stats)

        # === CONTENU CENTRAL ===
        self.content = ctk.CTkFrame(self, fg_color=COULEURS["fond"])
        self.content.pack(side="left", fill="both", expand=True)

        # Vue par défaut
        self.show_dashboard()

    # ---------- Helpers UI ----------

    def _add_nav_button(self, text, command):
        btn = ctk.CTkButton(
            self.sidebar,
            text=text,
            anchor="w",
            fg_color="transparent",
            hover_color="#111827",
            text_color=COULEURS["texte"],
            font=ctk.CTkFont(size=15),
            command=command
        )
        btn.pack(fill="x", padx=10, pady=4)

    def _clear_content(self):
        for w in self.content.winfo_children():
            w.destroy()

    def _get_date_text(self):
        return datetime.now().strftime("📅 %d/%m/%Y  ⏰ %H:%M")

    # ---------- Actions ----------

    def on_logout(self):
        self.destroy()  # tu peux ici réafficher la fenêtre de login si tu veux

    # ---------- Vues centre ----------

    def show_dashboard(self):
        def show_dashboard(self):
            self._clear_content()

        title = ctk.CTkLabel(
            self.content,
            text="Tableau de bord",
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color=COULEURS["texte"]
        )
        title.pack(pady=20, anchor="w", padx=20)

        cards_frame = ctk.CTkFrame(self.content, fg_color=COULEURS["fond"])
        cards_frame.pack(fill="x", padx=20)

        self._create_stat_card(
            cards_frame,
            "Produits totaux",
            str(total_produits())
        )

        self._create_stat_card(
            cards_frame,
            "Produits en rupture",
            str(produits_en_rupture())
        )

        self._create_stat_card(
            cards_frame,
            "Commandes aujourd'hui",
            str(commandes_aujourdhui())
        )

        self._create_stat_card(
            cards_frame,
            "CA du jour",
            f"{chiffre_affaires_jour()} DT"
        )


    def _create_stat_card(self, parent, label, value):
        card = ctk.CTkFrame(parent, fg_color=COULEURS["carte"], corner_radius=12)
        card.pack(side="left", expand=True, fill="both", padx=8, pady=8)

        ctk.CTkLabel(
            card,
            text=label,
            font=ctk.CTkFont(size=14),
            text_color="#9CA3AF"
        ).pack(pady=(10, 4), anchor="w", padx=10)

        ctk.CTkLabel(
            card,
            text=value,
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color=COULEURS["texte"]
        ).pack(pady=(0, 10), anchor="w", padx=10)

    def show_produits(self):
        self._clear_content()
        ctk.CTkLabel(
            self.content,
            text="📦 Gestion des produits",
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color=COULEURS["texte"]
        ).pack(pady=20, anchor="w", padx=20)
        # ici tu ajouteras table + formulaire produit

    def show_factures(self):
        self._clear_content()
        ctk.CTkLabel(
            self.content,
            text="🧾 Factures",
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color=COULEURS["texte"]
        ).pack(pady=20, anchor="w", padx=20)

    def show_commandes(self):
        self._clear_content()
        ctk.CTkLabel(
            self.content,
            text="🛍️ Commandes",
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color=COULEURS["texte"]
        ).pack(pady=20, anchor="w", padx=20)

    def show_stats(self):
        self._clear_content()
        ctk.CTkLabel(
            self.content,
            text="📊 Statistiques",
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color=COULEURS["texte"]
        ).pack(pady=20, anchor="w", padx=20)
