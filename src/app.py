import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from utils.database_manager import DatabaseManager
from utils.auth_manager import AuthManager
from utils.ui_config import configure_styles
from modules.contact_manager import ContactManager
from modules.contact_ui import ContactUI
from modules.interaction_manager import InteractionManager, RappelManager
from modules.tag_relation_manager import TagManager, RelationManager
from modules.task_manager import TaskManager, ProjetManager
from modules.import_export_manager import ImportExportManager
from modules.statistics_manager import StatisticsManager

from modules.dashboard_ui import DashboardUI
from modules.interaction_ui import InteractionUI
from modules.rappel_ui import RappelUI
from modules.task_ui import TaskUI
from modules.tag_relation_ui import TagRelationUI
from modules.projet_ui import ProjetUI
from modules.import_export_ui import ImportExportUI
from modules.statistics_ui import StatisticsUI


class LoginWindow:
    
    def __init__(self, root, auth_manager, on_success):
        self.root = root
        self.auth = auth_manager
        self.on_success = on_success
        
        self.window = tk.Toplevel(root)
        self.window.geometry("450x350")
        self.window.resizable(True, True)
        
        self.window.transient(root)
        self.window.grab_set()
        
        self.create_widgets()
    
    def create_widgets(self):
        main_frame = ttk.Frame(self.window, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(main_frame, text="Nom d'utilisateur:").pack(anchor=tk.W, pady=(10, 5))
        self.username_var = tk.StringVar(value="admin")
        username_entry = ttk.Entry(main_frame, textvariable=self.username_var, width=30)
        username_entry.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(main_frame, text="Mot de passe:").pack(anchor=tk.W, pady=(10, 5))
        self.password_var = tk.StringVar(value="admin")
        password_entry = ttk.Entry(main_frame, textvariable=self.password_var, show="*", width=30)
        password_entry.pack(fill=tk.X, pady=(0, 20))
        
        password_entry.bind("<Return>", lambda e: self.login())
        
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X)

        ttk.Button(
            button_frame,
            text="Se connecter",
            command=self.login
        ).pack(side=tk.LEFT, padx=10, expand=True)

        ttk.Button(
            button_frame,
            text="Quitter",
            command=self.root.quit
        ).pack(side=tk.LEFT, expand=True)
        
        info_label = ttk.Label(
            main_frame,
            text="Identifiants par défaut: admin / admin",
            font=("", 8, "italic"),
            foreground="gray"
        )
        info_label.pack(pady=(10, 0))
    
    def login(self):
        username = self.username_var.get()
        password = self.password_var.get()
        
        if not username or not password:
            messagebox.showerror("Erreur", "Veuillez remplir tous les champs")
            return
        
        success, user = self.auth.authenticate(username, password)
        
        if success:
            self.window.destroy()
            self.on_success(user)
        else:
            messagebox.showerror("Erreur", "Identifiants incorrects")


