import tkinter as tk
from tkinter import ttk, messagebox


class InteractionUI:
    
    def __init__(self, root, interaction_mgr, contact_mgr):
        self.root = root
        self.interaction_mgr = interaction_mgr
        self.contact_mgr = contact_mgr
        self.interactions_tree = None
    
    def create_interactions_tab(self, notebook):
        tab = ttk.Frame(notebook, padding="15")
        notebook.add(tab, text="💬 Interactions")

        ttk.Label(tab, text="Gestion des Interactions", style="Title.TLabel").pack(pady=(0, 15))

        btn_frame = ttk.Frame(tab)
        btn_frame.pack(fill=tk.X, pady=(0, 10))

        ttk.Button(btn_frame, text="➕ Nouvelle interaction", command=self.add_interaction).pack(side=tk.LEFT, padx=5)

        list_frame = ttk.Frame(tab)
        list_frame.pack(fill=tk.BOTH, expand=True)

        vsb = ttk.Scrollbar(list_frame, orient="vertical")
        hsb = ttk.Scrollbar(list_frame, orient="horizontal")

        self.interactions_tree = ttk.Treeview(
            list_frame,
            columns=("id", "contact", "type", "date", "description"),
            show="headings",
            yscrollcommand=vsb.set,
            xscrollcommand=hsb.set,
            height=18
        )

        vsb.config(command=self.interactions_tree.yview)
        hsb.config(command=self.interactions_tree.xview)

        self.interactions_tree.heading("id", text="ID")
        self.interactions_tree.heading("contact", text="Contact")
        self.interactions_tree.heading("type", text="Type")
        self.interactions_tree.heading("date", text="Date")
        self.interactions_tree.heading("description", text="Description")

        self.interactions_tree.column("id", width=60, minwidth=40, stretch=False)
        self.interactions_tree.column("contact", width=180, minwidth=100, stretch=True)
        self.interactions_tree.column("type", width=120, minwidth=80, stretch=True)
        self.interactions_tree.column("date", width=160, minwidth=100, stretch=True)
        self.interactions_tree.column("description", width=600, minwidth=200, stretch=True)

        self.interactions_tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")

        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(0, weight=1)

        self.load_interactions()
    
    def add_interaction(self):
        win = tk.Toplevel(self.root)
        win.title("Nouvelle interaction")
        win.geometry("700x600")
        win.minsize(600, 500)
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

        title = ttk.Label(frm, text="Créer une nouvelle interaction", font=("", 15, "bold"))
        title.grid(row=0, column=0, pady=(0, 18), sticky="nsew")

        contacts = self.contact_mgr.get_all_contacts()
        contact_names = [f"{c['prenom']} {c['nom']} (id:{c['id']})" for c in contacts]
        contact_ids = [c['id'] for c in contacts]
        contact_var = tk.StringVar()
        ttk.Label(frm, text="Contact :", font=("", 11, "bold")).grid(row=1, column=0, sticky="w", pady=(0, 2))
        contact_combo = ttk.Combobox(frm, values=contact_names, textvariable=contact_var, state="readonly", font=("", 11))
        contact_combo.grid(row=2, column=0, sticky="ew", pady=(0, 10))
        if contact_names:
            contact_combo.current(0)

        type_var = tk.StringVar()
        ttk.Label(frm, text="Type d'interaction :", font=("", 11, "bold")).grid(row=3, column=0, sticky="w", pady=(0, 2))
        type_entry = ttk.Entry(frm, textvariable=type_var, font=("", 11))
        type_entry.grid(row=4, column=0, sticky="ew", pady=(0, 10))

        desc_var = tk.StringVar()
        ttk.Label(frm, text="Description :", font=("", 11, "bold")).grid(row=5, column=0, sticky="w", pady=(0, 2))
        desc_entry = ttk.Entry(frm, textvariable=desc_var, font=("", 11))
        desc_entry.grid(row=6, column=0, sticky="ew", pady=(0, 10))

        statut_var = tk.StringVar()
        ttk.Label(frm, text="Statut :", font=("", 11, "bold")).grid(row=7, column=0, sticky="w", pady=(0, 2))
        statut_entry = ttk.Entry(frm, textvariable=statut_var, font=("", 11))
        statut_entry.grid(row=8, column=0, sticky="ew", pady=(0, 10))

        def submit():
            idx = contact_combo.current()
            if idx < 0:
                messagebox.showerror("Erreur", "Veuillez sélectionner un contact", parent=win)
                return
            contact_id = contact_ids[idx]
            type_inter = type_var.get().strip()
            desc = desc_var.get().strip()
            statut = statut_var.get().strip()
            if not type_inter or not desc:
                messagebox.showerror("Erreur", "Type et description obligatoires", parent=win)
                return
            self.interaction_mgr.create_interaction(contact_id, type_inter, desc, statut)
            self.load_interactions()
            win.destroy()

        btn = ttk.Button(frm, text="Créer l'interaction", command=submit, style="Accent.TButton")
        btn.grid(row=9, column=0, pady=(18, 0), sticky="ew")
    
    def load_interactions(self):
        if not self.interactions_tree:
            return
            
        for item in self.interactions_tree.get_children():
            self.interactions_tree.delete(item)

        interactions = self.interaction_mgr.get_interactions(limit=100)

        if interactions:
            for inter in interactions:
                contact_name = f"{inter['prenom']} {inter['nom']}"
                self.interactions_tree.insert("", "end", values=(
                    inter['id'],
                    contact_name,
                    inter['type_interaction'] or '',
                    inter['date_heure'],
                    inter['description']
                ))
