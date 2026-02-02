import tkinter as tk
from tkinter import ttk


class DashboardUI:
    
    def __init__(self, parent, stats_mgr, rappel_mgr):
        self.parent = parent
        self.stats_mgr = stats_mgr
        self.rappel_mgr = rappel_mgr
    
    def create_dashboard_tab(self, notebook):
        tab = ttk.Frame(notebook, padding="15")
        notebook.add(tab, text="Tableau de bord")
        
        ttk.Label(tab, text="Tableau de bord", style="Title.TLabel", font=("", 16, "bold")).pack(pady=(0, 20))
        
        stats_frame = ttk.LabelFrame(tab, text="Statistiques rapides", padding="10")
        stats_frame.pack(fill=tk.X, pady=(0, 10))
        
        stats = self.stats_mgr.get_global_statistics()
        
        stats_grid = ttk.Frame(stats_frame)
        stats_grid.pack(fill=tk.X)
        
        row = 0
        col = 0
        for key, value in stats.items():
            label = key.replace('_', ' ').title()
            
            card = ttk.Frame(stats_grid, relief=tk.RAISED, borderwidth=1)
            card.grid(row=row, column=col, padx=5, pady=5, sticky=(tk.W, tk.E))
            
            ttk.Label(card, text=str(value), font=("", 20, "bold")).pack(pady=(5, 0))
            ttk.Label(card, text=label, font=("", 9)).pack(pady=(0, 5))
            
            col += 1
            if col > 3:
                col = 0
                row += 1
        
        rappels_frame = ttk.LabelFrame(tab, text="Rappels d'aujourd'hui", padding="10")
        rappels_frame.pack(fill=tk.BOTH, expand=True, pady=(10, 0))
        
        rappels = self.rappel_mgr.get_rappels_aujourdhui()
        
        if rappels:
            rappels_tree = ttk.Treeview(
                rappels_frame,
                columns=("id", "contact", "titre", "heure", "priorite"),
                show="headings",
                height=8
            )
            
            rappels_tree.heading("id", text="ID")
            rappels_tree.heading("contact", text="Contact")
            rappels_tree.heading("titre", text="Titre")
            rappels_tree.heading("heure", text="Heure")
            rappels_tree.heading("priorite", text="Priorité")
            
            rappels_tree.column("id", width=50)
            rappels_tree.column("contact", width=150)
            rappels_tree.column("titre", width=200)
            rappels_tree.column("heure", width=100)
            rappels_tree.column("priorite", width=100)
            
            for rappel in rappels:
                contact_name = f"{rappel['prenom']} {rappel['nom']}"
                rappels_tree.insert("", "end", values=(
                    rappel['id'],
                    contact_name,
                    rappel['titre'],
                    rappel['date_heure'],
                    rappel['priorite']
                ))
            
            rappels_tree.pack(fill=tk.BOTH, expand=True)
        else:
            ttk.Label(rappels_frame, text="Aucun rappel pour aujourd'hui").pack()
