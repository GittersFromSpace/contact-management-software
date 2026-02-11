import tkinter as tk
from tkinter import ttk
from utils.ui_config import COLORS


class DashboardUI:

    def __init__(self, parent, stats_mgr, rappel_mgr):
        self.parent = parent
        self.stats_mgr = stats_mgr
        self.rappel_mgr = rappel_mgr
        self.tab = None
        self.notebook = None

    def create_dashboard_tab(self, notebook):
        self.notebook = notebook
        self.tab = ttk.Frame(notebook, padding="20")
        notebook.add(self.tab, text="Tableau de bord")

        self._build_content()

        notebook.bind("<<NotebookTabChanged>>", self._on_tab_changed)

    def _on_tab_changed(self, event):
        if self.notebook.select() == str(self.tab):
            self.refresh()

    def refresh(self):
        for widget in self.tab.winfo_children():
            widget.destroy()
        self._build_content()

    def _build_content(self):
        ttk.Label(self.tab, text="Tableau de bord", style="Title.TLabel").pack(pady=(0, 25))

        stats = self.stats_mgr.get_global_statistics()

        stats_container = ttk.Frame(self.tab)
        stats_container.pack(fill=tk.X, pady=(0, 20))

        stat_cards = [
            ("total_contacts", "Contacts", COLORS['primary']),
            ("total_interactions", "Interactions", COLORS['info']),
            ("total_taches", "Tâches", COLORS['accent_warning']),
            ("total_rappels", "Rappels", COLORS['accent']),
            ("rappels_aujourd_hui", "Rappels aujourd'hui", COLORS['error']),
            ("taches_en_cours", "Tâches en cours", COLORS['secondary']),
        ]

        for idx, (key, label, color) in enumerate(stat_cards):
            if key in stats:
                card = self._create_stat_card(stats_container, stats[key], label, color)
                card.grid(row=idx // 3, column=idx % 3, padx=8, pady=8, sticky="nsew")

        for i in range(3):
            stats_container.columnconfigure(i, weight=1)

        rappels_container = ttk.Frame(self.tab)
        rappels_container.pack(fill=tk.BOTH, expand=True)

        header_frame = ttk.Frame(rappels_container)
        header_frame.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(header_frame, text="Rappels d'aujourd'hui", style="Subtitle.TLabel").pack(side=tk.LEFT)

        rappels = self.rappel_mgr.get_rappels_aujourdhui()

        if rappels:
            rappels_card = tk.Frame(rappels_container, bg=COLORS['bg_primary'],
                                   relief="solid", borderwidth=1, highlightthickness=0)
            rappels_card.pack(fill=tk.BOTH, expand=True)

            rappels_tree = ttk.Treeview(
                rappels_card,
                columns=("contact", "titre", "heure", "priorite"),
                show="headings",
                height=10
            )

            rappels_tree.heading("contact", text="Contact")
            rappels_tree.heading("titre", text="Titre")
            rappels_tree.heading("heure", text="Heure")
            rappels_tree.heading("priorite", text="Priorité")

            rappels_tree.column("contact", width=200)
            rappels_tree.column("titre", width=300)
            rappels_tree.column("heure", width=120)
            rappels_tree.column("priorite", width=100)

            vsb = ttk.Scrollbar(rappels_card, orient="vertical", command=rappels_tree.yview)
            rappels_tree.configure(yscrollcommand=vsb.set)

            for rappel in rappels:
                contact_name = f"{rappel['prenom']} {rappel['nom']}"
                priority_display = self._get_priority_display(rappel['priorite'])
                rappels_tree.insert("", "end", values=(
                    contact_name,
                    rappel['titre'],
                    rappel['date_heure'],
                    priority_display
                ))

            rappels_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=1, pady=1)
            vsb.pack(side=tk.RIGHT, fill=tk.Y)
        else:
            empty_card = tk.Frame(rappels_container, bg=COLORS['bg_primary'],
                                 relief="solid", borderwidth=1, highlightthickness=0)
            empty_card.pack(fill=tk.BOTH, expand=True)

            empty_label = tk.Label(empty_card, text="Aucun rappel pour aujourd'hui",
                                  font=("Segoe UI", 11), bg=COLORS['bg_primary'],
                                  fg=COLORS['text_secondary'])
            empty_label.pack(expand=True, pady=40)

        # --- Rappels des 7 prochains jours ---
        week_container = ttk.Frame(self.tab)
        week_container.pack(fill=tk.BOTH, expand=True, pady=(10, 0))

        ttk.Label(week_container, text="Rappels des 7 prochains jours", style="Subtitle.TLabel").pack(anchor=tk.W, pady=(0, 5))

        rappels_week = self.rappel_mgr.get_rappels(traite=0, jours_futur=7)

        if rappels_week:
            week_card = tk.Frame(week_container, bg=COLORS['bg_primary'],
                                 relief="solid", borderwidth=1, highlightthickness=0)
            week_card.pack(fill=tk.BOTH, expand=True)

            week_tree = ttk.Treeview(
                week_card,
                columns=("contact", "titre", "heure", "priorite"),
                show="headings",
                height=min(len(rappels_week), 8)
            )

            week_tree.heading("contact", text="Contact")
            week_tree.heading("titre", text="Titre")
            week_tree.heading("heure", text="Date/Heure")
            week_tree.heading("priorite", text="Priorité")

            week_tree.column("contact", width=200)
            week_tree.column("titre", width=300)
            week_tree.column("heure", width=150)
            week_tree.column("priorite", width=100)

            week_vsb = ttk.Scrollbar(week_card, orient="vertical", command=week_tree.yview)
            week_tree.configure(yscrollcommand=week_vsb.set)

            for rappel in rappels_week:
                contact_name = f"{rappel['prenom']} {rappel['nom']}"
                priority_display = self._get_priority_display(rappel['priorite'])
                week_tree.insert("", "end", values=(
                    contact_name,
                    rappel['titre'],
                    rappel['date_heure'],
                    priority_display
                ))

            week_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=1, pady=1)
            week_vsb.pack(side=tk.RIGHT, fill=tk.Y)
        else:
            empty_week = tk.Frame(week_container, bg=COLORS['bg_primary'],
                                  relief="solid", borderwidth=1, highlightthickness=0)
            empty_week.pack(fill=tk.BOTH, expand=True)
            tk.Label(empty_week, text="Aucun rappel pour les 7 prochains jours",
                     font=("Segoe UI", 11), bg=COLORS['bg_primary'],
                     fg=COLORS['text_secondary']).pack(expand=True, pady=40)

    def _create_stat_card(self, parent, value, label, color):
        card = tk.Frame(parent, bg=COLORS['bg_primary'], relief="solid",
                       borderwidth=1, highlightthickness=0)

        content = tk.Frame(card, bg=COLORS['bg_primary'])
        content.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)

        value_label = tk.Label(content, text=str(value), font=("Segoe UI", 28, "bold"),
                              bg=COLORS['bg_primary'], fg=color)
        value_label.pack(anchor=tk.W)

        text_label = tk.Label(content, text=label, font=("Segoe UI", 11),
                             bg=COLORS['bg_primary'], fg=COLORS['text_secondary'])
        text_label.pack(anchor=tk.W, pady=(5, 0))

        return card

    def _get_priority_display(self, priority):
        priority_map = {
            'haute': '● Haute',
            'moyenne': '● Moyenne',
            'basse': '● Basse'
        }
        return priority_map.get(priority, priority)
