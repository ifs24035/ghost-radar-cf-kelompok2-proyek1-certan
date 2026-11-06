"""
Ghost Radar - Tactical Paranormal AI Scanner Launcher
Menjalankan Ghost Radar Interaktif di Browser Default Anda.
"""
import webbrowser
import os
import sys

def main():
    file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "index.html"))
    if not os.path.exists(file_path):
        print(f"[ERROR] File index.html tidak ditemukan di {file_path}")
        sys.exit(1)
        
    print("=" * 65)
    print("⚡ GHOST RADAR v2.0 - TACTICAL PARANORMAL AI SCANNER")
    print("=" * 65)
    print(f"[*] Meluncurkan Radar Interaktif di Browser Anda...")
    print(f"[*] Lokasi File: {file_path}")
    print("[*] Fitur Aktif: Web Audio SFX 3D, Radar Sweep 360°, EMF Meter Dinamis")
    print("=" * 65)
    
    webbrowser.open(f"file:///{file_path}")

if __name__ == "__main__":
    main()