class MainApplication:
    
    def __init__(self, root):
        self.root = root
        self.root.title("Gestion de Contacts Avancée")
        self.root.geometry("1400x900")
        self.root.minsize(1000, 600)
        
        # Configurer les styles globaux
        configure_styles(self.root)
        
        self.db = DatabaseManager()
        self.auth = AuthManager(self.db)
        
        LoginWindow(self.root, self.auth, self.on_login_success)
    
    def on_login_success(self, user):
        self.current_user = user
        
        self.contact_mgr = ContactManager(self.db, self.auth)
        self.interaction_mgr = InteractionManager(self.db, self.auth)
        self.rappel_mgr = RappelManager(self.db, self.auth)
        self.tag_mgr = TagManager(self.db, self.auth)
        self.relation_mgr = RelationManager(self.db, self.auth)
        self.task_mgr = TaskManager(self.db, self.auth)
        self.projet_mgr = ProjetManager(self.db, self.auth)
        self.import_export_mgr = ImportExportManager(self.db, self.auth, self.contact_mgr)
        self.stats_mgr = StatisticsManager(self.db)
        
        self.dashboard_ui = DashboardUI(self.root, self.stats_mgr, self.rappel_mgr)
        self.interaction_ui = InteractionUI(self.root, self.interaction_mgr, self.contact_mgr)
        self.rappel_ui = RappelUI(self.root, self.rappel_mgr, self.contact_mgr)
        self.task_ui = TaskUI(self.root, self.task_mgr, self.contact_mgr)
        self.tag_relation_ui = TagRelationUI(self.root, self.tag_mgr, self.relation_mgr, self.contact_mgr)
        self.projet_ui = ProjetUI(self.root, self.projet_mgr, self.task_mgr, self.contact_mgr)
        self.import_export_ui = ImportExportUI(self.root, self.import_export_mgr, self.db)
        self.statistics_ui = StatisticsUI(self.root, self.stats_mgr)
        
        self.create_main_interface()
        
        self.root.deiconify()
    
    def create_main_interface(self):
        main_container = ttk.Frame(self.root)
        main_container.pack(fill=tk.BOTH, expand=True)
        
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Fichier", menu=file_menu)
        file_menu.add_command(label="Sauvegarder la base", command=self.import_export_ui.backup_database)
        file_menu.add_separator()
        file_menu.add_command(label="Déconnexion", command=self.logout)
        file_menu.add_command(label="Quitter", command=self.root.quit)
        
        import_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Import/Export", menu=import_menu)
        import_menu.add_command(label="Importer CSV", command=self.import_export_ui.import_csv)
        import_menu.add_command(label="Exporter CSV", command=self.import_export_ui.export_csv)
        import_menu.add_command(label="Exporter vCard", command=self.import_export_ui.export_vcard)
        import_menu.add_separator()
        import_menu.add_command(label="Détecter les doublons", command=self.import_export_ui.detect_duplicates)
        
        stats_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Statistiques", menu=stats_menu)
        stats_menu.add_command(label="Voir les statistiques", command=self.statistics_ui.show_statistics)
        stats_menu.add_command(label="Générer des graphiques", command=self.statistics_ui.generate_charts)
        stats_menu.add_command(label="Exporter statistiques CSV", command=self.statistics_ui.export_statistics)
        
        # Menu Utilisateurs (si permissions)
        if self.auth.has_permission('create_user'):
            users_menu = tk.Menu(menubar, tearoff=0)
            menubar.add_cascade(label="Utilisateurs", menu=users_menu)
            users_menu.add_command(label="Gérer les utilisateurs", command=lambda: self.notebook.select(6))
            users_menu.add_command(label="Nouvel utilisateur", command=self.user_ui.add_user)
            users_menu.add_separator()
            users_menu.add_command(label="Changer mon mot de passe", command=self.user_ui.change_my_password)
        
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Aide", menu=help_menu)
        help_menu.add_command(label="À propos", command=self.show_about)
        
        # En-tête avec info utilisateur
        header = ttk.Frame(main_container, relief=tk.FLAT)
        header.pack(fill=tk.X, padx=10, pady=(5, 0))
        
        user_info = f"Connecté: {self.current_user['prenom']} {self.current_user['nom']} | Rôle: {self.current_user['role']}"
        ttk.Label(header, text=user_info, font=("", 11, "bold"), foreground="#2c3e50").pack(side=tk.LEFT, padx=10, pady=8)
        
        # Notebook principal avec meilleure mise en page
        self.notebook = ttk.Notebook(main_container)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.dashboard_ui.create_dashboard_tab(self.notebook)
        
        contact_tab = ttk.Frame(self.notebook)
        self.notebook.add(contact_tab, text="Contacts")
        contact_ui = ContactUI(self.root, self.contact_mgr, self.auth)
        contact_ui.create_main_interface(contact_tab)
        
        self.interaction_ui.create_interactions_tab(self.notebook)
        self.rappel_ui.create_rappels_tab(self.notebook)
        self.task_ui.create_tasks_tab(self.notebook)
        self.tag_relation_ui.create_tags_relations_tab(self.notebook)
        self.projet_ui.create_projets_tab(self.notebook)
    
    def logout(self):
        if messagebox.askyesno("Déconnexion", "Voulez-vous vraiment vous déconnecter ?"):
            self.auth.logout()
            self.root.withdraw()
            LoginWindow(self.root, self.auth, self.on_login_success)
    
    def show_about(self):
        messagebox.showinfo(
            "À propos",
            "Gestion de Contacts Avancée\nVersion 1.0\n\n"
            "Application de gestion de contacts professionnelle\n"
            "avec suivi des interactions, rappels, tâches et projets."
        )


def main():
    root = tk.Tk()
    app = MainApplication(root)
    root.mainloop()


if __name__ == "__main__":
    main()
