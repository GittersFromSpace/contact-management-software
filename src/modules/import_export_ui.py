import tkinter as tk
from tkinter import ttk, messagebox, filedialog


class ImportExportUI:
    
    def __init__(self, root, import_export_mgr, db):
        self.root = root
        self.import_export_mgr = import_export_mgr
        self.db = db
    
    def import_csv(self):
        messagebox.showinfo("Info", "Fonctionnalité en développement")
    
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
