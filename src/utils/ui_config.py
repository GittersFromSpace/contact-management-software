"""Configuration globale de l'interface utilisateur"""
from tkinter import ttk
import tkinter.font as tkfont


def configure_styles(root):
    """Configure les styles globaux de l'application"""
    style = ttk.Style(root)
    
    # Définir le thème de base
    try:
        style.theme_use('clam')  # Thème moderne
    except:
        pass
    
    # Configuration du Treeview pour éviter le texte coupé
    # Calculer la hauteur de ligne appropriée
    default_font = tkfont.nametofont("TkDefaultFont")
    font_height = default_font.metrics("linespace")
    rowheight = font_height + 8  # Ajouter de l'espace pour le padding
    
    style.configure("Treeview", 
                   rowheight=rowheight,
                   font=("", 10))
    
    style.configure("Treeview.Heading",
                   font=("", 10, "bold"),
                   padding=5)
    
    # Style pour les boutons
    style.configure("TButton",
                   padding=6,
                   font=("", 10))
    
    style.configure("Accent.TButton",
                   padding=8,
                   font=("", 10, "bold"))
    
    # Style pour les labels
    style.configure("TLabel",
                   font=("", 10))
    
    style.configure("Title.TLabel",
                   font=("", 14, "bold"))
    
    # Style pour les frames
    style.configure("TFrame",
                   background="#f0f0f0")
    
    # Style pour le notebook (tabs)
    style.configure("TNotebook",
                   padding=5)
    
    style.configure("TNotebook.Tab",
                   padding=[15, 8],
                   font=("", 10))


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
