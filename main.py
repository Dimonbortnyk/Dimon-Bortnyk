#!/usr/bin/env python3
"""
Leadger - Professional Accounting System
=========================================
App de escritorio con ventana nativa (pywebview).

Landing page: https://leadger.net (GitHub Pages)
App backend: Este servidor (localhost:8765)

Instalar dependencias:
    pip install pywebview

Ejecutar:
    python main.py

Compilar a .exe (Windows, sin consola):
    pyinstaller --onefile --noconsole --name=Leadger main.py
"""

import http.server
import socketserver
import threading
import time
import socket
import sys
import json as _json
import pathlib as _pathlib

PORT = 8765


def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        try:
            return socket.gethostbyname(socket.gethostname())
        except Exception:
            return "127.0.0.1"


def get_data_file():
    """Returns path to the persistent data file next to the executable."""
    if getattr(sys, 'frozen', False):
        # Running as compiled .exe
        base = _pathlib.Path(sys.executable).parent
    else:
        # Running as .py script
        base = _pathlib.Path(__file__).parent
    return base / 'leadger_data.json'


# Import the dashboard HTML from finledger_desktop_77.py
from finledger_desktop_77 import HTML


class Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        # Serve static files for auth pages
        if self.path == '/login.html':
            self._serve_file('login.html')
        elif self.path == '/signup.html':
            self._serve_file('signup.html')
        elif self.path == '/app.html':
            self._serve_file('app.html')
        elif self.path == '/config.js':
            self._serve_file('config.js')
        elif self.path == '/load':
            self._load_data()
        else:
            # Serve the main dashboard for everything else
            self._serve_app()

    def do_POST(self):
        if self.path == '/save':
            self._save_data()
        elif self.path == '/export':
            self._export_file()
        else:
            self.send_response(404)
            self.end_headers()

    def _serve_file(self, filename):
        """Serve static HTML/JS files from the same directory."""
        try:
            if getattr(sys, 'frozen', False):
                base = _pathlib.Path(sys.executable).parent
            else:
                base = _pathlib.Path(__file__).parent
            
            file_path = base / filename
            
            if file_path.exists():
                content_type = 'text/html; charset=utf-8'
                if filename.endswith('.js'):
                    content_type = 'application/javascript; charset=utf-8'
                
                self.send_response(200)
                self.send_header('Content-type', content_type)
                self.send_header('Cache-Control', 'no-cache')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(file_path.read_bytes())
            else:
                # File not found, serve dashboard instead
                self._serve_app()
        except Exception as e:
            print(f"Error serving {filename}: {e}")
            self._serve_app()

    def _export_file(self):
        import json as _json2
        import pathlib as _pathlib2
        try:
            length = int(self.headers.get('Content-Length', 0))
            body   = self.rfile.read(length)
            data   = _json2.loads(body)
            fname  = data.get('filename', 'export.csv')
            content= data.get('content', '')

            # Save to Desktop
            desktop = _pathlib2.Path.home() / 'Desktop' / fname
            desktop.write_text(content, encoding='utf-8-sig')

            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(_json2.dumps({'ok': True, 'path': str(desktop)}).encode())
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(_json2.dumps({'ok': False, 'error': str(e)}).encode())

    def _serve_app(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.send_header('Cache-Control', 'no-cache')
        self.end_headers()
        self.wfile.write(HTML.encode('utf-8'))

    def _load_data(self):
        data_file = get_data_file()
        if data_file.exists():
            try:
                data = data_file.read_text(encoding='utf-8')
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(data.encode('utf-8'))
                return
            except Exception:
                pass
        # No data file yet
        self.send_response(204)
        self.end_headers()

    def _save_data(self):
        try:
            length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(length)
            data = _json.loads(body)
            data_file = get_data_file()
            data_file.write_text(
                _json.dumps(data, ensure_ascii=False, indent=2),
                encoding='utf-8'
            )
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b'ok')
        except Exception as e:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(str(e).encode())

    def log_message(self, format, *args):
        pass  # Silencioso


def start_server(port):
    """Arranca el servidor HTTP en un hilo secundario."""
    socketserver.TCPServer.allow_reuse_address = True
    httpd = socketserver.TCPServer(("127.0.0.1", port), Handler)
    thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    thread.start()
    return httpd


def main():
    port = PORT
    url  = f"http://localhost:{port}"

    # Intentar importar pywebview
    try:
        import webview
        HAS_WEBVIEW = True
    except ImportError:
        HAS_WEBVIEW = False

    # Arrancar servidor local
    try:
        server = start_server(port)
    except OSError:
        # Puerto ocupado, probar el siguiente
        port += 1
        url = f"http://localhost:{port}"
        server = start_server(port)

    # Esperar un momento a que el servidor esté listo
    time.sleep(0.8)

    if HAS_WEBVIEW:
        # ── Modo app de escritorio nativa ─────────────────────────────
        window = webview.create_window(
            title      = "Leadger — Accounting System",
            url        = url,
            width      = 1280,
            height     = 820,
            min_size   = (900, 600),
            resizable  = True,
            text_select= True,
        )
        # Al cerrar la ventana, parar el servidor
        def on_closed():
            server.shutdown()
        window.events.closed += on_closed
        webview.start(debug=False)

    else:
        # ── Fallback: abrir en navegador si pywebview no está ─────────
        import webbrowser
        local_ip = get_local_ip()
        print()
        print("╔══════════════════════════════════════════════════════════╗")
        print("║       Leadger — Professional Accounting System           ║")
        print("╚══════════════════════════════════════════════════════════╝")
        print()
        print("  ⚠  pywebview no está instalado.")
        print("  Abriendo en el navegador como alternativa.")
        print()
        print(f"  ▶  This computer:  {url}")
        print(f"  ▶  Other devices:  http://{local_ip}:{port}")
        print()
        print("  💡 Landing page: https://leadger.net")
        print()
        print("  Instala pywebview para la ventana nativa:")
        print("      pip install pywebview")
        print()
        print("  Ctrl+C para salir.")
        print()
        webbrowser.open(url)
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            print()
            print("  Servidor parado. ¡Hasta luego!")
            print()


if __name__ == "__main__":
    main()
