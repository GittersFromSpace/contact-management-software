import tkinter as tk
from tkinter import ttk, messagebox
try:
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    import matplotlib
    matplotlib.use('TkAgg')
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False


class TagRelationUI:
    
    def __init__(self, root, tag_mgr, relation_mgr, contact_mgr):
        self.root = root
        self.tag_mgr = tag_mgr
        self.relation_mgr = relation_mgr
        self.contact_mgr = contact_mgr
        self.tags_tree = None
        self.relations_tree = None
        self.tag_filter_listbox = None
        self.operator_var = None
    
    def create_tags_relations_tab(self, notebook):
        tab = ttk.Frame(notebook, padding="15")
        notebook.add(tab, text="Tags & Relations")
        
        ttk.Label(tab, text="Tags et Relations", style="Title.TLabel").pack(pady=(0, 15))
        
        paned = ttk.PanedWindow(tab, orient=tk.HORIZONTAL)
        paned.pack(fill=tk.BOTH, expand=True)
        
        tags_frame = ttk.LabelFrame(paned, text="Gestion des Tags", padding="10")
        paned.add(tags_frame, weight=1)
        
        btn_tags_frame = ttk.Frame(tags_frame)
        btn_tags_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Button(btn_tags_frame, text="Nouveau tag", command=self.add_tag, style="Accent.TButton").pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_tags_frame, text="Supprimer tag", command=self.delete_tag, style="Danger.TButton").pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_tags_frame, text="Assigner à contact", command=self.assign_tag_to_contact).pack(side=tk.LEFT, padx=5)
        
        tags_list_frame = ttk.Frame(tags_frame)
        tags_list_frame.pack(fill=tk.BOTH, expand=True)
        
        vsb_tags = ttk.Scrollbar(tags_list_frame, orient="vertical")
        hsb_tags = ttk.Scrollbar(tags_list_frame, orient="horizontal")
        
        self.tags_tree = ttk.Treeview(
            tags_list_frame,
            columns=("id", "nom", "nb_contacts"),
            show="headings",
            yscrollcommand=vsb_tags.set,
            xscrollcommand=hsb_tags.set,
            height=10
        )
        
        vsb_tags.config(command=self.tags_tree.yview)
        hsb_tags.config(command=self.tags_tree.xview)
        
        self.tags_tree.heading("id", text="ID")
        self.tags_tree.heading("nom", text="Nom du tag")
        self.tags_tree.heading("nb_contacts", text="Nb Contacts")
        
        self.tags_tree.column("id", width=50, minwidth=40, stretch=False)
        self.tags_tree.column("nom", width=200, minwidth=150, stretch=True)
        self.tags_tree.column("nb_contacts", width=100, minwidth=80, stretch=False)
        
        self.tags_tree.grid(row=0, column=0, sticky="nsew")
        vsb_tags.grid(row=0, column=1, sticky="ns")
        hsb_tags.grid(row=1, column=0, sticky="ew")
        
        tags_list_frame.columnconfigure(0, weight=1)
        tags_list_frame.rowconfigure(0, weight=1)
        
        relations_frame = ttk.LabelFrame(paned, text="Gestion des Relations", padding="10")
        paned.add(relations_frame, weight=1)
        
        btn_relations_frame = ttk.Frame(relations_frame)
        btn_relations_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Button(btn_relations_frame, text="➕ Nouvelle relation", command=self.add_relation).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_relations_frame, text="🗑 Supprimer relation", command=self.delete_relation).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_relations_frame, text="🌳 Vue arbre", command=self.show_tree_view).pack(side=tk.LEFT, padx=5)
        if MATPLOTLIB_AVAILABLE:
            ttk.Button(btn_relations_frame, text="📊 Graphe réseau", command=self.show_graph_view).pack(side=tk.LEFT, padx=5)
        
        relations_list_frame = ttk.Frame(relations_frame)
        relations_list_frame.pack(fill=tk.BOTH, expand=True)
        
        vsb_rel = ttk.Scrollbar(relations_list_frame, orient="vertical")
        hsb_rel = ttk.Scrollbar(relations_list_frame, orient="horizontal")
        
        self.relations_tree = ttk.Treeview(
            relations_list_frame,
            columns=("id", "source", "type", "cible"),
            show="headings",
            yscrollcommand=vsb_rel.set,
            xscrollcommand=hsb_rel.set,
            height=10
        )
        
        vsb_rel.config(command=self.relations_tree.yview)
        hsb_rel.config(command=self.relations_tree.xview)
        
        self.relations_tree.heading("id", text="ID")
        self.relations_tree.heading("source", text="Contact Source")
        self.relations_tree.heading("type", text="Type de relation")
        self.relations_tree.heading("cible", text="Contact Cible")
        
        self.relations_tree.column("id", width=50, minwidth=40, stretch=False)
        self.relations_tree.column("source", width=200, minwidth=150, stretch=True)
        self.relations_tree.column("type", width=150, minwidth=100, stretch=True)
        self.relations_tree.column("cible", width=200, minwidth=150, stretch=True)
        
        self.relations_tree.grid(row=0, column=0, sticky="nsew")
        vsb_rel.grid(row=0, column=1, sticky="ns")
        hsb_rel.grid(row=1, column=0, sticky="ew")
        
        relations_list_frame.columnconfigure(0, weight=1)
        relations_list_frame.rowconfigure(0, weight=1)
        
        search_frame = ttk.LabelFrame(tab, text="Recherche par Tags", padding="10")
        search_frame.pack(fill=tk.X, pady=(10, 0))
        
        search_top_frame = ttk.Frame(search_frame)
        search_top_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(search_top_frame, text="Sélectionnez un ou plusieurs tags:").pack(side=tk.LEFT, padx=5)
        
        self.operator_var = tk.StringVar(value="ET")
        ttk.Radiobutton(search_top_frame, text="ET (tous les tags)", variable=self.operator_var, value="ET").pack(side=tk.LEFT, padx=10)
        ttk.Radiobutton(search_top_frame, text="OU (au moins un tag)", variable=self.operator_var, value="OU").pack(side=tk.LEFT, padx=10)
        
        ttk.Button(search_top_frame, text="Rechercher", command=self.search_by_tags, style="Accent.TButton").pack(side=tk.LEFT, padx=10)
        
        tags_select_frame = ttk.Frame(search_frame)
        tags_select_frame.pack(fill=tk.X)
        
        vsb_filter = ttk.Scrollbar(tags_select_frame, orient="vertical")
        
        self.tag_filter_listbox = tk.Listbox(tags_select_frame, selectmode=tk.MULTIPLE, yscrollcommand=vsb_filter.set, height=5)
        self.tag_filter_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        vsb_filter.config(command=self.tag_filter_listbox.yview)
        vsb_filter.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.load_tags()
        self.load_relations()
        self.load_tags_for_filter()
    
    def add_tag(self):
        win = tk.Toplevel(self.root)
        win.title("Nouveau tag")
        win.geometry("500x300")
        win.minsize(420, 260)
        win.minsize(340, 180)
        win.transient(self.root)
        win.grab_set()

        frm = ttk.Frame(win, padding=24)
        frm.grid(row=0, column=0, sticky="nsew")

        win.grid_rowconfigure(0, weight=1)
        win.grid_columnconfigure(0, weight=1)
        for i in range(4):
            frm.grid_rowconfigure(i, weight=1)
        frm.grid_columnconfigure(0, weight=1)

        ttk.Label(frm, text="Créer un nouveau tag", font=("", 15, "bold")).grid(row=0, column=0, pady=(0, 18), sticky="nsew")

        tag_var = tk.StringVar()
        ttk.Label(frm, text="Nom du tag :", font=("", 11, "bold")).grid(row=1, column=0, sticky="w", pady=(0, 2))
        tag_entry = ttk.Entry(frm, textvariable=tag_var, font=("", 11))
        tag_entry.grid(row=2, column=0, sticky="ew", pady=(0, 10))

        def submit():
            nom_tag = tag_var.get().strip()
            if not nom_tag:
                messagebox.showerror("Erreur", "Le nom du tag est obligatoire", parent=win)
                return
            tag_id = self.tag_mgr.create_tag(nom_tag)
            if tag_id:
                messagebox.showinfo("Succès", "Tag créé", parent=win)
                win.destroy()
            else:
                messagebox.showerror("Erreur", "Ce tag existe déjà", parent=win)

        btn = ttk.Button(frm, text="Créer le tag", command=submit, style="Accent.TButton")
        btn.grid(row=3, column=0, pady=(18, 0), sticky="ew")
    
    def load_tags(self):
        if not self.tags_tree:
            return
        
        for item in self.tags_tree.get_children():
            self.tags_tree.delete(item)
        
        tags = self.tag_mgr.get_all_tags()
        if tags:
            for tag in tags:
                nb_contacts = self.tag_mgr.count_contacts_by_tag(tag['id'])
                self.tags_tree.insert("", "end", values=(
                    tag['id'],
                    tag['nom_tag'],
                    nb_contacts
                ))
        
        self.load_tags_for_filter()
    
    def load_tags_for_filter(self):
        if not self.tag_filter_listbox:
            return
        
        self.tag_filter_listbox.delete(0, tk.END)
        tags = self.tag_mgr.get_all_tags()
        if tags:
            for tag in tags:
                self.tag_filter_listbox.insert(tk.END, f"{tag['nom_tag']} (id:{tag['id']})")
    
    def delete_tag(self):
        selected = self.tags_tree.selection()
        if not selected:
            messagebox.showwarning("Attention", "Veuillez sélectionner un tag à supprimer", parent=self.root)
            return
        
        item = self.tags_tree.item(selected[0])
        tag_id = item['values'][0]
        tag_nom = item['values'][1]
        
        if messagebox.askyesno("Confirmation", f"Voulez-vous vraiment supprimer le tag '{tag_nom}' ?\nIl sera retiré de tous les contacts.", parent=self.root):
            success = self.tag_mgr.delete_tag(tag_id)
            if success:
                messagebox.showinfo("Succès", "Tag supprimé")
                self.load_tags()
            else:
                messagebox.showerror("Erreur", "Erreur lors de la suppression du tag")
    
    def assign_tag_to_contact(self):
        selected = self.tags_tree.selection()
        if not selected:
            messagebox.showwarning("Attention", "Veuillez d'abord sélectionner un tag", parent=self.root)
            return
        
        item = self.tags_tree.item(selected[0])
        tag_id = item['values'][0]
        tag_nom = item['values'][1]
        
        win = tk.Toplevel(self.root)
        win.title(f"Assigner le tag '{tag_nom}' à des contacts")
        win.geometry("600x450")
        win.transient(self.root)
        win.grab_set()
        
        frm = ttk.Frame(win, padding=20)
        frm.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(frm, text=f"Sélectionnez les contacts pour le tag '{tag_nom}'", font=("", 12, "bold")).pack(pady=(0, 10))
        
        listbox_frame = ttk.Frame(frm)
        listbox_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        scrollbar = ttk.Scrollbar(listbox_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        contacts_listbox = tk.Listbox(listbox_frame, selectmode=tk.MULTIPLE, yscrollcommand=scrollbar.set, height=15)
        contacts_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=contacts_listbox.yview)
        
        contacts = self.contact_mgr.get_all_contacts()
        contact_ids = []
        already_tagged = self.tag_mgr.get_contacts_by_tag(tag_id)
        already_tagged_ids = {c['id'] for c in already_tagged}
        
        for idx, contact in enumerate(contacts):
            contact_ids.append(contact['id'])
            display_text = f"{contact['prenom']} {contact['nom']} - {contact['societe'] or 'N/A'}"
            if contact['id'] in already_tagged_ids:
                display_text += " ✓"
            contacts_listbox.insert(tk.END, display_text)
            if contact['id'] in already_tagged_ids:
                contacts_listbox.selection_set(idx)
        
        def submit():
            selected_indices = contacts_listbox.curselection()
            selected_contact_ids = {contact_ids[idx] for idx in selected_indices}
            
            to_add = selected_contact_ids - already_tagged_ids
            to_remove = already_tagged_ids - selected_contact_ids
            
            for contact_id in to_add:
                self.tag_mgr.assign_tag_to_contact(tag_id, contact_id)
            
            for contact_id in to_remove:
                self.tag_mgr.remove_tag_from_contact(tag_id, contact_id)
            
            messagebox.showinfo("Succès", f"{len(to_add)} contact(s) ajouté(s), {len(to_remove)} retiré(s)", parent=win)
            win.destroy()
            self.load_tags()
        
        ttk.Button(frm, text="Enregistrer", command=submit, style="Accent.TButton").pack(pady=(0, 5))
        ttk.Button(frm, text="Annuler", command=win.destroy).pack()
    
    def search_by_tags(self):
        selected_indices = self.tag_filter_listbox.curselection()
        if not selected_indices:
            messagebox.showwarning("Attention", "Veuillez sélectionner au moins un tag", parent=self.root)
            return
        
        tag_ids = []
        for idx in selected_indices:
            tag_text = self.tag_filter_listbox.get(idx)
            tag_id = int(tag_text.split("id:")[1].rstrip(")"))
            tag_ids.append(tag_id)
        
        operator = self.operator_var.get()
        
        if operator == "ET":
            contacts = self.tag_mgr.search_contacts_by_tags_and(tag_ids)
        else:
            contacts = self.tag_mgr.search_contacts_by_tags_or(tag_ids)
        
        win = tk.Toplevel(self.root)
        win.title(f"Résultats de recherche - {len(contacts)} contact(s)")
        win.geometry("700x500")
        win.transient(self.root)
        
        frm = ttk.Frame(win, padding=20)
        frm.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(frm, text=f"Contacts trouvés avec tags {operator}: {len(contacts)}", font=("", 12, "bold")).pack(pady=(0, 10))
        
        tree_frame = ttk.Frame(frm)
        tree_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        vsb = ttk.Scrollbar(tree_frame, orient="vertical")
        
        result_tree = ttk.Treeview(
            tree_frame,
            columns=("id", "nom", "prenom", "societe", "tags"),
            show="headings",
            yscrollcommand=vsb.set,
            height=15
        )
        
        vsb.config(command=result_tree.yview)
        
        result_tree.heading("id", text="ID")
        result_tree.heading("nom", text="Nom")
        result_tree.heading("prenom", text="Prénom")
        result_tree.heading("societe", text="Société")
        result_tree.heading("tags", text="Tags")
        
        result_tree.column("id", width=50, minwidth=40, stretch=False)
        result_tree.column("nom", width=120, minwidth=80, stretch=True)
        result_tree.column("prenom", width=120, minwidth=80, stretch=True)
        result_tree.column("societe", width=150, minwidth=100, stretch=True)
        result_tree.column("tags", width=200, minwidth=150, stretch=True)
        
        result_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        vsb.pack(side=tk.RIGHT, fill=tk.Y)
        
        for contact in contacts:
            contact_tags = self.tag_mgr.get_tags_by_contact(contact['id'])
            tags_str = ", ".join([t['nom_tag'] for t in contact_tags])
            
            result_tree.insert("", "end", values=(
                contact['id'],
                contact['nom'],
                contact['prenom'],
                contact['societe'] or 'N/A',
                tags_str
            ))
        
        ttk.Button(frm, text="Fermer", command=win.destroy).pack()
    
    def load_relations(self):
        if not self.relations_tree:
            return
        
        for item in self.relations_tree.get_children():
            self.relations_tree.delete(item)
        
        relations = self.relation_mgr.get_all_relations()
        if relations:
            for rel in relations:
                self.relations_tree.insert("", "end", values=(
                    rel['id'],
                    f"{rel['source_prenom']} {rel['source_nom']}",
                    rel['type_relation'],
                    f"{rel['cible_prenom']} {rel['cible_nom']}"
                ))
    
    def delete_relation(self):
        selected = self.relations_tree.selection()
        if not selected:
            messagebox.showwarning("Attention", "Veuillez sélectionner une relation à supprimer", parent=self.root)
            return
        
        item = self.relations_tree.item(selected[0])
        relation_id = item['values'][0]
        
        if messagebox.askyesno("Confirmation", "Voulez-vous vraiment supprimer cette relation ?", parent=self.root):
            success = self.relation_mgr.delete_relation(relation_id)
            if success:
                messagebox.showinfo("Succès", "Relation supprimée")
                self.load_relations()
            else:
                messagebox.showerror("Erreur", "Erreur lors de la suppression de la relation")
    
    def show_tree_view(self):
        relations = self.relation_mgr.get_all_relations()
        if not relations:
            messagebox.showinfo("Info", "Aucune relation à afficher")
            return
        
        win = tk.Toplevel(self.root)
        win.title("Vue en arbre hiérarchique des relations")
        win.geometry("800x600")
        win.transient(self.root)
        
        frm = ttk.Frame(win, padding=20)
        frm.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(frm, text="Relations - Vue hiérarchique", font=("", 14, "bold")).pack(pady=(0, 10))
        
        tree_frame = ttk.Frame(frm)
        tree_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        vsb = ttk.Scrollbar(tree_frame, orient="vertical")
        hsb = ttk.Scrollbar(tree_frame, orient="horizontal")
        
        hierarchy_tree = ttk.Treeview(
            tree_frame,
            yscrollcommand=vsb.set,
            xscrollcommand=hsb.set,
            height=20
        )
        
        vsb.config(command=hierarchy_tree.yview)
        hsb.config(command=hierarchy_tree.xview)
        
        hierarchy_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        vsb.pack(side=tk.RIGHT, fill=tk.Y)
        hsb.pack(side=tk.BOTTOM, fill=tk.X)
        
        contact_nodes = {}
        
        for rel in relations:
            source_id = rel['contact_source_id']
            cible_id = rel['contact_cible_id']
            source_name = f"{rel['source_prenom']} {rel['source_nom']}"
            cible_name = f"{rel['cible_prenom']} {rel['cible_nom']}"
            type_rel = rel['type_relation']
            
            if source_id not in contact_nodes:
                contact_nodes[source_id] = hierarchy_tree.insert("", "end", text=source_name, open=True)
            
            hierarchy_tree.insert(contact_nodes[source_id], "end", text=f"[{type_rel}] → {cible_name}")
        
        ttk.Button(frm, text="Fermer", command=win.destroy).pack()
    
    def show_graph_view(self):
        if not MATPLOTLIB_AVAILABLE:
            messagebox.showerror("Erreur", "Matplotlib n'est pas installé", parent=self.root)
            return
        
        relations = self.relation_mgr.get_all_relations()
        if not relations:
            messagebox.showinfo("Info", "Aucune relation à afficher")
            return
        
        win = tk.Toplevel(self.root)
        win.title("Graphe réseau des relations")
        win.geometry("900x700")
        win.transient(self.root)
        
        frm = ttk.Frame(win, padding=10)
        frm.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(frm, text="Relations - Graphe de réseau", font=("", 14, "bold")).pack(pady=(0, 10))
        
        fig, ax = plt.subplots(figsize=(10, 8))
        
        nodes = {}
        edges = []
        
        for rel in relations:
            source_id = rel['contact_source_id']
            cible_id = rel['contact_cible_id']
            source_name = f"{rel['source_prenom']} {rel['source_nom']}"
            cible_name = f"{rel['cible_prenom']} {rel['cible_nom']}"
            
            if source_id not in nodes:
                nodes[source_id] = source_name
            if cible_id not in nodes:
                nodes[cible_id] = cible_name
            
            edges.append((source_id, cible_id, rel['type_relation']))
        
        node_list = list(nodes.keys())
        positions = {}
        
        import math
        n = len(node_list)
        radius = 3
        for i, node_id in enumerate(node_list):
            angle = 2 * math.pi * i / n
            positions[node_id] = (radius * math.cos(angle), radius * math.sin(angle))
        
        for node_id, (x, y) in positions.items():
            ax.plot(x, y, 'o', markersize=20, color='skyblue', zorder=3)
            ax.text(x, y + 0.3, nodes[node_id], ha='center', va='bottom', fontsize=9, weight='bold')
        
        for source_id, cible_id, type_rel in edges:
            x1, y1 = positions[source_id]
            x2, y2 = positions[cible_id]
            ax.plot([x1, x2], [y1, y2], 'gray', linewidth=1, zorder=1)
            
            mid_x, mid_y = (x1 + x2) / 2, (y1 + y2) / 2
            ax.text(mid_x, mid_y, type_rel, fontsize=8, color='red', ha='center', bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.7))
        
        ax.set_xlim(-radius - 1, radius + 1)
        ax.set_ylim(-radius - 1, radius + 1)
        ax.set_aspect('equal')
        ax.axis('off')
        ax.set_title('Réseau de relations entre contacts', fontsize=14, weight='bold')
        
        canvas = FigureCanvasTkAgg(fig, master=frm)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        ttk.Button(frm, text="Fermer", command=win.destroy).pack(pady=(10, 0))
    
    def add_relation(self):
        win = tk.Toplevel(self.root)
        win.title("Nouvelle relation")
        win.geometry("700x500")
        win.minsize(600, 400)
        win.minsize(480, 260)
        win.transient(self.root)
        win.grab_set()

        frm = ttk.Frame(win, padding=24)
        frm.grid(row=0, column=0, sticky="nsew")

        win.grid_rowconfigure(0, weight=1)
        win.grid_columnconfigure(0, weight=1)
        for i in range(8):
            frm.grid_rowconfigure(i, weight=1)
        frm.grid_columnconfigure(0, weight=1)

        ttk.Label(frm, text="Créer une nouvelle relation", font=("", 15, "bold")).grid(row=0, column=0, pady=(0, 18), sticky="nsew")

        contacts = self.contact_mgr.get_all_contacts()
        contact_names = [f"{c['prenom']} {c['nom']} (id:{c['id']})" for c in contacts]
        contact_ids = [c['id'] for c in contacts]
        ttk.Label(frm, text="Contact source :", font=("", 11, "bold")).grid(row=1, column=0, sticky="w", pady=(0, 2))
        source_var = tk.StringVar()
        source_combo = ttk.Combobox(frm, values=contact_names, textvariable=source_var, state="readonly", font=("", 11))
        source_combo.grid(row=2, column=0, sticky="ew", pady=(0, 10))
        if contact_names:
            source_combo.current(0)

        ttk.Label(frm, text="Contact cible :", font=("", 11, "bold")).grid(row=3, column=0, sticky="w", pady=(0, 2))
        cible_var = tk.StringVar()
        cible_combo = ttk.Combobox(frm, values=contact_names, textvariable=cible_var, state="readonly", font=("", 11))
        cible_combo.grid(row=4, column=0, sticky="ew", pady=(0, 10))
        if contact_names:
            cible_combo.current(0)

        type_var = tk.StringVar()
        ttk.Label(frm, text="Type de relation :", font=("", 11, "bold")).grid(row=5, column=0, sticky="w", pady=(0, 2))
        type_entry = ttk.Entry(frm, textvariable=type_var, font=("", 11))
        type_entry.grid(row=6, column=0, sticky="ew", pady=(0, 10))

        def submit():
            idx_source = source_combo.current()
            idx_cible = cible_combo.current()
            if idx_source < 0 or idx_cible < 0:
                messagebox.showerror("Erreur", "Sélectionnez les deux contacts", parent=win)
                return
            if idx_source == idx_cible:
                messagebox.showerror("Erreur", "Source et cible doivent être différents", parent=win)
                return
            contact_source_id = contact_ids[idx_source]
            contact_cible_id = contact_ids[idx_cible]
            type_relation = type_var.get().strip()
            if not type_relation:
                messagebox.showerror("Erreur", "Type de relation obligatoire", parent=win)
                return
            rel_id = self.relation_mgr.create_relation(contact_source_id, contact_cible_id, type_relation)
            if rel_id:
                messagebox.showinfo("Succès", "Relation créée", parent=win)
                win.destroy()
            else:
                messagebox.showerror("Erreur", "Erreur lors de la création de la relation", parent=win)

        btn = ttk.Button(frm, text="Créer la relation", command=submit, style="Accent.TButton")
        btn.grid(row=7, column=0, pady=(18, 0), sticky="ew")
