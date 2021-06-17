"""
Kontrolliert ob die nötigen Packages installiert sind
Wenn nicht, wird über subprocess.Popen installiert.
"""
import sys
import os
import subprocess


# Liste Element = Package / alle Packages die es zur Ausführung braucht.
packages = ["pywin32", "tkcalendar", "Pillow", "Babel", "importlib", "urllib3"]


# Forschleife um alle Elemente durch zu gehen.
for package in packages:

    try:
        __import__(package)
        print("okey")
    except ImportError:
        print("notOkey")
        subprocess.Popen("pip install "+ package)
        print("now_all_Okey")


