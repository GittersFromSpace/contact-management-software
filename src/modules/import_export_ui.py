import tkinter as tk
from tkinter import ttk, messagebox, filedialog


class ImportExportUI:
    
    def __init__(self, root, import_export_mgr, db):
        self.root = root
        self.import_export_mgr = import_export_mgr
        self.db = db
    
    def import_csv(self):
        file_path = filedialog.askopenfilename(
            title="Importer un fichier CSV",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        if not file_path:
            return

        try:
            import csv
            with open(file_path, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                csv_headers = next(reader)
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible de lire le fichier: {e}", parent=self.root)
            return

        db_fields = [
            ('', '-- Ignorer --'),
            ('civilite', 'Civilité'),
            ('nom', 'Nom'),
            ('prenom', 'Prénom'),
            ('societe', 'Société'),
            ('poste', 'Poste'),
            ('categorie', 'Catégorie'),
            ('date_naissance', 'Date de naissance'),
            ('site_web', 'Site web'),
            ('adresse_rue', 'Adresse rue'),
            ('adresse_code_postal', 'Code postal'),
            ('adresse_ville', 'Ville'),
            ('adresse_pays', 'Pays'),
        ]

        auto_map = {
            'civilite': 'civilite', 'civilité': 'civilite',
            'nom': 'nom', 'name': 'nom', 'last_name': 'nom', 'lastname': 'nom',
            'prenom': 'prenom', 'prénom': 'prenom', 'first_name': 'prenom', 'firstname': 'prenom',
            'societe': 'societe', 'société': 'societe', 'company': 'societe', 'entreprise': 'societe',
            'poste': 'poste', 'title': 'poste', 'job': 'poste', 'fonction': 'poste',
            'categorie': 'categorie', 'catégorie': 'categorie', 'category': 'categorie',
            'date_naissance': 'date_naissance', 'birthday': 'date_naissance',
            'site_web': 'site_web', 'website': 'site_web', 'url': 'site_web',
            'adresse_rue': 'adresse_rue', 'rue': 'adresse_rue', 'street': 'adresse_rue', 'adresse': 'adresse_rue',
            'adresse_code_postal': 'adresse_code_postal', 'code_postal': 'adresse_code_postal', 'zip': 'adresse_code_postal', 'cp': 'adresse_code_postal',
            'adresse_ville': 'adresse_ville', 'ville': 'adresse_ville', 'city': 'adresse_ville',
            'adresse_pays': 'adresse_pays', 'pays': 'adresse_pays', 'country': 'adresse_pays',
        }

        win = tk.Toplevel(self.root)
        win.title("Mapping des colonnes CSV")
        win.geometry("700x500")
        win.transient(self.root)
        win.lift()
        win.focus_force()

        frm = ttk.Frame(win, padding=20)
        frm.pack(fill=tk.BOTH, expand=True)

        ttk.Label(frm, text="Associez chaque colonne CSV à un champ", font=("", 13, "bold")).pack(pady=(0, 15))

        canvas = tk.Canvas(frm)
        scrollbar = ttk.Scrollbar(frm, orient="vertical", command=canvas.yview)
        scroll_frame = ttk.Frame(canvas)

        scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        combos = {}
        field_values = [label for _, label in db_fields]

        for idx, header in enumerate(csv_headers):
            row_frame = ttk.Frame(scroll_frame)
            row_frame.pack(fill=tk.X, pady=3, padx=5)

            ttk.Label(row_frame, text=header, font=("", 10, "bold"), width=25).pack(side=tk.LEFT, padx=(0, 10))
            ttk.Label(row_frame, text="→", font=("", 12)).pack(side=tk.LEFT, padx=5)

            var = tk.StringVar(value='-- Ignorer --')
            matched = auto_map.get(header.lower().strip())
            if matched:
                for db_key, db_label in db_fields:
                    if db_key == matched:
                        var.set(db_label)
                        break

            combo = ttk.Combobox(row_frame, textvariable=var, values=field_values, state="readonly", width=25)
            combo.pack(side=tk.LEFT, padx=5)
            combos[header] = (var, db_fields)

        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        def do_import():
            mapping = {}
            for csv_col, (var, fields) in combos.items():
                selected_label = var.get()
                for db_key, db_label in fields:
                    if db_label == selected_label and db_key:
                        mapping[csv_col] = db_key
                        break

            if not mapping:
                messagebox.showerror("Erreur", "Aucune colonne mappée", parent=win)
                return

            success, imported, duplicates, errors = self.import_export_mgr.import_from_csv(file_path, mapping)

            if success:
                msg = f"Import terminé:\n- {imported} contact(s) importé(s)\n- {duplicates} doublon(s) ignoré(s)"
                if errors:
                    msg += f"\n- {len(errors)} erreur(s)"
                messagebox.showinfo("Résultat", msg, parent=win)
                win.destroy()
            else:
                messagebox.showerror("Erreur", f"Erreur: {errors}", parent=win)

        btn_frame = ttk.Frame(frm)
        btn_frame.pack(fill=tk.X, pady=(15, 0))
        ttk.Button(btn_frame, text="Importer", command=do_import, style="Accent.TButton").pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Annuler", command=win.destroy).pack(side=tk.LEFT, padx=5)
    
    def export_csv(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        if file_path:
            success, message = self.import_export_mgr.export_to_csv(file_path)
            if success:
                messagebox.showinfo("Succès", message)
            else:
                messagebox.showerror("Erreur", message)
    
    def export_vcard(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".vcf",
            filetypes=[("vCard files", "*.vcf"), ("All files", "*.*")]
        )
        if file_path:
            success, message = self.import_export_mgr.export_to_vcard(file_path)
            if success:
                messagebox.showinfo("Succès", message)
            else:
                messagebox.showerror("Erreur", message)
    
    def detect_duplicates(self):
        duplicates = self.import_export_mgr.find_duplicates()
        if duplicates:
            messagebox.showinfo("Doublons", f"{len(duplicates)} doublons potentiels trouvés")
        else:
            messagebox.showinfo("Doublons", "Aucun doublon trouvé")
    
    def backup_database(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".db",
            filetypes=[("SQLite Database", "*.db")]
        )
        if file_path:
            success, message = self.db.backup_database(file_path)
            if success:
                messagebox.showinfo("Succès", f"Sauvegarde créée: {message}")
            else:
                messagebox.showerror("Erreur", message)
