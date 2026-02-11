"""Interface graphique pour la gestion des contacts"""
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime
import webbrowser



class ContactUI:
    
    
    def __init__(self, parent, contact_manager, auth_manager, notebook=None):
        self.parent = parent
        self.contact_mgr = contact_manager
        self.auth = auth_manager
        self.notebook = notebook
        self.current_contact_id = None
        
    def create_main_interface(self, container):
        
        
        main_frame = ttk.Frame(container, padding="15")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        
        search_frame = ttk.LabelFrame(main_frame, text="Recherche", padding="10")
        search_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Label(search_frame, text="Rechercher:").grid(row=0, column=0, sticky=tk.W)
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var, width=40)
        search_entry.grid(row=0, column=1, padx=5, sticky=(tk.W, tk.E))
        
        ttk.Button(search_frame, text="Rechercher", command=self.search_contacts, style="Accent.TButton").grid(row=0, column=2, padx=5)
        ttk.Button(search_frame, text="Réinitialiser", command=self.reset_search).grid(row=0, column=3, padx=5)
        
        
        ttk.Label(search_frame, text="Catégorie:").grid(row=1, column=0, sticky=tk.W, pady=(5, 0))
        self.categorie_var = tk.StringVar()
        self.categorie_combo = ttk.Combobox(search_frame, textvariable=self.categorie_var, width=20, state="readonly")
        self.categorie_combo.grid(row=1, column=1, padx=5, pady=(5, 0), sticky=tk.W)
        self.categorie_combo.bind("<<ComboboxSelected>>", lambda e: self.search_contacts())

        ttk.Label(search_frame, text="Ville:").grid(row=1, column=2, sticky=tk.W, pady=(5, 0))
        self.ville_var = tk.StringVar()
        self.ville_combo = ttk.Combobox(search_frame, textvariable=self.ville_var, width=20, state="readonly")
        self.ville_combo.grid(row=1, column=3, padx=5, pady=(5, 0), sticky=tk.W)
        self.ville_combo.bind("<<ComboboxSelected>>", lambda e: self.search_contacts())
        
        
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Button(button_frame, text="Nouveau contact", command=self.open_add_contact_window, style="Accent.TButton").pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Voir détails", command=self.view_contact_details).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Modifier", command=self.edit_contact).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Supprimer", command=self.delete_contact, style="Danger.TButton").pack(side=tk.LEFT, padx=5)
        
        
        list_frame = ttk.Frame(main_frame)
        list_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        
        vsb = ttk.Scrollbar(list_frame, orient="vertical")
        hsb = ttk.Scrollbar(list_frame, orient="horizontal")
        
        
        self.contacts_tree = ttk.Treeview(
            list_frame,
            columns=("id", "nom", "prenom", "societe", "poste", "ville", "categorie"),
            show="headings",
            yscrollcommand=vsb.set,
            xscrollcommand=hsb.set
        )
        
        vsb.config(command=self.contacts_tree.yview)
        hsb.config(command=self.contacts_tree.xview)
        
        
        self.contacts_tree.heading("id", text="ID")
        self.contacts_tree.heading("nom", text="Nom")
        self.contacts_tree.heading("prenom", text="Prénom")
        self.contacts_tree.heading("societe", text="Société")
        self.contacts_tree.heading("poste", text="Poste")
        self.contacts_tree.heading("ville", text="Ville")
        self.contacts_tree.heading("categorie", text="Catégorie")
        
        self.contacts_tree.column("id", width=50)
        self.contacts_tree.column("nom", width=120)
        self.contacts_tree.column("prenom", width=120)
        self.contacts_tree.column("societe", width=150)
        self.contacts_tree.column("poste", width=120)
        self.contacts_tree.column("ville", width=100)
        self.contacts_tree.column("categorie", width=100)
        
        
        self.contacts_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        vsb.grid(row=0, column=1, sticky=(tk.N, tk.S))
        hsb.grid(row=1, column=0, sticky=(tk.W, tk.E))
        
        self.contacts_tree.bind("<Double-1>", lambda e: self.view_contact_details())
        
        
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(2, weight=1)
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(0, weight=1)
        
        
        self.load_contacts()
        self.load_filter_options()
        
        return main_frame
    
    def load_contacts(self, filters=None):
        for item in self.contacts_tree.get_children():
            self.contacts_tree.delete(item)
        
        if filters:
            contacts = self.contact_mgr.search_contacts(filters)
        else:
            contacts = self.contact_mgr.get_all_contacts()
        
        if contacts:
            for contact in contacts:
                self.contacts_tree.insert("", "end", values=(
                    contact['id'],
                    contact['nom'] or '',
                    contact['prenom'] or '',
                    contact['societe'] or '',
                    contact['poste'] or '',
                    contact['adresse_ville'] or '',
                    contact['categorie'] or ''
                ))
    
    def load_filter_options(self):
        
        categories = [''] + self.contact_mgr.get_categories()
        self.categorie_combo['values'] = categories
        
        villes = [''] + self.contact_mgr.get_villes()
        self.ville_combo['values'] = villes
    
    def search_contacts(self):
        
        filters = {}
        
        if self.search_var.get():
            filters['search_text'] = self.search_var.get()
        
        if self.categorie_var.get():
            filters['categorie'] = self.categorie_var.get()
        
        if self.ville_var.get():
            filters['ville'] = self.ville_var.get()
        
        self.load_contacts(filters if filters else None)
    
    def reset_search(self):
        
        self.search_var.set('')
        self.categorie_var.set('')
        self.ville_var.set('')
        self.load_contacts()
    
    def get_selected_contact_id(self):
        
        selection = self.contacts_tree.selection()
        if not selection:
            return None
        
        item = self.contacts_tree.item(selection[0])
        return item['values'][0]
    
    def open_add_contact_window(self):
        
        self.open_contact_form_window()
    
    def edit_contact(self):
        
        contact_id = self.get_selected_contact_id()
        if not contact_id:
            messagebox.showwarning("Sélection requise", "Veuillez sélectionner un contact à modifier", parent=self.parent)
            return
        
        self.open_contact_form_window(contact_id)
    
    def delete_contact(self):
        
        contact_id = self.get_selected_contact_id()
        if not contact_id:
            messagebox.showwarning("Sélection requise", "Veuillez sélectionner un contact à supprimer", parent=self.parent)
            return
        
        if messagebox.askyesno("Confirmation", "Êtes-vous sûr de vouloir supprimer ce contact ?", parent=self.parent):
            if self.contact_mgr.delete_contact(contact_id):
                messagebox.showinfo("Succès", "Contact supprimé avec succès", parent=self.parent)
                self.load_contacts()
            else:
                messagebox.showerror("Erreur", "Erreur lors de la suppression du contact", parent=self.parent)
    
    def view_contact_details(self):

        contact_id = self.get_selected_contact_id()
        if not contact_id:
            messagebox.showwarning("Sélection requise", "Veuillez sélectionner un contact", parent=self.parent)
            return

        self.open_contact_details_window(contact_id)
    
    def open_contact_form_window(self, contact_id=None):
        
        window = tk.Toplevel(self.parent)
        window.title("Nouveau contact" if not contact_id else "Modifier le contact")
        window.geometry("1100x900")
        window.minsize(1000, 800)
        window.transient(self.parent)
        window.lift()
        window.focus_force()
        
        
        contact_data = self.contact_mgr.get_contact(contact_id) if contact_id else {}
        
        
        canvas = tk.Canvas(window)
        scrollbar = ttk.Scrollbar(window, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        
        notebook = ttk.Notebook(scrollable_frame)
        notebook.pack(fill="both", expand=True, padx=10, pady=10)
        
        
        tab1 = ttk.Frame(notebook, padding="10")
        notebook.add(tab1, text="Informations")
        
        
        form_vars = {}
        
        row = 0
        
        
        ttk.Label(tab1, text="Civilité:").grid(row=row, column=0, sticky=tk.W, pady=5)
        form_vars['civilite'] = tk.StringVar(value=contact_data.get('civilite', ''))
        civilite_combo = ttk.Combobox(tab1, textvariable=form_vars['civilite'], values=['M.', 'Mme', 'Mlle'], width=30)
        civilite_combo.grid(row=row, column=1, sticky=(tk.W, tk.E), pady=5)
        row += 1
        
        
        ttk.Label(tab1, text="Nom *:").grid(row=row, column=0, sticky=tk.W, pady=5)
        form_vars['nom'] = tk.StringVar(value=contact_data.get('nom', ''))
        ttk.Entry(tab1, textvariable=form_vars['nom'], width=32).grid(row=row, column=1, sticky=(tk.W, tk.E), pady=5)
        row += 1
        
        
        ttk.Label(tab1, text="Prénom:").grid(row=row, column=0, sticky=tk.W, pady=5)
        form_vars['prenom'] = tk.StringVar(value=contact_data.get('prenom', ''))
        ttk.Entry(tab1, textvariable=form_vars['prenom'], width=32).grid(row=row, column=1, sticky=(tk.W, tk.E), pady=5)
        row += 1
        
        
        ttk.Label(tab1, text="Société:").grid(row=row, column=0, sticky=tk.W, pady=5)
        form_vars['societe'] = tk.StringVar(value=contact_data.get('societe', ''))
        ttk.Entry(tab1, textvariable=form_vars['societe'], width=32).grid(row=row, column=1, sticky=(tk.W, tk.E), pady=5)
        row += 1
        
        
        ttk.Label(tab1, text="Poste/Fonction:").grid(row=row, column=0, sticky=tk.W, pady=5)
        form_vars['poste'] = tk.StringVar(value=contact_data.get('poste', ''))
        ttk.Entry(tab1, textvariable=form_vars['poste'], width=32).grid(row=row, column=1, sticky=(tk.W, tk.E), pady=5)
        row += 1
        
        
        ttk.Label(tab1, text="Catégorie:").grid(row=row, column=0, sticky=tk.W, pady=5)
        form_vars['categorie'] = tk.StringVar(value=contact_data.get('categorie', ''))
        categories = ['Client', 'Fournisseur', 'Partenaire', 'Collègue', 'Ami', 'Famille', 'Autre']
        ttk.Combobox(tab1, textvariable=form_vars['categorie'], values=categories, width=30).grid(row=row, column=1, sticky=(tk.W, tk.E), pady=5)
        row += 1
        
        
        ttk.Label(tab1, text="Date de naissance:").grid(row=row, column=0, sticky=tk.W, pady=5)
        form_vars['date_naissance'] = tk.StringVar(value=contact_data.get('date_naissance', ''))
        ttk.Entry(tab1, textvariable=form_vars['date_naissance'], width=32).grid(row=row, column=1, sticky=(tk.W, tk.E), pady=5)
        ttk.Label(tab1, text="(YYYY-MM-DD)", font=("", 8, "italic")).grid(row=row, column=2, sticky=tk.W, padx=5)
        row += 1
        
        
        ttk.Label(tab1, text="Site web:").grid(row=row, column=0, sticky=tk.W, pady=5)
        form_vars['site_web'] = tk.StringVar(value=contact_data.get('site_web', ''))
        ttk.Entry(tab1, textvariable=form_vars['site_web'], width=32).grid(row=row, column=1, sticky=(tk.W, tk.E), pady=5)
        row += 1
        
        
        tab2 = ttk.Frame(notebook, padding="10")
        notebook.add(tab2, text="Coordonnées")
        
        row = 0
        
        
        ttk.Label(tab2, text="Téléphones:", font=("", 10, "bold")).grid(row=row, column=0, columnspan=3, sticky=tk.W, pady=(5, 10))
        row += 1
        
        ttk.Label(tab2, text="Mobile:").grid(row=row, column=0, sticky=tk.W, pady=5)
        form_vars['tel_mobile'] = tk.StringVar(value='')
        ttk.Entry(tab2, textvariable=form_vars['tel_mobile'], width=32).grid(row=row, column=1, sticky=(tk.W, tk.E), pady=5)
        row += 1
        
        ttk.Label(tab2, text="Fixe:").grid(row=row, column=0, sticky=tk.W, pady=5)
        form_vars['tel_fixe'] = tk.StringVar(value='')
        ttk.Entry(tab2, textvariable=form_vars['tel_fixe'], width=32).grid(row=row, column=1, sticky=(tk.W, tk.E), pady=5)
        row += 1
        
        ttk.Label(tab2, text="Pro:").grid(row=row, column=0, sticky=tk.W, pady=5)
        form_vars['tel_pro'] = tk.StringVar(value='')
        ttk.Entry(tab2, textvariable=form_vars['tel_pro'], width=32).grid(row=row, column=1, sticky=(tk.W, tk.E), pady=5)
        row += 1
        
        
        ttk.Label(tab2, text="Emails:", font=("", 10, "bold")).grid(row=row, column=0, columnspan=3, sticky=tk.W, pady=(15, 10))
        row += 1
        
        ttk.Label(tab2, text="Email professionnel:").grid(row=row, column=0, sticky=tk.W, pady=5)
        form_vars['email_pro'] = tk.StringVar(value='')
        ttk.Entry(tab2, textvariable=form_vars['email_pro'], width=32).grid(row=row, column=1, sticky=(tk.W, tk.E), pady=5)
        row += 1
        
        ttk.Label(tab2, text="Email personnel:").grid(row=row, column=0, sticky=tk.W, pady=5)
        form_vars['email_perso'] = tk.StringVar(value='')
        ttk.Entry(tab2, textvariable=form_vars['email_perso'], width=32).grid(row=row, column=1, sticky=(tk.W, tk.E), pady=5)
        row += 1
        
        
        if contact_id:
            coordonnees = self.contact_mgr.get_coordonnees(contact_id)
            if coordonnees:
                for coord in coordonnees:
                    type_coord = coord['type_coord']
                    valeur = coord['valeur']
                    if type_coord == 'tel_mobile':
                        form_vars['tel_mobile'].set(valeur)
                    elif type_coord == 'tel_fixe':
                        form_vars['tel_fixe'].set(valeur)
                    elif type_coord == 'tel_pro':
                        form_vars['tel_pro'].set(valeur)
                    elif type_coord == 'email_pro':
                        form_vars['email_pro'].set(valeur)
                    elif type_coord == 'email_perso':
                        form_vars['email_perso'].set(valeur)
        
        
        tab3 = ttk.Frame(notebook, padding="10")
        notebook.add(tab3, text="Adresse")
        
        row = 0
        
        ttk.Label(tab3, text="Rue:").grid(row=row, column=0, sticky=tk.W, pady=5)
        form_vars['adresse_rue'] = tk.StringVar(value=contact_data.get('adresse_rue', ''))
        ttk.Entry(tab3, textvariable=form_vars['adresse_rue'], width=32).grid(row=row, column=1, sticky=(tk.W, tk.E), pady=5)
        row += 1
        
        ttk.Label(tab3, text="Code postal:").grid(row=row, column=0, sticky=tk.W, pady=5)
        form_vars['adresse_code_postal'] = tk.StringVar(value=contact_data.get('adresse_code_postal', ''))
        ttk.Entry(tab3, textvariable=form_vars['adresse_code_postal'], width=32).grid(row=row, column=1, sticky=(tk.W, tk.E), pady=5)
        row += 1
        
        ttk.Label(tab3, text="Ville:").grid(row=row, column=0, sticky=tk.W, pady=5)
        form_vars['adresse_ville'] = tk.StringVar(value=contact_data.get('adresse_ville', ''))
        ttk.Entry(tab3, textvariable=form_vars['adresse_ville'], width=32).grid(row=row, column=1, sticky=(tk.W, tk.E), pady=5)
        row += 1
        
        ttk.Label(tab3, text="Pays:").grid(row=row, column=0, sticky=tk.W, pady=5)
        form_vars['adresse_pays'] = tk.StringVar(value=contact_data.get('adresse_pays', ''))
        ttk.Entry(tab3, textvariable=form_vars['adresse_pays'], width=32).grid(row=row, column=1, sticky=(tk.W, tk.E), pady=5)
        
        
        tab4 = ttk.Frame(notebook, padding="10")
        notebook.add(tab4, text="Réseaux & Infos")
        
        row = 0
        
        ttk.Label(tab4, text="Réseaux sociaux:", font=("", 10, "bold")).grid(row=row, column=0, columnspan=3, sticky=tk.W, pady=(5, 10))
        row += 1
        
        ttk.Label(tab4, text="LinkedIn:").grid(row=row, column=0, sticky=tk.W, pady=5)
        form_vars['linkedin'] = tk.StringVar(value='')
        ttk.Entry(tab4, textvariable=form_vars['linkedin'], width=32).grid(row=row, column=1, sticky=(tk.W, tk.E), pady=5)
        row += 1
        
        ttk.Label(tab4, text="Twitter/X:").grid(row=row, column=0, sticky=tk.W, pady=5)
        form_vars['twitter'] = tk.StringVar(value='')
        ttk.Entry(tab4, textvariable=form_vars['twitter'], width=32).grid(row=row, column=1, sticky=(tk.W, tk.E), pady=5)
        row += 1
        
        ttk.Label(tab4, text="Facebook:").grid(row=row, column=0, sticky=tk.W, pady=5)
        form_vars['facebook'] = tk.StringVar(value='')
        ttk.Entry(tab4, textvariable=form_vars['facebook'], width=32).grid(row=row, column=1, sticky=(tk.W, tk.E), pady=5)
        row += 1
        
        ttk.Label(tab4, text="Instagram:").grid(row=row, column=0, sticky=tk.W, pady=5)
        form_vars['instagram'] = tk.StringVar(value='')
        ttk.Entry(tab4, textvariable=form_vars['instagram'], width=32).grid(row=row, column=1, sticky=(tk.W, tk.E), pady=5)
        row += 1
        
        
        if contact_id:
            reseaux = self.contact_mgr.get_reseaux_sociaux(contact_id)
            if reseaux:
                for reseau in reseaux:
                    plateforme = reseau['plateforme']
                    if plateforme in form_vars:
                        form_vars[plateforme].set(reseau['url'])
        
        ttk.Label(tab4, text="Autres informations:", font=("", 10, "bold")).grid(row=row, column=0, columnspan=3, sticky=tk.W, pady=(15, 10))
        row += 1
        
        ttk.Label(tab4, text="Anniversaire professionnel:").grid(row=row, column=0, sticky=tk.W, pady=5)
        form_vars['anniversaire_pro'] = tk.StringVar(value=contact_data.get('anniversaire_professionnel', ''))
        ttk.Entry(tab4, textvariable=form_vars['anniversaire_pro'], width=32).grid(row=row, column=1, sticky=(tk.W, tk.E), pady=5)
        ttk.Label(tab4, text="(YYYY-MM-DD)", font=("", 8, "italic")).grid(row=row, column=2, sticky=tk.W, padx=5)
        row += 1
        
        ttk.Label(tab4, text="Chemin photo:").grid(row=row, column=0, sticky=tk.W, pady=5)
        form_vars['photo_path'] = tk.StringVar(value=contact_data.get('photo_path', ''))
        photo_entry = ttk.Entry(tab4, textvariable=form_vars['photo_path'], width=32)
        photo_entry.grid(row=row, column=1, sticky=(tk.W, tk.E), pady=5)
        ttk.Button(tab4, text="📁", width=3, command=lambda: self.browse_photo(form_vars['photo_path'])).grid(row=row, column=2, padx=5)
        row += 1
        
        
        tab5 = ttk.Frame(notebook, padding="10")
        notebook.add(tab5, text="Notes")
        
        ttk.Label(tab5, text="Notes libres (texte multiligne):", font=("", 10, "bold")).pack(anchor=tk.W, pady=(0, 10))
        
        form_vars['notes_text'] = tk.Text(tab5, wrap=tk.WORD, width=60, height=20)
        form_vars['notes_text'].pack(fill="both", expand=True)
        
        
        if contact_id and 'notes' in contact_data and contact_data['notes']:
            form_vars['notes_text'].insert(1.0, contact_data['notes'])
        
        
        button_frame = ttk.Frame(scrollable_frame)
        button_frame.pack(fill="x", padx=10, pady=10)
        
        ttk.Button(
            button_frame,
            text="Enregistrer",
            command=lambda: self.save_contact(contact_id, form_vars, window)
        ).pack(side=tk.RIGHT, padx=5)
        
        ttk.Button(button_frame, text="Annuler", command=window.destroy).pack(side=tk.RIGHT, padx=5)
        
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        tab1.columnconfigure(1, weight=1)
        tab2.columnconfigure(1, weight=1)
        tab3.columnconfigure(1, weight=1)
        tab4.columnconfigure(1, weight=1)
    
    def browse_photo(self, photo_var):
        
        filename = filedialog.askopenfilename(
            title="Sélectionner une photo",
            filetypes=[("Images", "*.png *.jpg *.jpeg *.gif *.bmp"), ("Tous les fichiers", "*.*")]
        )
        if filename:
            photo_var.set(filename)
    
    def save_contact(self, contact_id, form_vars, window):
        
        
        if not form_vars['nom'].get():
            messagebox.showerror("Erreur", "Le nom est obligatoire", parent=window)
            return
        
        
        contact_data = {
            'civilite': form_vars['civilite'].get(),
            'nom': form_vars['nom'].get(),
            'prenom': form_vars['prenom'].get(),
            'societe': form_vars['societe'].get(),
            'poste': form_vars['poste'].get(),
            'categorie': form_vars['categorie'].get(),
            'date_naissance': form_vars['date_naissance'].get() or None,
            'anniversaire_professionnel': form_vars['anniversaire_pro'].get() or None,
            'site_web': form_vars['site_web'].get(),
            'photo_path': form_vars['photo_path'].get(),
            'adresse_rue': form_vars['adresse_rue'].get(),
            'adresse_code_postal': form_vars['adresse_code_postal'].get(),
            'adresse_ville': form_vars['adresse_ville'].get(),
            'adresse_pays': form_vars['adresse_pays'].get(),
        }
        
        
        emails = [form_vars['email_pro'].get(), form_vars['email_perso'].get()]
        for email in emails:
            if email and '@' not in email:
                messagebox.showerror("Erreur", f"Format email invalide: {email}", parent=window)
                return
        
        if contact_id:
            
            if self.contact_mgr.update_contact(contact_id, contact_data):
                
                self.save_coordonnees(contact_id, form_vars)
                
                self.save_reseaux_sociaux(contact_id, form_vars)
                
                notes_content = form_vars['notes_text'].get("1.0", tk.END).strip()
                if notes_content:
                    self.contact_mgr.add_note(contact_id, notes_content)
                
                messagebox.showinfo("Succès", "Contact modifié avec succès", parent=window)
                window.destroy()
                self.load_contacts()
                self.load_filter_options()
            else:
                messagebox.showerror("Erreur", "Erreur lors de la modification", parent=window)
        else:
            
            success, new_id = self.contact_mgr.create_contact(contact_data)
            if success:
                
                self.save_coordonnees(new_id, form_vars)
                
                self.save_reseaux_sociaux(new_id, form_vars)
                
                notes_content = form_vars['notes_text'].get("1.0", tk.END).strip()
                if notes_content:
                    self.contact_mgr.add_note(new_id, notes_content)
                
                messagebox.showinfo("Succès", f"Contact créé avec succès (ID: {new_id})", parent=window)
                window.destroy()
                self.load_contacts()
                self.load_filter_options()
            else:
                messagebox.showerror("Erreur", "Erreur lors de la création", parent=window)
    
    def save_coordonnees(self, contact_id, form_vars):
        
        
        self.contact_mgr.delete_coordonnees(contact_id)
        
        
        coordonnees = [
            ('tel_mobile', form_vars['tel_mobile'].get()),
            ('tel_fixe', form_vars['tel_fixe'].get()),
            ('tel_pro', form_vars['tel_pro'].get()),
            ('email_pro', form_vars['email_pro'].get()),
            ('email_perso', form_vars['email_perso'].get()),
        ]
        
        for type_coord, valeur in coordonnees:
            if valeur:
                self.contact_mgr.add_coordonnee(contact_id, type_coord, valeur)
    
    def save_reseaux_sociaux(self, contact_id, form_vars):
        
        
        self.contact_mgr.delete_reseaux_sociaux(contact_id)
        
        
        reseaux = [
            ('linkedin', form_vars['linkedin'].get()),
            ('twitter', form_vars['twitter'].get()),
            ('facebook', form_vars['facebook'].get()),
            ('instagram', form_vars['instagram'].get()),
        ]
        
        for plateforme, url in reseaux:
            if url:
                self.contact_mgr.add_reseau_social(contact_id, plateforme, url)
    
    def open_contact_details_window(self, contact_id):
        
        contact = self.contact_mgr.get_contact(contact_id)
        if not contact:
            messagebox.showerror("Erreur", "Contact introuvable", parent=self.parent)
            return
        
        window = tk.Toplevel(self.parent)
        window.title(f"Fiche contact - {contact.get('prenom', '')} {contact.get('nom', '')}")
        window.geometry("1000x800")
        window.minsize(900, 700)
        window.transient(self.parent)
        window.lift()
        window.focus_force()
        
        
        main_frame = ttk.Frame(window, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        
        top_buttons = ttk.Frame(main_frame)
        top_buttons.pack(fill=tk.X, pady=(0, 10))
        
        if self.auth.has_permission('update'):
            ttk.Button(top_buttons, text="✏ Modifier", command=lambda: [window.destroy(), self.edit_contact()]).pack(side=tk.LEFT, padx=5)
        
        if self.auth.has_permission('delete'):
            ttk.Button(top_buttons, text="🗑 Supprimer", command=lambda: [window.destroy(), self.delete_contact()]).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(top_buttons, text="📋 Exporter fiche", command=lambda: self.export_contact(contact_id)).pack(side=tk.LEFT, padx=5)
        ttk.Button(top_buttons, text="✉ Ajouter interaction", command=lambda: self.quick_add_interaction(contact_id)).pack(side=tk.LEFT, padx=5)
        ttk.Button(top_buttons, text="⏰ Ajouter rappel", command=lambda: self.quick_add_rappel(contact_id)).pack(side=tk.LEFT, padx=5)
        
        
        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill=tk.BOTH, expand=True)
        
        
        tab_identite = ttk.Frame(notebook, padding="15")
        notebook.add(tab_identite, text="👤 Identité")
        
        
        identity_frame = ttk.Frame(tab_identite)
        identity_frame.pack(fill=tk.BOTH, expand=True)
        
        
        photo_frame = ttk.LabelFrame(identity_frame, text="Photo", padding=10)
        photo_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        
        if contact.get('photo_path'):
            try:
                from PIL import Image, ImageTk
                img = Image.open(contact['photo_path'])
                img.thumbnail((150, 150))
                photo = ImageTk.PhotoImage(img)
                photo_label = ttk.Label(photo_frame, image=photo)
                photo_label.image = photo
                photo_label.pack()
            except:
                ttk.Label(photo_frame, text="📷\nPhoto\nindisponible", justify=tk.CENTER).pack()
        else:
            ttk.Label(photo_frame, text="📷\nPas de photo", justify=tk.CENTER).pack()
        
        
        info_frame = ttk.Frame(identity_frame)
        info_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        info_text = f"""INFORMATIONS PERSONNELLES
{'═' * 50}
Civilité: {contact.get('civilite', 'N/A')}
Nom: {contact.get('nom', 'N/A')}
Prénom: {contact.get('prenom', 'N/A')}
Date de naissance: {contact.get('date_naissance', 'N/A')}

INFORMATIONS PROFESSIONNELLES
{'═' * 50}
Société: {contact.get('societe', 'N/A')}
Poste: {contact.get('poste', 'N/A')}
Anniversaire professionnel: {contact.get('anniversaire_professionnel', 'N/A')}

CATÉGORISATION
{'═' * 50}
Catégorie: {contact.get('categorie', 'N/A')}

SITE WEB
{'═' * 50}
{contact.get('site_web', 'N/A')}
        """
        
        text_widget = tk.Text(info_frame, wrap=tk.WORD, font=("Courier", 10))
        text_widget.insert(1.0, info_text.strip())
        text_widget.config(state=tk.DISABLED)
        text_widget.pack(fill=tk.BOTH, expand=True)
        
        
        tab_coords = ttk.Frame(notebook, padding="15")
        notebook.add(tab_coords, text="📞 Coordonnées")
        
        coords_frame = ttk.Frame(tab_coords)
        coords_frame.pack(fill=tk.BOTH, expand=True)
        
        
        coordonnees = self.contact_mgr.get_coordonnees(contact_id)
        
        coords_text = "TÉLÉPHONES\n" + "═" * 50 + "\n"
        emails_text = "\n\nEMAILS\n" + "═" * 50 + "\n"
        
        tel_mobile = tel_fixe = tel_pro = ""
        email_pro = email_perso = ""
        
        if coordonnees:
            for coord in coordonnees:
                type_coord = coord['type_coord']
                valeur = coord['valeur']
                if type_coord == 'tel_mobile':
                    tel_mobile = valeur
                    coords_text += f"📱 Mobile: {valeur}\n"
                elif type_coord == 'tel_fixe':
                    tel_fixe = valeur
                    coords_text += f"☎ Fixe: {valeur}\n"
                elif type_coord == 'tel_pro':
                    tel_pro = valeur
                    coords_text += f"📞 Pro: {valeur}\n"
                elif type_coord == 'email_pro':
                    email_pro = valeur
                    emails_text += f"📧 Professionnel: {valeur}\n"
                elif type_coord == 'email_perso':
                    email_perso = valeur
                    emails_text += f"📧 Personnel: {valeur}\n"
        
        if not any([tel_mobile, tel_fixe, tel_pro]):
            coords_text += "Aucun téléphone\n"
        
        if not any([email_pro, email_perso]):
            emails_text += "Aucun email\n"
        
        coords_text += emails_text
        
        coords_text += "\n\nADRESSE POSTALE\n" + "═" * 50 + "\n"
        if contact.get('adresse_rue') or contact.get('adresse_ville'):
            coords_text += f"{contact.get('adresse_rue', '')}\n"
            coords_text += f"{contact.get('adresse_code_postal', '')} {contact.get('adresse_ville', '')}\n"
            coords_text += f"{contact.get('adresse_pays', '')}\n"
        else:
            coords_text += "Aucune adresse\n"
        
        text_coords = tk.Text(coords_frame, wrap=tk.WORD, font=("Courier", 10))
        text_coords.insert(1.0, coords_text)
        text_coords.config(state=tk.DISABLED)
        text_coords.pack(fill=tk.BOTH, expand=True)
        
        
        action_frame = ttk.Frame(tab_coords)
        action_frame.pack(fill=tk.X, pady=(10, 0))
        
        if tel_mobile:
            ttk.Button(action_frame, text=f"📱 Appeler Mobile: {tel_mobile}", 
                      command=lambda: webbrowser.open(f"tel:{tel_mobile}")).pack(side=tk.LEFT, padx=5)
        
        if email_pro:
            ttk.Button(action_frame, text=f"✉ Email Pro", 
                      command=lambda: webbrowser.open(f"mailto:{email_pro}")).pack(side=tk.LEFT, padx=5)
        
        if email_perso:
            ttk.Button(action_frame, text=f"✉ Email Perso", 
                      command=lambda: webbrowser.open(f"mailto:{email_perso}")).pack(side=tk.LEFT, padx=5)
        
        
        tab_sociaux = ttk.Frame(notebook, padding="15")
        notebook.add(tab_sociaux, text="🌐 Réseaux sociaux")
        
        reseaux = self.contact_mgr.get_reseaux_sociaux(contact_id)
        
        if reseaux:
            for reseau in reseaux:
                btn_frame = ttk.Frame(tab_sociaux)
                btn_frame.pack(fill=tk.X, pady=5)
                
                plateforme = reseau['plateforme'].capitalize()
                url = reseau['url']
                
                ttk.Label(btn_frame, text=f"{plateforme}:", font=("", 10, "bold"), width=15).pack(side=tk.LEFT, padx=5)
                ttk.Label(btn_frame, text=url).pack(side=tk.LEFT, padx=5)
                ttk.Button(btn_frame, text="🔗 Ouvrir", 
                          command=lambda u=url: webbrowser.open(u)).pack(side=tk.LEFT, padx=5)
        else:
            ttk.Label(tab_sociaux, text="Aucun réseau social configuré").pack()
        
        
        tab_notes = ttk.Frame(notebook, padding="15")
        notebook.add(tab_notes, text="📝 Notes")
        
        notes = self.contact_mgr.get_notes(contact_id)
        
        if notes:
            notes_text = tk.Text(tab_notes, wrap=tk.WORD, font=("", 10))
            for note in notes:
                notes_text.insert(tk.END, f"[{note.get('date_creation', 'N/A')}]\n{note.get('contenu', '')}\n\n" + "─" * 50 + "\n\n")
            notes_text.config(state=tk.DISABLED)
            notes_text.pack(fill=tk.BOTH, expand=True)
        else:
            ttk.Label(tab_notes, text="Aucune note").pack()
        
        
        tab_historique = ttk.Frame(notebook, padding="15")
        notebook.add(tab_historique, text="📜 Historique")
        
        interactions = self.contact_mgr.get_interactions(contact_id)
        
        if interactions:
            
            hist_frame = ttk.Frame(tab_historique)
            hist_frame.pack(fill=tk.BOTH, expand=True)
            
            vsb = ttk.Scrollbar(hist_frame, orient="vertical")
            
            hist_tree = ttk.Treeview(
                hist_frame,
                columns=("date", "type", "description", "statut"),
                show="headings",
                yscrollcommand=vsb.set,
                height=15
            )
            
            vsb.config(command=hist_tree.yview)
            
            hist_tree.heading("date", text="Date")
            hist_tree.heading("type", text="Type")
            hist_tree.heading("description", text="Description")
            hist_tree.heading("statut", text="Statut")
            
            hist_tree.column("date", width=150)
            hist_tree.column("type", width=100)
            hist_tree.column("description", width=300)
            hist_tree.column("statut", width=100)
            
            for interaction in sorted(interactions, key=lambda x: x.get('date_heure', ''), reverse=True):
                hist_tree.insert("", "end", values=(
                    interaction.get('date_heure', 'N/A'),
                    interaction.get('type_interaction', 'N/A'),
                    interaction.get('description', '')[:50] + '...' if len(interaction.get('description', '')) > 50 else interaction.get('description', ''),
                    interaction.get('statut', 'N/A')
                ))
            
            hist_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            vsb.pack(side=tk.RIGHT, fill=tk.Y)
        else:
            ttk.Label(tab_historique, text="Aucune interaction enregistrée").pack()
        
        
        ttk.Button(main_frame, text="Fermer", command=window.destroy).pack(pady=(10, 0))
    
    def export_contact(self, contact_id):
        
        contact = self.contact_mgr.get_contact(contact_id)
        if not contact:
            return
        
        filename = filedialog.asksaveasfilename(
            title="Exporter la fiche contact",
            defaultextension=".csv",
            filetypes=[("CSV", "*.csv"), ("Tous les fichiers", "*.*")],
            initialfile=f"contact_{contact['nom']}_{contact['prenom']}.csv"
        )
        
        if filename:
            try:
                import csv
                with open(filename, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    writer.writerow(["Champ", "Valeur"])
                    for key, value in contact.items():
                        writer.writerow([key, value])
                messagebox.showinfo("Succès", f"Fiche exportée vers {filename}", parent=self.parent)
            except Exception as e:
                messagebox.showerror("Erreur", f"Erreur lors de l'export: {str(e)}", parent=self.parent)
    
    def quick_add_interaction(self, contact_id):
        if self.notebook:
            self.notebook.select(2)

    def quick_add_rappel(self, contact_id):
        if self.notebook:
            self.notebook.select(3)
