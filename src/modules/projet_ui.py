import tkinter as tk
from tkinter import ttk, messagebox


class ProjetUI:
    
    def __init__(self, root, projet_mgr, task_mgr=None, contact_mgr=None):
        self.root = root
        self.projet_mgr = projet_mgr
        self.task_mgr = task_mgr
        self.contact_mgr = contact_mgr
        self.projets_tree = None
        self.selected_projet_id = None
    
    def create_projets_tab(self, notebook):
        tab = ttk.Frame(notebook, padding="15")
        notebook.add(tab, text="Projets")
        
        ttk.Label(tab, text="Gestion des Projets", style="Title.TLabel").pack(pady=(0, 15))
        
        btn_frame = ttk.Frame(tab)
        btn_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Button(btn_frame, text="Nouveau projet", command=self.add_projet, style="Accent.TButton").pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Voir détails", command=self.show_projet_details).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Supprimer", command=self.delete_projet, style="Danger.TButton").pack(side=tk.LEFT, padx=5)
        
        filter_frame = ttk.LabelFrame(tab, text="Filtres", padding="10")
        filter_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(filter_frame, text="Filtrer par contact :").pack(side=tk.LEFT, padx=5)
        self.contact_filter_var = tk.StringVar()
        self.contact_filter_combo = ttk.Combobox(filter_frame, textvariable=self.contact_filter_var, state="readonly", width=30)
        self.contact_filter_combo.pack(side=tk.LEFT, padx=5)
        self.contact_filter_combo.bind("<<ComboboxSelected>>", lambda e: self.load_projets())
        
        ttk.Button(filter_frame, text="Réinitialiser", command=self.reset_filters).pack(side=tk.LEFT, padx=5)
        
        list_frame = ttk.Frame(tab)
        list_frame.pack(fill=tk.BOTH, expand=True)

        vsb = ttk.Scrollbar(list_frame, orient="vertical")
        hsb = ttk.Scrollbar(list_frame, orient="horizontal")

        self.projets_tree = ttk.Treeview(
            list_frame,
            columns=("id", "nom", "objectif", "debut", "fin", "avancement", "nb_taches", "contacts"),
            show="headings",
            yscrollcommand=vsb.set,
            xscrollcommand=hsb.set,
            height=15
        )

        vsb.config(command=self.projets_tree.yview)
        hsb.config(command=self.projets_tree.xview)

        self.projets_tree.heading("id", text="ID")
        self.projets_tree.heading("nom", text="Nom du projet")
        self.projets_tree.heading("objectif", text="Objectif")
        self.projets_tree.heading("debut", text="Début")
        self.projets_tree.heading("fin", text="Fin prév.")
        self.projets_tree.heading("avancement", text="% Avanc.")
        self.projets_tree.heading("nb_taches", text="Nb Tâches")
        self.projets_tree.heading("contacts", text="Contacts")

        self.projets_tree.column("id", width=50, minwidth=40, stretch=False)
        self.projets_tree.column("nom", width=200, minwidth=150, stretch=True)
        self.projets_tree.column("objectif", width=250, minwidth=150, stretch=True)
        self.projets_tree.column("debut", width=100, minwidth=80, stretch=False)
        self.projets_tree.column("fin", width=100, minwidth=80, stretch=False)
        self.projets_tree.column("avancement", width=80, minwidth=60, stretch=False)
        self.projets_tree.column("nb_taches", width=80, minwidth=60, stretch=False)
        self.projets_tree.column("contacts", width=150, minwidth=100, stretch=True)

        self.projets_tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")

        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(0, weight=1)
        
        self.projets_tree.bind("<Double-1>", lambda e: self.show_projet_details())

        self.load_projets()
        self.load_contact_filter()
    
    def add_projet(self):
        win = tk.Toplevel(self.root)
        win.title("Nouveau projet")
        win.geometry("700x550")
        win.minsize(600, 440)
        win.minsize(480, 260)
        win.transient(self.root)
        win.lift()
        win.focus_force()

        frm = ttk.Frame(win, padding=24)
        frm.grid(row=0, column=0, sticky="nsew")

        win.grid_rowconfigure(0, weight=1)
        win.grid_columnconfigure(0, weight=1)
        for i in range(12):
            frm.grid_rowconfigure(i, weight=1)
        frm.grid_columnconfigure(0, weight=1)

        ttk.Label(frm, text="Créer un nouveau projet", font=("", 15, "bold")).grid(row=0, column=0, pady=(0, 18), sticky="nsew")

        nom_var = tk.StringVar()
        ttk.Label(frm, text="Nom du projet :", font=("", 11, "bold")).grid(row=1, column=0, sticky="w", pady=(0, 2))
        nom_entry = ttk.Entry(frm, textvariable=nom_var, font=("", 11))
        nom_entry.grid(row=2, column=0, sticky="ew", pady=(0, 10))

        desc_var = tk.StringVar()
        ttk.Label(frm, text="Description :", font=("", 11, "bold")).grid(row=3, column=0, sticky="w", pady=(0, 2))
        desc_entry = ttk.Entry(frm, textvariable=desc_var, font=("", 11))
        desc_entry.grid(row=4, column=0, sticky="ew", pady=(0, 10))

        obj_var = tk.StringVar()
        ttk.Label(frm, text="Objectif :", font=("", 11, "bold")).grid(row=5, column=0, sticky="w", pady=(0, 2))
        obj_entry = ttk.Entry(frm, textvariable=obj_var, font=("", 11))
        obj_entry.grid(row=6, column=0, sticky="ew", pady=(0, 10))

        date_debut_var = tk.StringVar()
        ttk.Label(frm, text="Date début (YYYY-MM-DD):", font=("", 11, "bold")).grid(row=7, column=0, sticky="w", pady=(0, 2))
        date_debut_entry = ttk.Entry(frm, textvariable=date_debut_var, font=("", 11))
        date_debut_entry.grid(row=8, column=0, sticky="ew", pady=(0, 10))

        date_fin_var = tk.StringVar()
        ttk.Label(frm, text="Date fin prévisionnelle (YYYY-MM-DD):", font=("", 11, "bold")).grid(row=9, column=0, sticky="w", pady=(0, 2))
        date_fin_entry = ttk.Entry(frm, textvariable=date_fin_var, font=("", 11))
        date_fin_entry.grid(row=10, column=0, sticky="ew", pady=(0, 10))

        def submit():
            nom = nom_var.get().strip()
            desc = desc_var.get().strip()
            obj = obj_var.get().strip()
            date_debut = date_debut_var.get().strip()
            date_fin = date_fin_var.get().strip()
            if not nom:
                messagebox.showerror("Erreur", "Le nom du projet est obligatoire", parent=win)
                return
            projet_id = self.projet_mgr.create_projet(nom, desc, obj, date_debut, date_fin)
            if projet_id:
                messagebox.showinfo("Succès", "Projet créé", parent=win)
                win.destroy()
                self.load_projets()
            else:
                messagebox.showerror("Erreur", "Erreur lors de la création du projet", parent=win)

        btn = ttk.Button(frm, text="Créer le projet", command=submit, style="Accent.TButton")
        btn.grid(row=11, column=0, pady=(18, 0), sticky="ew")
    
    def load_contact_filter(self):
        if not self.contact_mgr:
            return
        
        contacts = self.contact_mgr.get_all_contacts()
        contact_names = ["Tous les contacts"] + [f"{c['prenom']} {c['nom']} (id:{c['id']})" for c in contacts]
        self.contact_filter_combo['values'] = contact_names
        if contact_names:
            self.contact_filter_combo.current(0)
    
    def reset_filters(self):
        self.contact_filter_combo.current(0)
        self.load_projets()
    
    def load_projets(self):
        if not self.projets_tree:
            return
        
        for item in self.projets_tree.get_children():
            self.projets_tree.delete(item)
        
        contact_filter = None
        if self.contact_filter_var.get() and self.contact_filter_var.get() != "Tous les contacts":
            try:
                contact_id = int(self.contact_filter_var.get().split("id:")[1].rstrip(")"))
                contact_filter = contact_id
            except:
                pass
        
        projets = self.projet_mgr.get_all_projets()
        
        if projets:
            for projet in projets:
                tasks = []
                contacts_impliques = set()
                
                if self.task_mgr:
                    tasks = self.task_mgr.get_tasks_by_projet(projet['id'])
                    for task in tasks:
                        task_contacts = self.task_mgr.get_task_contacts(task['id'])
                        for tc in task_contacts:
                            contacts_impliques.add(tc['id'])
                
                if contact_filter and contact_filter not in contacts_impliques:
                    continue
                
                completed_tasks = sum(1 for t in tasks if t['statut'] == 'Terminé')
                total_tasks = len(tasks)
                avancement = int((completed_tasks / total_tasks * 100)) if total_tasks > 0 else 0
                
                contacts_str = f"{len(contacts_impliques)} contact(s)"
                
                self.projets_tree.insert("", "end", values=(
                    projet['id'],
                    projet['nom'],
                    projet['objectif'] or '',
                    projet['date_debut'] or '',
                    projet['date_fin_previsionnelle'] or '',
                    f"{avancement}%",
                    total_tasks,
                    contacts_str
                ))
    
    def delete_projet(self):
        selected = self.projets_tree.selection()
        if not selected:
            messagebox.showwarning("Attention", "Veuillez sélectionner un projet à supprimer", parent=self.root)
            return
        
        item = self.projets_tree.item(selected[0])
        projet_id = item['values'][0]
        projet_nom = item['values'][1]
        
        if messagebox.askyesno("Confirmation", f"Voulez-vous vraiment supprimer le projet '{projet_nom}' ?", parent=self.root):
            success = self.projet_mgr.delete_projet(projet_id)
            if success:
                messagebox.showinfo("Succès", "Projet supprimé")
                self.load_projets()
            else:
                messagebox.showerror("Erreur", "Erreur lors de la suppression du projet")
    
    def show_projet_details(self):
        selected = self.projets_tree.selection()
        if not selected:
            messagebox.showwarning("Attention", "Veuillez sélectionner un projet", parent=self.root)
            return
        
        item = self.projets_tree.item(selected[0])
        projet_id = item['values'][0]
        
        self.open_projet_detail_window(projet_id)
    
    def open_projet_detail_window(self, projet_id):
        projet = self.projet_mgr.get_projet_by_id(projet_id)
        if not projet:
            messagebox.showerror("Erreur", "Projet introuvable", parent=self.root)
            return
        
        win = tk.Toplevel(self.root)
        win.title(f"Projet: {projet['nom']}")
        win.geometry("1050x800")
        win.minsize(900, 700)
        win.transient(self.root)
        win.lift()
        win.focus_force()

        main_frame = ttk.Frame(win, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        header_frame = ttk.LabelFrame(main_frame, text="Informations du projet", padding=10)
        header_frame.pack(fill=tk.X, pady=(0, 10))
        
        info_grid = ttk.Frame(header_frame)
        info_grid.pack(fill=tk.X)
        
        ttk.Label(info_grid, text="Nom:", font=("", 10, "bold")).grid(row=0, column=0, sticky="w", padx=5, pady=2)
        ttk.Label(info_grid, text=projet['nom']).grid(row=0, column=1, sticky="w", padx=5, pady=2)
        
        ttk.Label(info_grid, text="Description:", font=("", 10, "bold")).grid(row=1, column=0, sticky="w", padx=5, pady=2)
        ttk.Label(info_grid, text=projet['description'] or 'N/A').grid(row=1, column=1, sticky="w", padx=5, pady=2)
        
        ttk.Label(info_grid, text="Objectif:", font=("", 10, "bold")).grid(row=2, column=0, sticky="w", padx=5, pady=2)
        ttk.Label(info_grid, text=projet['objectif'] or 'N/A').grid(row=2, column=1, sticky="w", padx=5, pady=2)
        
        ttk.Label(info_grid, text="Date début:", font=("", 10, "bold")).grid(row=0, column=2, sticky="w", padx=15, pady=2)
        ttk.Label(info_grid, text=projet['date_debut'] or 'N/A').grid(row=0, column=3, sticky="w", padx=5, pady=2)
        
        ttk.Label(info_grid, text="Date fin prévue:", font=("", 10, "bold")).grid(row=1, column=2, sticky="w", padx=15, pady=2)
        ttk.Label(info_grid, text=projet['date_fin_previsionnelle'] or 'N/A').grid(row=1, column=3, sticky="w", padx=5, pady=2)
        
        tasks = []
        if self.task_mgr:
            tasks = self.task_mgr.get_tasks_by_projet(projet_id)
        
        completed_tasks = sum(1 for t in tasks if t['statut'] == 'Terminé')
        total_tasks = len(tasks)
        avancement = int((completed_tasks / total_tasks * 100)) if total_tasks > 0 else 0
        
        contacts_impliques = set()
        if self.task_mgr:
            for task in tasks:
                task_contacts = self.task_mgr.get_task_contacts(task['id'])
                for tc in task_contacts:
                    contacts_impliques.add(tc['id'])
        
        synthese_frame = ttk.LabelFrame(main_frame, text="Vue de synthèse", padding=10)
        synthese_frame.pack(fill=tk.X, pady=(0, 10))
        
        synthese_grid = ttk.Frame(synthese_frame)
        synthese_grid.pack(fill=tk.X)
        
        ttk.Label(synthese_grid, text="Avancement:", font=("", 11, "bold")).grid(row=0, column=0, sticky="w", padx=10, pady=5)
        progress_frame = ttk.Frame(synthese_grid)
        progress_frame.grid(row=0, column=1, sticky="ew", padx=10, pady=5)
        
        progress_bar = ttk.Progressbar(progress_frame, length=200, mode='determinate', value=avancement)
        progress_bar.pack(side=tk.LEFT, padx=(0, 10))
        ttk.Label(progress_frame, text=f"{avancement}% ({completed_tasks}/{total_tasks} tâches)", font=("", 10, "bold")).pack(side=tk.LEFT)
        
        ttk.Label(synthese_grid, text="Contacts impliqués:", font=("", 11, "bold")).grid(row=1, column=0, sticky="w", padx=10, pady=5)
        ttk.Label(synthese_grid, text=f"{len(contacts_impliques)} contact(s)").grid(row=1, column=1, sticky="w", padx=10, pady=5)
        
        synthese_grid.columnconfigure(1, weight=1)
        
        tasks_frame = ttk.LabelFrame(main_frame, text=f"Tâches du projet ({len(tasks)})", padding=10)
        tasks_frame.pack(fill=tk.BOTH, expand=True)
        
        btn_tasks_frame = ttk.Frame(tasks_frame)
        btn_tasks_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Button(btn_tasks_frame, text="Ajouter tâche", command=lambda: self.add_task_to_projet(projet_id, win), style="Accent.TButton").pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_tasks_frame, text="Retirer tâche", command=lambda: self.remove_task_from_projet(projet_id, tasks_tree, win), style="Danger.TButton").pack(side=tk.LEFT, padx=5)
        
        tasks_list_frame = ttk.Frame(tasks_frame)
        tasks_list_frame.pack(fill=tk.BOTH, expand=True)
        
        vsb = ttk.Scrollbar(tasks_list_frame, orient="vertical")
        hsb = ttk.Scrollbar(tasks_list_frame, orient="horizontal")
        
        tasks_tree = ttk.Treeview(
            tasks_list_frame,
            columns=("id", "titre", "priorite", "statut", "echeance", "contacts"),
            show="headings",
            yscrollcommand=vsb.set,
            xscrollcommand=hsb.set,
            height=12
        )
        
        vsb.config(command=tasks_tree.yview)
        hsb.config(command=tasks_tree.xview)
        
        tasks_tree.heading("id", text="ID")
        tasks_tree.heading("titre", text="Titre")
        tasks_tree.heading("priorite", text="Priorité")
        tasks_tree.heading("statut", text="Statut")
        tasks_tree.heading("echeance", text="Échéance")
        tasks_tree.heading("contacts", text="Contacts")
        
        tasks_tree.column("id", width=50, minwidth=40, stretch=False)
        tasks_tree.column("titre", width=250, minwidth=150, stretch=True)
        tasks_tree.column("priorite", width=100, minwidth=80, stretch=False)
        tasks_tree.column("statut", width=100, minwidth=80, stretch=False)
        tasks_tree.column("echeance", width=120, minwidth=80, stretch=False)
        tasks_tree.column("contacts", width=150, minwidth=100, stretch=True)
        
        tasks_tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")
        
        tasks_list_frame.columnconfigure(0, weight=1)
        tasks_list_frame.rowconfigure(0, weight=1)
        
        for task in tasks:
            task_contacts = self.task_mgr.get_task_contacts(task['id']) if self.task_mgr else []
            contacts_names = ", ".join([f"{tc['prenom']} {tc['nom']}" for tc in task_contacts[:2]])
            if len(task_contacts) > 2:
                contacts_names += f" +{len(task_contacts)-2}"
            
            tasks_tree.insert("", "end", values=(
                task['id'],
                task['titre'],
                task['priorite'] or 'N/A',
                task['statut'] or 'A faire',
                task['date_echeance'] or 'N/A',
                contacts_names
            ))
        
        ttk.Button(main_frame, text="Fermer", command=win.destroy).pack(pady=(10, 0))
    
    def add_task_to_projet(self, projet_id, parent_win):
        if not self.task_mgr:
            messagebox.showwarning("Attention", "Gestionnaire de tâches non disponible", parent=self.root)
            return
        
        all_tasks = self.task_mgr.get_tasks()
        projet_tasks = self.task_mgr.get_tasks_by_projet(projet_id)
        projet_task_ids = {t['id'] for t in projet_tasks}
        
        available_tasks = [t for t in all_tasks if t['id'] not in projet_task_ids]
        
        if not available_tasks:
            messagebox.showinfo("Info", "Aucune tâche disponible à ajouter", parent=self.root)
            return
        
        win = tk.Toplevel(parent_win)
        win.title("Ajouter une tâche au projet")
        win.geometry("600x400")
        win.transient(parent_win)
        win.lift()
        win.focus_force()

        frm = ttk.Frame(win, padding=20)
        frm.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(frm, text="Sélectionnez les tâches à ajouter:", font=("", 12, "bold")).pack(pady=(0, 10))
        
        listbox_frame = ttk.Frame(frm)
        listbox_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        scrollbar = ttk.Scrollbar(listbox_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        tasks_listbox = tk.Listbox(listbox_frame, selectmode=tk.MULTIPLE, yscrollcommand=scrollbar.set, height=15)
        tasks_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=tasks_listbox.yview)
        
        for task in available_tasks:
            tasks_listbox.insert(tk.END, f"[{task['id']}] {task['titre']} - {task['statut']}")
        
        def add_selected():
            selected_indices = tasks_listbox.curselection()
            if not selected_indices:
                messagebox.showwarning("Attention", "Veuillez sélectionner au moins une tâche", parent=win)
                return
            
            for idx in selected_indices:
                task_id = available_tasks[idx]['id']
                self.task_mgr.assign_task_to_projet(task_id, projet_id)
            
            messagebox.showinfo("Succès", f"{len(selected_indices)} tâche(s) ajoutée(s) au projet", parent=win)
            win.destroy()
            parent_win.destroy()
            self.open_projet_detail_window(projet_id)
            self.load_projets()
        
        ttk.Button(frm, text="Ajouter les tâches sélectionnées", command=add_selected).pack(pady=(0, 5))
        ttk.Button(frm, text="Annuler", command=win.destroy).pack()
    
    def remove_task_from_projet(self, projet_id, tasks_tree, parent_win):
        selected = tasks_tree.selection()
        if not selected:
            messagebox.showwarning("Attention", "Veuillez sélectionner une tâche à retirer")
            return
        
        item = tasks_tree.item(selected[0])
        task_id = item['values'][0]
        task_titre = item['values'][1]
        
        if messagebox.askyesno("Confirmation", f"Voulez-vous retirer la tâche '{task_titre}' du projet ?"):
            if self.task_mgr:
                self.task_mgr.assign_task_to_projet(task_id, None)
                messagebox.showinfo("Succès", "Tâche retirée du projet")
                parent_win.destroy()
                self.open_projet_detail_window(projet_id)
                self.load_projets()
