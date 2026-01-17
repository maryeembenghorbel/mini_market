import customtkinter as ctk
from tkinter import messagebox
from modules.commande import get_commandes_du_vendeur
from modules.facture import generer_facture, generer_pdf_facture
from functools import partial

class CommandesPage(ctk.CTkFrame):

    def __init__(self, parent, user_id):
        super().__init__(parent, fg_color="#0F172A")
        self.user_id = user_id

        ctk.CTkLabel(
            self, text="📋 Liste des commandes",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="#3B82F6"
        ).pack(pady=20)

        self.scroll = ctk.CTkScrollableFrame(self)
        self.scroll.pack(fill="both", expand=True, padx=20, pady=10)

        self.refresh()

    def refresh(self):
        for w in self.scroll.winfo_children():
            w.destroy()

        commandes = get_commandes_du_vendeur(self.user_id)

        if not commandes:
            ctk.CTkLabel(self.scroll, text="Aucune commande").pack(pady=20)
            return

        for c in commandes:
            row = ctk.CTkFrame(self.scroll, fg_color="#1E293B")
            row.pack(fill="x", pady=5, padx=5)

            ctk.CTkLabel(row, text=f"CMD #{c['id']}").pack(side="left", padx=10)
            ctk.CTkLabel(row, text=str(c['date_commande'])).pack(side="left", padx=10)

            # Bouton supprimer facture

            btn_supprimer = ctk.CTkButton(
                row,
                text="Supprimer",
                fg_color="#EF4444",
                command=partial(self.supprimer_commande, c['id'])
            )
            btn_supprimer.pack(side="right", padx=5)



            # Bouton Facture (affiche messagebox)
            btn_facture = ctk.CTkButton(
                row, text="Facture",
                command=partial(self.voir_facture, c['id'])
            )
            btn_facture.pack(side="right", padx=5)

            # Bouton Télécharger PDF
            btn_pdf = ctk.CTkButton(
                row, text="Télécharger PDF",
                width=120,
                fg_color="#3B82F6",
                command=partial(self.telecharger_facture, c['id'])
            )
            btn_pdf.pack(side="right", padx=5)

    def voir_facture(self, id_commande):
        details, total = generer_facture(id_commande)
        
        texte = f"Facture #{id_commande}\n\n"
        for d in details:
            texte += f"{d['nom']} x{d['quantite']} = {d['quantite']*d['prix']} DT\n"
        texte += f"\nTotal: {total} DT"
        messagebox.showinfo("Facture", texte)


    def telecharger_facture(self, id_commande):
        try:
            details, total = generer_facture(id_commande)
            chemin_pdf = generer_pdf_facture(id_commande, details, total)
            messagebox.showinfo("Téléchargé", f"Facture téléchargée : {chemin_pdf}")
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible de générer la facture : {e}")



    def supprimer_commande(self, id_commande):
        confirm = messagebox.askyesno(
            "Confirmation",
            f"Voulez-vous vraiment supprimer la commande #{id_commande} ?\n"
            "Les produits seront remis en stock."
        )

        if not confirm:
            return

        try:
            from modules.commande import supprimer_commande_et_restituer_stock
            supprimer_commande_et_restituer_stock(id_commande)
            messagebox.showinfo("Succès", "Commande supprimée et stock mis à jour.")
            self.refresh()
        except Exception as e:
            messagebox.showerror("Erreur", str(e))
