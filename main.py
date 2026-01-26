#!/usr/bin/env python3
"""
Application de Gestion de Contacts Avancée
Point d'entrée principal
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.app import main

if __name__ == "__main__":
    main()
