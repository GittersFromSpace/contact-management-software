import tkinter as tk
from tkinter import ttk, messagebox


class RappelUI:
    
    def __init__(self, root, rappel_mgr, contact_mgr):
        self.root = root
        self.rappel_mgr = rappel_mgr
        self.contact_mgr = contact_mgr
        self.rappels_tree = None
    
    def create_rappels_tab(self, notebook):
        tab = ttk.Frame(notebook, padding="15")
        notebook.add(tab, text="Rappels")

        ttk.Label(tab, text="Gestion des Rappels", style="Title.TLabel").pack(pady=(0, 15))

        btn_frame = ttk.Frame(tab)
        btn_frame.pack(fill=tk.X, pady=(0, 10))

        ttk.Button(btn_frame, text="Nouveau rappel", command=self.add_rappel, style="Accent.TButton").pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Marquer traité", command=self.mark_rappel_done, style="Success.TButton").pack(side=tk.LEFT, padx=5)

        list_frame = ttk.Frame(tab)
        list_frame.pack(fill=tk.BOTH, expand=True)

        vsb = ttk.Scrollbar(list_frame, orient="vertical")
        hsb = ttk.Scrollbar(list_frame, orient="horizontal")

        self.rappels_tree = ttk.Treeview(
            list_frame,
            columns=("id", "contact", "titre", "date", "priorite", "traite"),
            show="headings",
            yscrollcommand=vsb.set,
            xscrollcommand=hsb.set,
            height=18
        )

        vsb.config(command=self.rappels_tree.yview)
        hsb.config(command=self.rappels_tree.xview)

        self.rappels_tree.heading("id", text="ID")
        self.rappels_tree.heading("contact", text="Contact")
        self.rappels_tree.heading("titre", text="Titre")
        self.rappels_tree.heading("date", text="Date/Heure")
        self.rappels_tree.heading("priorite", text="Priorité")
        self.rappels_tree.heading("traite", text="Traité")

        self.rappels_tree.column("id", width=60, minwidth=40, stretch=False)
        self.rappels_tree.column("contact", width=180, minwidth=100, stretch=True)
        self.rappels_tree.column("titre", width=400, minwidth=150, stretch=True)
        self.rappels_tree.column("date", width=180, minwidth=100, stretch=True)
        self.rappels_tree.column("priorite", width=120, minwidth=80, stretch=True)
        self.rappels_tree.column("traite", width=100, minwidth=60, stretch=True)

        self.rappels_tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")

        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(0, weight=1)

        self.load_rappels()
    
    def add_rappel(self):
        win = tk.Toplevel(self.root)
        win.title("Nouveau rappel")
        win.geometry("750x650")
        win.minsize(650, 550)
        win.minsize(520, 420)
        win.transient(self.root)
        win.grab_set()

        frm = ttk.Frame(win, padding=24)
        frm.grid(row=0, column=0, sticky="nsew")

        win.grid_rowconfigure(0, weight=1)
        win.grid_columnconfigure(0, weight=1)
        for i in range(10):
            frm.grid_rowconfigure(i, weight=1)
        frm.grid_columnconfigure(0, weight=1)

        ttk.Label(frm, text="Créer un nouveau rappel", font=("", 15, "bold")).grid(row=0, column=0, pady=(0, 18), sticky="nsew")

        contacts = self.contact_mgr.get_all_contacts()
        contact_names = [f"{c['prenom']} {c['nom']} (id:{c['id']})" for c in contacts]
        contact_ids = [c['id'] for c in contacts]
        contact_var = tk.StringVar()
        ttk.Label(frm, text="Contact :", font=("", 11, "bold")).grid(row=1, column=0, sticky="w", pady=(0, 2))
        contact_combo = ttk.Combobox(frm, values=contact_names, textvariable=contact_var, state="readonly", font=("", 11))
        contact_combo.grid(row=2, column=0, sticky="ew", pady=(0, 10))
        if contact_names:
            contact_combo.current(0)

        titre_var = tk.StringVar()
        ttk.Label(frm, text="Titre :", font=("", 11, "bold")).grid(row=3, column=0, sticky="w", pady=(0, 2))
        titre_entry = ttk.Entry(frm, textvariable=titre_var, font=("", 11))
        titre_entry.grid(row=4, column=0, sticky="ew", pady=(0, 10))

        date_var = tk.StringVar()
        ttk.Label(frm, text="Date/Heure (YYYY-MM-DD HH:MM):", font=("", 11, "bold")).grid(row=5, column=0, sticky="w", pady=(0, 2))
        date_entry = ttk.Entry(frm, textvariable=date_var, font=("", 11))
        date_entry.grid(row=6, column=0, sticky="ew", pady=(0, 10))

        priorite_var = tk.StringVar()
        ttk.Label(frm, text="Priorité :", font=("", 11, "bold")).grid(row=7, column=0, sticky="w", pady=(0, 2))
        priorite_combo = ttk.Combobox(frm, values=["Haute", "Moyenne", "Basse"], textvariable=priorite_var, state="readonly", font=("", 11))
        priorite_combo.grid(row=8, column=0, sticky="ew", pady=(0, 10))
        priorite_combo.current(1)

        def submit():
            idx = contact_combo.current()
            if idx < 0:
                messagebox.showerror("Erreur", "Veuillez sélectionner un contact", parent=win)
                return
            contact_id = contact_ids[idx]
            titre = titre_var.get().strip()
            date_heure = date_var.get().strip()
            priorite = priorite_var.get().strip()
            if not titre or not date_heure:
                messagebox.showerror("Erreur", "Titre et date obligatoires", parent=win)
                return
            self.rappel_mgr.create_rappel(contact_id, titre, date_heure, priorite=priorite)
            self.load_rappels()
            win.destroy()

        btn = ttk.Button(frm, text="Créer le rappel", command=submit, style="Accent.TButton")
        btn.grid(row=9, column=0, pady=(18, 0), sticky="ew")
    
    def mark_rappel_done(self):
        messagebox.showinfo("Info", "Fonctionnalité en développement", parent=self.root)
    
    def load_rappels(self):
        if not self.rappels_tree:
            return
            
        for item in self.rappels_tree.get_children():
            self.rappels_tree.delete(item)
        
        rappels = self.rappel_mgr.get_rappels()
        
        if rappels:
            for rappel in rappels:
                contact_name = f"{rappel['prenom']} {rappel['nom']}"
                self.rappels_tree.insert("", "end", values=(
                    rappel['id'],
                    contact_name,
                    rappel['titre'],
                    rappel['date_heure'],
                    rappel['priorite'] or '',
                    "Oui" if rappel['traite'] else "Non"
                ))
