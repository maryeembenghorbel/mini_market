import customtkinter as ctk
from tkinter import messagebox, simpledialog
from database.db_connection import get_connection
from modules.commande import creer_commande, ajouter_detail_commande

class NouvelleCommandePage(ctk.CTkFrame):

    def __init__(self, parent, user_id):
        super().__init__(parent, fg_color="#0F172A")
        self.user_id = user_id
        self.id_commande = None
        self.panier = []  # Produits ajoutés

        self.create_widgets()

    def create_widgets(self):
        ctk.CTkLabel(
            self,
            text="🧾 Création de commande",
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color="#3B82F6"
        ).pack(pady=15)

        self.btn_creer = ctk.CTkButton(
            self,
            text="Créer une commande",
            command=self.creer_commande
        )
        self.btn_creer.pack(pady=10)

        self.produits_scroll = ctk.CTkScrollableFrame(self)
        self.produits_scroll.pack(fill="both", expand=True, padx=20, pady=10)

        self.btn_valider = ctk.CTkButton(
            self,
            text="Ajouter la commande",
            fg_color="#10B981",
            command=self.valider_commande,
            state="disabled"
        )
        self.btn_valider.pack(pady=15)

    # 1️⃣ Création de la commande
    def creer_commande(self):
        self.id_commande = creer_commande(self.user_id)
        self.btn_creer.configure(state="disabled")
        self.btn_valider.configure(state="normal")
        self.load_produits()

    # 2️⃣ Chargement produits + stock
    def load_produits(self):
        for w in self.produits_scroll.winfo_children():
            w.destroy()

        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id, nom, prix, quantite FROM produits WHERE quantite > 0")
        produits = cursor.fetchall()
        conn.close()

        for p in produits:
            frame = ctk.CTkFrame(self.produits_scroll, fg_color="#1E293B")
            frame.pack(fill="x", pady=5)

            ctk.CTkLabel(frame, text=p['nom']).pack(side="left", padx=10)
            ctk.CTkLabel(frame, text=f"Stock: {p['quantite']}").pack(side="left", padx=10)
            ctk.CTkLabel(frame, text=f"{p['prix']} DT").pack(side="left", padx=10)

            ctk.CTkButton(
                frame,
                text="Ajouter",
                command=lambda prod=p: self.ajouter_produit(prod)
            ).pack(side="right", padx=10)

    # 3️⃣ Ajouter produit au panier
    def ajouter_produit(self, produit):
        qte = simpledialog.askinteger(
            "Quantité",
            f"Quantité pour {produit['nom']} ?",
            minvalue=1,
            maxvalue=produit['quantite']
        )
        if not qte:
            return

        self.panier.append({
            "id": produit['id'],
            "nom": produit['nom'],
            "quantite": qte,
            "prix": produit['prix']
        })

        messagebox.showinfo("Ajouté", f"{produit['nom']} ajouté à la commande")

    # 4️⃣ Validation finale
    def valider_commande(self):
        if not self.panier:
            messagebox.showwarning("Attention", "Aucun produit ajouté")
            return

        for item in self.panier:
            ajouter_detail_commande(
                self.id_commande,
                item['id'],
                item['quantite'],
                item['prix']
            )

        messagebox.showinfo("Succès", f"Commande #{self.id_commande} enregistrée")

        # Reset
        self.panier.clear()
        self.btn_creer.configure(state="normal")
        self.btn_valider.configure(state="disabled")
        self.id_commande = None

        for w in self.produits_scroll.winfo_children():
            w.destroy()
