"""Configuration globale de l'interface utilisateur"""
from tkinter import ttk
import tkinter.font as tkfont


COLORS = {
    'primary': '#2563eb',
    'primary_dark': '#1e40af',
    'primary_light': '#3b82f6',
    
    'secondary': '#64748b',
    'secondary_dark': '#475569',
    'secondary_light': '#94a3b8',
    
    'accent': '#10b981',
    'accent_warning': '#f59e0b',
    'accent_danger': '#ef4444',
    
    'bg_primary': '#ffffff',
    'bg_secondary': '#f8fafc',
    'bg_tertiary': '#e2e8f0',
    'bg_dark': '#1e293b',
    
    'text_primary': '#0f172a',
    'text_secondary': '#475569',
    'text_light': '#94a3b8',
    'text_white': '#ffffff',
    
    'border': '#cbd5e1',
    'border_focus': '#2563eb',
    
    'success': '#10b981',
    'warning': '#f59e0b',
    'error': '#ef4444',
    'info': '#3b82f6',
}


def configure_styles(root):
    """Configure les styles globaux de l'application"""
    style = ttk.Style(root)
    
    try:
        style.theme_use('clam')
    except:
        pass
    
    root.configure(bg=COLORS['bg_secondary'])
    
    default_font = tkfont.nametofont("TkDefaultFont")
    font_height = default_font.metrics("linespace")
    rowheight = font_height + 8
    
    style.configure("Treeview", 
                   rowheight=rowheight,
                   font=("", 10),
                   background=COLORS['bg_primary'],
                   foreground=COLORS['text_primary'],
                   fieldbackground=COLORS['bg_primary'],
                   borderwidth=0)
    
    style.configure("Treeview.Heading",
                   font=("", 10, "bold"),
                   padding=5,
                   background=COLORS['primary'],
                   foreground=COLORS['text_white'],
                   relief="flat")
    
    style.map("Treeview.Heading",
             background=[('active', COLORS['primary_dark'])])
    
    style.map("Treeview",
             background=[('selected', COLORS['primary_light'])],
             foreground=[('selected', COLORS['text_white'])])
    
    style.configure("TButton",
                   padding=6,
                   font=("", 10),
                   background=COLORS['secondary'],
                   foreground=COLORS['text_primary'],
                   borderwidth=1,
                   relief="flat")
    
    style.map("TButton",
             background=[('active', COLORS['secondary_dark']),
                        ('pressed', COLORS['secondary'])],
             relief=[('pressed', 'flat')])
    
    style.configure("Accent.TButton",
                   padding=8,
                   font=("", 10, "bold"),
                   background=COLORS['primary'],
                   foreground=COLORS['text_white'],
                   borderwidth=0,
                   relief="flat")
    
    style.map("Accent.TButton",
             background=[('active', COLORS['primary_dark']),
                        ('pressed', COLORS['primary'])],
             relief=[('pressed', 'flat')])
    
    style.configure("Success.TButton",
                   padding=6,
                   font=("", 10),
                   background=COLORS['success'],
                   foreground=COLORS['text_white'],
                   borderwidth=0,
                   relief="flat")
    
    style.map("Success.TButton",
             background=[('active', '#059669'),
                        ('pressed', COLORS['success'])])
    
    style.configure("Danger.TButton",
                   padding=6,
                   font=("", 10),
                   background=COLORS['error'],
                   foreground=COLORS['text_white'],
                   borderwidth=0,
                   relief="flat")
    
    style.map("Danger.TButton",
             background=[('active', '#dc2626'),
                        ('pressed', COLORS['error'])])
    
    style.configure("TLabel",
                   font=("", 10),
                   background=COLORS['bg_secondary'],
                   foreground=COLORS['text_primary'])
    
    style.configure("Title.TLabel",
                   font=("", 14, "bold"),
                   background=COLORS['bg_secondary'],
                   foreground=COLORS['text_primary'])
    
    style.configure("Subtitle.TLabel",
                   font=("", 11),
                   background=COLORS['bg_secondary'],
                   foreground=COLORS['text_secondary'])
    
    style.configure("Info.TLabel",
                   font=("", 9),
                   background=COLORS['bg_secondary'],
                   foreground=COLORS['text_light'])
    
    style.configure("TFrame",
                   background=COLORS['bg_secondary'])
    
    style.configure("Card.TFrame",
                   background=COLORS['bg_primary'],
                   relief="solid",
                   borderwidth=1)
    
    style.configure("TLabelframe",
                   background=COLORS['bg_secondary'],
                   foreground=COLORS['text_primary'],
                   borderwidth=2,
                   relief="solid",
                   bordercolor=COLORS['border'])
    
    style.configure("TLabelframe.Label",
                   font=("", 10, "bold"),
                   background=COLORS['bg_secondary'],
                   foreground=COLORS['primary'])
    
    style.configure("TEntry",
                   fieldbackground=COLORS['bg_primary'],
                   foreground=COLORS['text_primary'],
                   bordercolor=COLORS['border'],
                   lightcolor=COLORS['border_focus'],
                   darkcolor=COLORS['border'],
                   borderwidth=1,
                   relief="solid")
    
    style.map("TEntry",
             bordercolor=[('focus', COLORS['border_focus'])],
             lightcolor=[('focus', COLORS['border_focus'])])
    
    style.configure("TCombobox",
                   fieldbackground=COLORS['bg_primary'],
                   background=COLORS['bg_primary'],
                   foreground=COLORS['text_primary'],
                   bordercolor=COLORS['border'],
                   arrowcolor=COLORS['secondary'],
                   borderwidth=1)
    
    style.map("TCombobox",
             fieldbackground=[('readonly', COLORS['bg_primary'])],
             selectbackground=[('readonly', COLORS['bg_primary'])],
             bordercolor=[('focus', COLORS['border_focus'])])
    
    style.configure("TNotebook",
                   background=COLORS['bg_secondary'],
                   borderwidth=0)
    
    style.configure("TNotebook.Tab",
                   padding=[15, 8],
                   font=("", 10),
                   background=COLORS['bg_tertiary'],
                   foreground=COLORS['text_secondary'])
    
    style.map("TNotebook.Tab",
             background=[('selected', COLORS['bg_primary']),
                        ('active', COLORS['bg_secondary'])],
             foreground=[('selected', COLORS['primary'])])
    
    style.configure("TScrollbar",
                   background=COLORS['bg_tertiary'],
                   troughcolor=COLORS['bg_secondary'],
                   borderwidth=0,
                   arrowcolor=COLORS['secondary'])
    
    style.map("TScrollbar",
             background=[('active', COLORS['secondary'])])


def create_centered_frame(parent, padding="20"):
    """Crée un frame centré qui s'adapte au redimensionnement"""
    # Frame principal qui remplit tout l'espace
    outer_frame = ttk.Frame(parent)
    outer_frame.pack(fill="both", expand=True)
    
    # Frame centré
    centered_frame = ttk.Frame(outer_frame, padding=padding)
    centered_frame.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.95, relheight=0.95)
    
    return centered_frame


def create_scrollable_frame(parent):
    """Crée un frame avec scrollbar qui s'adapte au redimensionnement"""
    import tkinter as tk
    
    # Frame conteneur
    container = ttk.Frame(parent)
    container.pack(fill="both", expand=True)
    
    # Canvas pour le scrolling
    canvas = tk.Canvas(container, highlightthickness=0)
    scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
    
    # Frame scrollable
    scrollable_frame = ttk.Frame(canvas)
    
    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )
    
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    
    # Pack
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    
    # Activer le scroll avec la molette
    def _on_mousewheel(event):
        canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    
    canvas.bind_all("<MouseWheel>", _on_mousewheel)
    
    return scrollable_frame, canvas
