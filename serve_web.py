"""Serveur HTTP simple pour servir l'interface web."""

import http.server
import socketserver
import os
import webbrowser
from pathlib import Path

PORT = 8000

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    """Handler personnalisé pour servir les fichiers."""
    
    def end_headers(self):
        # Ajouter les headers CORS
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()
    
    def log_message(self, format, *args):
        """Personnaliser les logs."""
        print(f"[{self.log_date_time_string()}] {format % args}")

def main():
    """Lance le serveur HTTP."""
    # Changer vers le répertoire du script
    os.chdir(Path(__file__).parent)
    
    with socketserver.TCPServer(("", PORT), MyHTTPRequestHandler) as httpd:
        url = f"http://localhost:{PORT}/index.html"
        print("=" * 60)
        print("🌐 Serveur web démarré !")
        print("=" * 60)
        print(f"📂 URL: {url}")
        print(f"🔗 Ouvrez cette URL dans votre navigateur")
        print("=" * 60)
        print("⚠️  Appuyez sur Ctrl+C pour arrêter le serveur")
        print("=" * 60)
        print()
        
        # Ouvrir automatiquement dans le navigateur
        try:
            webbrowser.open(url)
            print("✅ Navigateur ouvert automatiquement")
        except Exception:
            print("ℹ️  Ouvrez manuellement:", url)
        
        print()
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n\n🛑 Arrêt du serveur...")
            httpd.shutdown()

if __name__ == "__main__":
    main()

