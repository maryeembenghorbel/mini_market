import customtkinter as ctk

class VendeurDashboard(ctk.CTkToplevel):
    def __init__(self):
        super().__init__()
        self.title("Dashboard Vendeur")
        self.geometry("900x700")
        self.configure(fg_color="#0F172A")
        
        ctk.CTkLabel(self, text="🛒 DASHBOARD VENDEUR", 
                    font=ctk.CTkFont(size=32, weight="bold")).pack(pady=50)
        ctk.CTkLabel(self, text="Fonctionnalités à venir :\n- Ventes\n- Stock\n- Commandes", 
                    font=ctk.CTkFont(size=18)).pack(pady=20)
