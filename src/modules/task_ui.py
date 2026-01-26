import tkinter as tk
from tkinter import ttk, messagebox


class TaskUI:
    
    def __init__(self, root, task_mgr, contact_mgr):
        self.root = root
        self.task_mgr = task_mgr
        self.contact_mgr = contact_mgr
        self.tasks_tree = None
    
    def create_tasks_tab(self, notebook):
        tab = ttk.Frame(notebook, padding="15")
        notebook.add(tab, text="☑ Tâches")

        ttk.Label(tab, text="Gestion des Tâches", style="Title.TLabel").pack(pady=(0, 15))

        btn_frame = ttk.Frame(tab)
        btn_frame.pack(fill=tk.X, pady=(0, 10))

        ttk.Button(btn_frame, text="➕ Nouvelle tâche", command=self.add_task).pack(side=tk.LEFT, padx=5)

        list_frame = ttk.Frame(tab)
        list_frame.pack(fill=tk.BOTH, expand=True)

        vsb = ttk.Scrollbar(list_frame, orient="vertical")
        hsb = ttk.Scrollbar(list_frame, orient="horizontal")

        self.tasks_tree = ttk.Treeview(
            list_frame,
            columns=("id", "titre", "priorite", "statut", "echeance"),
            show="headings",
            yscrollcommand=vsb.set,
            xscrollcommand=hsb.set,
            height=18
        )

        vsb.config(command=self.tasks_tree.yview)
        hsb.config(command=self.tasks_tree.xview)

        self.tasks_tree.heading("id", text="ID")
        self.tasks_tree.heading("titre", text="Titre")
        self.tasks_tree.heading("priorite", text="Priorité")
        self.tasks_tree.heading("statut", text="Statut")
        self.tasks_tree.heading("echeance", text="Échéance")

        self.tasks_tree.column("id", width=60, minwidth=40, stretch=False)
        self.tasks_tree.column("titre", width=400, minwidth=150, stretch=True)
        self.tasks_tree.column("priorite", width=120, minwidth=80, stretch=True)
        self.tasks_tree.column("statut", width=120, minwidth=80, stretch=True)
        self.tasks_tree.column("echeance", width=180, minwidth=100, stretch=True)

        self.tasks_tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")

        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(0, weight=1)

        self.load_tasks()
    
    def add_task(self):
        win = tk.Toplevel(self.root)
        win.title("Nouvelle tâche")
        win.geometry("750x700")
        win.minsize(650, 600)
        win.minsize(520, 420)
        win.transient(self.root)
        win.grab_set()

        frm = ttk.Frame(win, padding=24)
        frm.grid(row=0, column=0, sticky="nsew")

        win.grid_rowconfigure(0, weight=1)
        win.grid_columnconfigure(0, weight=1)
        for i in range(14):
            frm.grid_rowconfigure(i, weight=1)
        frm.grid_columnconfigure(0, weight=1)

        ttk.Label(frm, text="Créer une nouvelle tâche", font=("", 15, "bold")).grid(row=0, column=0, pady=(0, 18), sticky="nsew")

        titre_var = tk.StringVar()
        ttk.Label(frm, text="Titre :", font=("", 11, "bold")).grid(row=1, column=0, sticky="w", pady=(0, 2))
        titre_entry = ttk.Entry(frm, textvariable=titre_var, font=("", 11))
        titre_entry.grid(row=2, column=0, sticky="ew", pady=(0, 10))

        desc_var = tk.StringVar()
        ttk.Label(frm, text="Description :", font=("", 11, "bold")).grid(row=3, column=0, sticky="w", pady=(0, 2))
        desc_entry = ttk.Entry(frm, textvariable=desc_var, font=("", 11))
        desc_entry.grid(row=4, column=0, sticky="ew", pady=(0, 10))

        priorite_var = tk.StringVar()
        ttk.Label(frm, text="Priorité :", font=("", 11, "bold")).grid(row=5, column=0, sticky="w", pady=(0, 2))
        priorite_combo = ttk.Combobox(frm, values=["Haute", "Moyenne", "Basse"], textvariable=priorite_var, state="readonly", font=("", 11))
        priorite_combo.grid(row=6, column=0, sticky="ew", pady=(0, 10))
        priorite_combo.current(1)

        statut_var = tk.StringVar()
        ttk.Label(frm, text="Statut :", font=("", 11, "bold")).grid(row=7, column=0, sticky="w", pady=(0, 2))
        statut_combo = ttk.Combobox(frm, values=["A faire", "En cours", "Terminé"], textvariable=statut_var, state="readonly", font=("", 11))
        statut_combo.grid(row=8, column=0, sticky="ew", pady=(0, 10))
        statut_combo.current(0)

        echeance_var = tk.StringVar()
        ttk.Label(frm, text="Échéance (YYYY-MM-DD):", font=("", 11, "bold")).grid(row=9, column=0, sticky="w", pady=(0, 2))
        echeance_entry = ttk.Entry(frm, textvariable=echeance_var, font=("", 11))
        echeance_entry.grid(row=10, column=0, sticky="ew", pady=(0, 10))

        contacts = self.contact_mgr.get_all_contacts()
        contact_names = [f"{c['prenom']} {c['nom']} (id:{c['id']})" for c in contacts]
        contact_ids = [c['id'] for c in contacts]
        contacts_var = tk.Variable(value=[])
        ttk.Label(frm, text="Associer à des contacts :", font=("", 11, "bold")).grid(row=11, column=0, sticky="w", pady=(0, 2))
        contacts_listbox = tk.Listbox(frm, listvariable=contacts_var, selectmode=tk.MULTIPLE, height=4, font=("", 11))
        contacts_listbox.grid(row=12, column=0, sticky="ew", pady=(0, 10))
        for name in contact_names:
            contacts_listbox.insert(tk.END, name)

        def submit():
            titre = titre_var.get().strip()
            desc = desc_var.get().strip()
            priorite = priorite_var.get().strip()
            statut = statut_var.get().strip()
            echeance = echeance_var.get().strip()
            selected = contacts_listbox.curselection()
            if not titre or not selected:
                messagebox.showerror("Erreur", "Titre et au moins un contact sont obligatoires", parent=win)
                return
            selected_ids = [contact_ids[i] for i in selected]
            success, _ = self.task_mgr.create_task(titre, desc, selected_ids, priorite, statut, echeance)
            if success:
                self.load_tasks()
                win.destroy()
            else:
                messagebox.showerror("Erreur", "Erreur lors de la création de la tâche", parent=win)

        btn = ttk.Button(frm, text="Créer la tâche", command=submit, style="Accent.TButton")
        btn.grid(row=13, column=0, pady=(18, 0), sticky="ew")
    
    def load_tasks(self):
        if not self.tasks_tree:
            return
            
        for item in self.tasks_tree.get_children():
            self.tasks_tree.delete(item)
        
        tasks = self.task_mgr.get_tasks()
        
        if tasks:
            for task in tasks:
                self.tasks_tree.insert("", "end", values=(
                    task['id'],
                    task['titre'],
                    task['priorite'] or '',
                    task['statut'] or '',
                    task['date_echeance'] or ''
                ))
