import customtkinter as ctk
from tkinter import messagebox
from modules.auth import login
# AJOUTER CES IMPORTS pour les dashboards
from gui.admin_dashboard import AdminDashboard  # ou ton chemin
from gui.vendeur_dashboard import VendeurDashboard  # ou ton chemin


# Configuration charte graphique bleu marine / rouge bordeaux
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

# Couleurs personnalisées gestion de stock
COULEURS = {
    "bleu_marine": "#1E3A8A",
    "rouge_bordeaux": "#8B0000",
    "fond": "#0F172A",
    "texte": "#F8FAFC",
    "accent": "#3B82F6",
    "hover": "#1D4ED8"
}

app = ctk.CTk()
app.title("Gestion Stock Pro - Connexion")
app.geometry("450x600")
app.configure(fg_color=COULEURS["fond"])

# Frame centrale stylée
frame = ctk.CTkFrame(
    app, 
    fg_color="transparent",
    corner_radius=25,
    border_width=3,
    border_color=COULEURS["accent"]
)
frame.pack(expand=True, padx=40, pady=40)

# Titre principal
titre = ctk.CTkLabel(
    frame,
    text="🛒 GESTION STOCK PRO",
    font=ctk.CTkFont(size=32, weight="bold"),
    text_color=COULEURS["accent"]
)
titre.pack(pady=(50, 20))

# Sous-titre
sous_titre = ctk.CTkLabel(
    frame,
    text="Interface de connexion sécurisée",
    font=ctk.CTkFont(size=16),
    text_color=COULEURS["texte"]
)
sous_titre.pack(pady=(0, 50))

ctk.CTkLabel(frame, text="👤 Nom d'utilisateur", 
             font=ctk.CTkFont(size=16, weight="bold"),
             text_color=COULEURS["texte"]).pack(pady=5)
username_entry = ctk.CTkEntry(
    frame,
    height=50,
    font=ctk.CTkFont(size=16),
    fg_color="#1E293B",
    border_color=COULEURS["bleu_marine"],
    border_width=2,
    corner_radius=12
)
username_entry.pack(pady=5, padx=40, fill="x")

ctk.CTkLabel(frame, text="🔒 Mot de passe", 
             font=ctk.CTkFont(size=16, weight="bold"),
             text_color=COULEURS["texte"]).pack(pady=20)
password_entry = ctk.CTkEntry(
    frame,
    show="*",
    height=50,
    font=ctk.CTkFont(size=16),
    fg_color="#1E293B",
    border_color=COULEURS["bleu_marine"],
    border_width=2,
    corner_radius=12
)
password_entry.pack(pady=5, padx=40, fill="x")

def on_login():
    username = username_entry.get().strip()
    password = password_entry.get().strip()
    role, user_id = login(username, password)

    if role == "admin":
        messagebox.showinfo("Succès", "Connecté en tant qu'Admin")
        app.withdraw()  # cacher la fenêtre de login
        admin_win = AdminDashboard(user_id=user_id)
        admin_win.mainloop()  # ou juste admin_win.focus() si app tourne déjà

    elif role == "vendeur":
        messagebox.showinfo("Succès", "Connecté en tant que Vendeur")
<<<<<<< HEAD
        # ici tu appelleras plus tard VendeurDashboard(user_id=user_id)
=======
        app.withdraw()
        vendeur_win = VendeurDashboard(user_id=user_id, username=username)
        vendeur_win.mainloop()


>>>>>>> 2b6e9f1 (Add my updates to mini_market project)

    else:
        messagebox.showerror("Erreur", "Nom d'utilisateur ou mot de passe incorrect")

ctk.CTkButton(
    frame, 
    text="🚀 SE CONNECTER", 
    command=on_login,
    height=55,
    font=ctk.CTkFont(size=18, weight="bold"),
    fg_color=COULEURS["rouge_bordeaux"],
    hover_color=COULEURS["accent"],
    text_color="white",
    corner_radius=15
).pack(pady=40, padx=50, fill="x")

app.mainloop()
