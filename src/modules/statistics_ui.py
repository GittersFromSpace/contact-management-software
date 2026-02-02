import tkinter as tk
from tkinter import ttk, messagebox, filedialog


class StatisticsUI:
    
    def __init__(self, root, stats_mgr):
        self.root = root
        self.stats_mgr = stats_mgr
    
    def show_statistics(self):
        stats = self.stats_mgr.get_global_statistics()
        message = "\n".join([f"{k.replace('_', ' ').title()}: {v}" for k, v in stats.items()])
        messagebox.showinfo("Statistiques", message, parent=self.root)
    
    def generate_charts(self):
        output_dir = filedialog.askdirectory(title="Choisir le dossier de sortie")
        if output_dir:
            success, message = self.stats_mgr.generate_charts(output_dir)
            if success:
                messagebox.showinfo("Succès", message, parent=self.root)
            else:
                messagebox.showerror("Erreur", message, parent=self.root)
    
    def export_statistics(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv")]
        )
        if file_path:
            success, message = self.stats_mgr.export_statistics_to_csv(file_path)
            if success:
                messagebox.showinfo("Succès", message, parent=self.root)
            else:
                messagebox.showerror("Erreur", message, parent=self.root)
