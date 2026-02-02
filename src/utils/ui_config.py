"""Configuration globale de l'interface utilisateur"""
from tkinter import ttk
import tkinter.font as tkfont


THEMES = {
    'light': {
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
    },
    'dark': {
        'primary': '#60a5fa',
        'primary_dark': '#3b82f6',
        'primary_light': '#93c5fd',
        
        'secondary': '#94a3b8',
        'secondary_dark': '#cbd5e1',
        'secondary_light': '#64748b',
        
        'accent': '#34d399',
        'accent_warning': '#fbbf24',
        'accent_danger': '#f87171',
        
        'bg_primary': '#1e293b',
        'bg_secondary': '#0f172a',
        'bg_tertiary': '#334155',
        'bg_dark': '#020617',
        
        'text_primary': '#f1f5f9',
        'text_secondary': '#cbd5e1',
        'text_light': '#94a3b8',
        'text_white': '#ffffff',
        
        'border': '#475569',
        'border_focus': '#60a5fa',
        
        'success': '#34d399',
        'warning': '#fbbf24',
        'error': '#f87171',
        'info': '#60a5fa',
    }
}

FONTS = {
    'base': ('Segoe UI', 11),
    'small': ('Segoe UI', 10),
    'large': ('Segoe UI', 12),
    'title': ('Segoe UI', 18, 'bold'),
    'subtitle': ('Segoe UI', 13, 'bold'),
    'heading': ('Segoe UI', 11, 'bold'),
}

_current_theme = 'light'
COLORS = THEMES[_current_theme]


def load_theme_preference(db_manager):
    """Load saved theme preference from database"""
    global _current_theme, COLORS
    try:
        theme = db_manager.get_setting('theme', 'light')
        _current_theme = theme
        COLORS = THEMES[_current_theme]
    except Exception:
        pass


def save_theme_preference(db_manager, theme):
    """Save theme preference to database"""
    try:
        db_manager.set_setting('theme', theme)
    except Exception:
        pass


def get_current_theme():
    """Get current theme name"""
    return _current_theme


def set_theme(db_manager, theme_name):
    """Change the current theme"""
    global _current_theme, COLORS
    if theme_name in THEMES:
        _current_theme = theme_name
        COLORS = THEMES[theme_name]
        save_theme_preference(db_manager, theme_name)
        return True
    return False


def apply_theme(root):
    """Apply theme to existing window without restart"""
    configure_styles(root)
    
    for widget in root.winfo_children():
        _update_widget_colors(widget)
        _update_treeview_tags(widget)


def _update_treeview_tags(widget):
    """Recursively update treeview tags"""
    try:
        if widget.winfo_class() == 'Treeview':
            configure_treeview_tags(widget)
        
        for child in widget.winfo_children():
            _update_treeview_tags(child)
    except:
        pass


def _update_widget_colors(widget):
    """Recursively update widget colors"""
    try:
        widget_type = widget.winfo_class()
        
        if widget_type in ('Frame', 'TFrame'):
            widget.configure(background=COLORS['bg_primary'])
        elif widget_type == 'Label':
            widget.configure(bg=COLORS['bg_primary'], fg=COLORS['text_primary'])
        
        for child in widget.winfo_children():
            _update_widget_colors(child)
    except:
        pass


def apply_theme(root):
    """Apply the current theme to all widgets"""
    global COLORS
    COLORS = THEMES[_current_theme]
    configure_styles(root)


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
    rowheight = max(font_height + 12, 28)
    
    style.configure("Treeview", 
                   rowheight=rowheight,
                   font=FONTS['base'],
                   background=COLORS['bg_primary'],
                   foreground=COLORS['text_primary'],
                   fieldbackground=COLORS['bg_primary'],
                   borderwidth=0)
    
    style.configure("Treeview.Heading",
                   font=FONTS['heading'],
                   padding=8,
                   background=COLORS['primary'],
                   foreground=COLORS['text_white'],
                   relief="flat")
    
    style.map("Treeview.Heading",
             background=[('active', COLORS['primary_dark'])])
    
    style.map("Treeview",
             background=[('selected', COLORS['primary_light'])],
             foreground=[('selected', COLORS['text_white'])])
    
    style.configure("TButton",
                   padding=(12, 8),
                   font=FONTS['base'],
                   background=COLORS['secondary'],
                   foreground=COLORS['text_primary'],
                   borderwidth=1,
                   relief="flat")
    
    style.map("TButton",
             background=[('active', COLORS['secondary_dark']),
                        ('pressed', COLORS['secondary'])],
             relief=[('pressed', 'flat')])
    
    style.configure("Accent.TButton",
                   padding=(14, 10),
                   font=FONTS['heading'],
                   background=COLORS['primary'],
                   foreground=COLORS['text_white'],
                   borderwidth=0,
                   relief="flat")
    
    style.map("Accent.TButton",
             background=[('active', COLORS['primary_dark']),
                        ('pressed', COLORS['primary'])],
             relief=[('pressed', 'flat')])
    
    style.configure("Success.TButton",
                   padding=(12, 8),
                   font=FONTS['base'],
                   background=COLORS['success'],
                   foreground=COLORS['text_white'],
                   borderwidth=0,
                   relief="flat")
    
    style.map("Success.TButton",
             background=[('active', '#059669'),
                        ('pressed', COLORS['success'])])
    
    style.configure("Danger.TButton",
                   padding=(12, 8),
                   font=FONTS['base'],
                   background=COLORS['error'],
                   foreground=COLORS['text_white'],
                   borderwidth=0,
                   relief="flat")
    
    style.map("Danger.TButton",
             background=[('active', '#dc2626'),
                        ('pressed', COLORS['error'])])
    
    style.configure("TLabel",
                   font=FONTS['base'],
                   background=COLORS['bg_secondary'],
                   foreground=COLORS['text_primary'])
    
    style.configure("Title.TLabel",
                   font=FONTS['title'],
                   background=COLORS['bg_secondary'],
                   foreground=COLORS['text_primary'])
    
    style.configure("Subtitle.TLabel",
                   font=FONTS['subtitle'],
                   background=COLORS['bg_secondary'],
                   foreground=COLORS['text_secondary'])
    
    style.configure("Info.TLabel",
                   font=FONTS['small'],
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
                   font=FONTS['heading'],
                   background=COLORS['bg_secondary'],
                   foreground=COLORS['primary'])
    
    style.configure("TEntry",
                   font=FONTS['base'],
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
                   font=FONTS['base'],
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
                   padding=[18, 10],
                   font=FONTS['base'],
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
    
    style.configure("TText",
                   font=FONTS['base'],
                   background=COLORS['bg_primary'],
                   foreground=COLORS['text_primary'],
                   borderwidth=1,
                   relief="solid")


def configure_treeview_tags(treeview):
    """Configure alternating row colors for a treeview"""
    treeview.tag_configure('oddrow', background=COLORS['bg_primary'])
    treeview.tag_configure('evenrow', background=COLORS['bg_secondary'])


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
