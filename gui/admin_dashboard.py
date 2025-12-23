import customtkinter as ctk
from tkinter import messagebox, filedialog
from datetime import datetime
import tkinter.ttk as ttk
from PIL import Image

from modules.admin_service import (
    total_produits,
    produits_en_rupture,
    commandes_aujourdhui,
    chiffre_affaires_jour,
)
from modules.produits import (
    get_all_products,
    create_product,
    update_product,
    delete_product,
    product_exists_by_name,
)

COULEURS = {
    "fond": "#0F172A",
    "sidebar": "#020617",
    "topbar": "#020617",
    "carte": "#111827",
    "texte": "#F8FAFC",
    "accent": "#3B82F6",
    "rouge": "#8B0000",
}


class AdminDashboard(ctk.CTkToplevel):

    def __init__(self, user_id=None):
        super().__init__()

        self.title("Dashboard Administrateur - Mini-Market")
        self.geometry("1200x700")
        self.configure(fg_color=COULEURS["fond"])

        self.user_id = user_id

        # catégories disponibles
        self.categories_dispo = ["Alimentaire", "Fourniture", "Tech"]

        # ---------- TOPBAR ----------
        self._build_topbar()

        # ---------- SIDEBAR ----------
        self._build_sidebar()

        # ---------- CONTENU CENTRAL ----------
        self.content = ctk.CTkFrame(self, fg_color=COULEURS["fond"])
        self.content.pack(side="left", fill="both", expand=True)

        # Vue par défaut
        self.show_dashboard()

    # ==================================================
    # UI BUILDERS
    # ==================================================

    def _build_topbar(self):
        self.topbar = ctk.CTkFrame(self, height=60, fg_color=COULEURS["topbar"])
        self.topbar.pack(side="top", fill="x")

        ctk.CTkLabel(
            self.topbar,
            text="Dashboard Administrateur",
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color=COULEURS["texte"],
        ).pack(side="left", padx=20)

        self.date_label = ctk.CTkLabel(
            self.topbar,
            text=self._get_date_text(),
            font=ctk.CTkFont(size=14),
            text_color=COULEURS["texte"],
        )
        self.date_label.pack(side="right", padx=20)

        ctk.CTkButton(
            self.topbar,
            text="Déconnexion",
            fg_color=COULEURS["rouge"],
            hover_color="#b91c1c",
            width=120,
            command=self.on_logout,
        ).pack(side="right", padx=10)

    def _build_sidebar(self):
        self.sidebar = ctk.CTkFrame(self, width=220, fg_color=COULEURS["sidebar"])
        self.sidebar.pack(side="left", fill="y")

        ctk.CTkLabel(
            self.sidebar,
            text="ADMIN",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=COULEURS["accent"],
        ).pack(pady=(20, 10))

        self._add_nav_button("🏠 Tableau de bord", self.show_dashboard)
        self._add_nav_button("📦 Produits", self.show_produits)
        self._add_nav_button("🧾 Factures", self.show_factures)
        self._add_nav_button("🛍️ Commandes", self.show_commandes)
        self._add_nav_button("📊 Statistiques", self.show_stats)

    def _add_nav_button(self, text, command):
        btn = ctk.CTkButton(
            self.sidebar,
            text=text,
            anchor="w",
            fg_color="transparent",
            hover_color="#111827",
            text_color=COULEURS["texte"],
            font=ctk.CTkFont(size=15),
            command=command,
        )
        btn.pack(fill="x", padx=10, pady=4)

    def _clear_content(self):
        for w in self.content.winfo_children():
            w.destroy()

    def _get_date_text(self):
        return datetime.now().strftime("%d/%m/%Y  %H:%M")

    # ==================================================
    # ACTIONS
    # ==================================================

    def on_logout(self):
        self.destroy()

    # ==================================================
    # VUES
    # ==================================================

    def show_dashboard(self):
        self._clear_content()

        title = ctk.CTkLabel(
            self.content,
            text="Tableau de bord",
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color=COULEURS["texte"],
        )
        title.pack(pady=20, anchor="w", padx=20)

        cards = ctk.CTkFrame(self.content, fg_color=COULEURS["fond"])
        cards.pack(fill="x", padx=20)

        self._create_stat_card(cards, "Produits totaux", total_produits())
        self._create_stat_card(cards, "Produits en rupture", produits_en_rupture())
        self._create_stat_card(cards, "Commandes aujourd'hui", commandes_aujourdhui())
        self._create_stat_card(cards, "CA du jour", f"{chiffre_affaires_jour()} DT")

    def _create_stat_card(self, parent, label, value):
        card = ctk.CTkFrame(parent, fg_color=COULEURS["carte"], corner_radius=12)
        card.pack(side="left", expand=True, fill="both", padx=8, pady=8)

        ctk.CTkLabel(
            card,
            text=label,
            font=ctk.CTkFont(size=14),
            text_color="#9CA3AF",
        ).pack(pady=(10, 4), anchor="w", padx=10)

        ctk.CTkLabel(
            card,
            text=value,
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color=COULEURS["texte"],
        ).pack(pady=(0, 10), anchor="w", padx=10)

    # ---------- PAGE PRODUITS ----------

    def show_produits(self):
        self._clear_content()

        title = ctk.CTkLabel(
            self.content,
            text="Gestion des Produits",
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color=COULEURS["texte"],
        )
        title.pack(anchor="w", padx=20, pady=10)

        main = ctk.CTkFrame(self.content, fg_color=COULEURS["fond"])
        main.pack(fill="both", expand=True, padx=20, pady=10)

        # ================= TABLE PRODUITS =================
        table_frame = ctk.CTkFrame(main, fg_color=COULEURS["fond"])
        table_frame.pack(side="left", fill="both", expand=True, padx=(0, 15))

        columns = ("id", "nom", "categorie", "prix", "quantite")
        self.prod_tree = ttk.Treeview(
            table_frame, columns=columns, show="headings", height=15
        )

        self.prod_tree.heading("id", text="ID")
        self.prod_tree.heading("nom", text="Nom")
        self.prod_tree.heading("categorie", text="Catégorie")
        self.prod_tree.heading("prix", text="Prix")
        self.prod_tree.heading("quantite", text="Qté")

        self.prod_tree.column("id", width=50)
        self.prod_tree.column("nom", width=150)
        self.prod_tree.column("categorie", width=120)
        self.prod_tree.column("prix", width=80)
        self.prod_tree.column("quantite", width=80)

        self.prod_tree.pack(fill="both", expand=True)
        self.prod_tree.bind("<<TreeviewSelect>>", self.on_select_product)

        # ================= FORMULAIRE (scrollable) =================
        form = ctk.CTkScrollableFrame(
            main,
            width=320,
            fg_color=COULEURS["carte"]
        )
        form.pack(side="right", fill="both", expand=True, padx=(0, 5), pady=5)

        ctk.CTkLabel(
            form,
            text="Détail du produit",
            font=ctk.CTkFont(size=18, weight="bold"),
        ).pack(pady=(10, 5))

        self.var_id = ctk.StringVar()
        self.var_nom = ctk.StringVar()
        self.var_categorie = ctk.StringVar()
        self.var_prix = ctk.StringVar()
        self.var_quantite = ctk.StringVar()
        self.var_image_path = ctk.StringVar()
        self.var_date_creation = ctk.StringVar()

        # Nom
        ctk.CTkLabel(form, text="Nom *").pack(anchor="w", padx=10, pady=(8, 0))
        ctk.CTkEntry(
            form,
            textvariable=self.var_nom,
            placeholder_text="Ex : Lait demi-écrémé"
        ).pack(fill="x", pady=3, padx=10)

        # Catégorie
        ctk.CTkLabel(form, text="Catégorie *").pack(anchor="w", padx=10, pady=(8, 0))
        self.categorie_combo = ctk.CTkComboBox(
            form,
            values=self.categories_dispo,
            variable=self.var_categorie,
        )
        self.categorie_combo.pack(fill="x", pady=3, padx=10)
        if self.categories_dispo:
            self.categorie_combo.set(self.categories_dispo[0])

        # Prix
        ctk.CTkLabel(form, text="Prix (DT) *").pack(anchor="w", padx=10, pady=(8, 0))
        ctk.CTkEntry(
            form,
            textvariable=self.var_prix,
            placeholder_text="Ex : 3.500"
        ).pack(fill="x", pady=3, padx=10)

        # Quantité
        ctk.CTkLabel(form, text="Quantité *").pack(anchor="w", padx=10, pady=(8, 0))
        ctk.CTkEntry(
            form,
            textvariable=self.var_quantite,
            placeholder_text="Ex : 20"
        ).pack(fill="x", pady=3, padx=10)

        # Date création (lecture seule)
        ctk.CTkLabel(form, text="Créé le").pack(anchor="w", padx=10, pady=(8, 0))
        ctk.CTkLabel(
            form,
            textvariable=self.var_date_creation,
            text_color="#9CA3AF",
        ).pack(anchor="w", padx=10)

        # Image
        ctk.CTkLabel(form, text="Image").pack(anchor="w", padx=10, pady=(8, 0))

        img_frame = ctk.CTkFrame(form, fg_color="transparent")
        img_frame.pack(fill="x", pady=3, padx=10)

        ctk.CTkEntry(
            img_frame,
            textvariable=self.var_image_path,
            placeholder_text="Chemin image"
        ).pack(side="left", fill="x", expand=True)

        ctk.CTkButton(
            img_frame,
            text="📁",
            width=40,
            command=self.browse_image
        ).pack(side="right")

        self.img_label = ctk.CTkLabel(
            form,
            text="(Aucune image)",
            height=100
        )
        self.img_label.pack(pady=10)

        # Boutons
        btn_frame = ctk.CTkFrame(form, fg_color="transparent")
        btn_frame.pack(fill="x", padx=10, pady=10)

        ctk.CTkButton(
            btn_frame,
            text="Ajouter",
            command=self.add_product
        ).pack(fill="x", pady=3)

        ctk.CTkButton(
            btn_frame,
            text="Modifier",
            command=self.update_product
        ).pack(fill="x", pady=3)

        ctk.CTkButton(
            btn_frame,
            text="Supprimer",
            fg_color=COULEURS["rouge"],
            hover_color="#991B1B",
            command=self.delete_product
        ).pack(fill="x", pady=3)

        self.load_products_into_table()

    # ================= MÉTHODES PRODUITS =================

    def clear_form(self):
        self.var_id.set("")
        self.var_nom.set("")
        self.var_categorie.set("")
        self.var_prix.set("")
        self.var_quantite.set("")
        self.var_image_path.set("")
        self.var_date_creation.set("")
        self.img_label.configure(text="(Aucune image)", image=None)

    def load_products_into_table(self):
        for row in self.prod_tree.get_children():
            self.prod_tree.delete(row)
        for p in get_all_products():
            self.prod_tree.insert("", "end", values=p[:5])

    def on_select_product(self, event):
        selected = self.prod_tree.focus()
        if not selected:
            return
        values = self.prod_tree.item(selected, "values")
        self.var_id.set(values[0])
        self.var_nom.set(values[1])
        self.var_categorie.set(values[2])
        self.var_prix.set(values[3])
        self.var_quantite.set(values[4])

        for p in get_all_products():
            if str(p[0]) == str(values[0]):
                self.var_image_path.set(p[5] or "")
                self.var_date_creation.set(p[6])
                if p[5]:
                    self.show_product_image(p[5])
                else:
                    self.img_label.configure(text="(Aucune image)", image=None)
                break

    def browse_image(self):
        path = filedialog.askopenfilename(
            filetypes=[("Images", "*.png *.jpg *.jpeg")]
        )
        if path:
            self.var_image_path.set(path)
            self.show_product_image(path)

    def show_product_image(self, path):
        try:
            img = Image.open(path)
            img = img.resize((150, 150))
            self.ctk_img = ctk.CTkImage(img, size=(150, 150))
            self.img_label.configure(image=self.ctk_img, text="")
        except Exception:
            self.img_label.configure(text="Image introuvable", image=None)

    def add_product(self):
        nom = self.var_nom.get().strip()
        categorie = self.var_categorie.get().strip()
        prix_txt = self.var_prix.get().strip()
        qte_txt = self.var_quantite.get().strip()
        image = self.var_image_path.get().strip()

        if not nom or not categorie or not prix_txt or not qte_txt:
            messagebox.showwarning(
                "Attention", "Les champs marqués * sont obligatoires."
            )
            return

        if product_exists_by_name(nom):
            messagebox.showwarning(
                "Attention",
                "Un produit avec ce nom existe déjà."
            )
            return

        try:
            prix = float(prix_txt)
            if prix < 0:
                raise ValueError
        except ValueError:
            messagebox.showwarning(
                "Attention", "Le prix doit être un nombre positif."
            )
            return

        try:
            quantite = int(qte_txt)
            if quantite < 0:
                raise ValueError
        except ValueError:
            messagebox.showwarning(
                "Attention", "La quantité doit être un entier positif."
            )
            return

        create_product(nom, categorie, prix, quantite, image)
        self.load_products_into_table()
        self.clear_form()

    def update_product(self):
        if not self.var_id.get():
            messagebox.showwarning("Attention", "Sélectionnez un produit")
            return

        nom = self.var_nom.get().strip()
        categorie = self.var_categorie.get().strip()
        prix_txt = self.var_prix.get().strip()
        qte_txt = self.var_quantite.get().strip()
        image = self.var_image_path.get().strip()

        if not nom or not categorie or not prix_txt or not qte_txt:
            messagebox.showwarning(
                "Attention", "Les champs marqués * sont obligatoires."
            )
            return

        try:
            prix = float(prix_txt)
            if prix < 0:
                raise ValueError
        except ValueError:
            messagebox.showwarning(
                "Attention", "Le prix doit être un nombre positif."
            )
            return

        try:
            quantite = int(qte_txt)
            if quantite < 0:
                raise ValueError
        except ValueError:
            messagebox.showwarning(
                "Attention", "La quantité doit être un entier positif."
            )
            return

        update_product(
            int(self.var_id.get()),
            nom,
            categorie,
            prix,
            quantite,
            image,
        )
        self.load_products_into_table()
        self.clear_form()

    def delete_product(self):
        if not self.var_id.get():
            messagebox.showwarning("Attention", "Sélectionnez un produit")
            return
        if messagebox.askyesno("Confirmation", "Supprimer ce produit ?"):
            delete_product(int(self.var_id.get()))
            self.load_products_into_table()
            self.clear_form()

    # ---------- AUTRES PAGES ----------

    def show_factures(self):
        self._clear_content()
        ctk.CTkLabel(
            self.content,
            text="Factures",
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color=COULEURS["texte"],
        ).pack(pady=20, anchor="w", padx=20)

    def show_commandes(self):
        self._clear_content()
        ctk.CTkLabel(
            self.content,
            text="Commandes",
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color=COULEURS["texte"],
        ).pack(pady=20, anchor="w", padx=20)

    def show_stats(self):
        self._clear_content()
        ctk.CTkLabel(
            self.content,
            text="Statistiques",
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color=COULEURS["texte"],
        ).pack(pady=20, anchor="w", padx=20)


if __name__ == "__main__":
    app = ctk.CTk()
    app.withdraw()
    AdminDashboard()
    app.mainloop()
