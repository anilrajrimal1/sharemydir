#!/usr/bin/env python3

import argparse
import http.server
import socket
import socketserver
import os
import io
import urllib.parse
import zipfile
import qrcode_terminal
from datetime import datetime

def get_local_ip():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))
            return s.getsockname()[0]
    except Exception:
        return "127.0.0.1"

class DownloadableHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urllib.parse.urlparse(self.path)
        query = urllib.parse.parse_qs(parsed_path.query)
        path = parsed_path.path

        fs_path = self.translate_path(path)

        # If folder requested with ?zip=1, serve zipped folder
        if os.path.isdir(fs_path) and query.get("zip", ["0"])[0] == "1":
            try:
                zip_data = self.create_zip_in_memory(fs_path)
            except Exception as e:
                self.send_error(500, f"Error creating ZIP: {e}")
                return

            zip_filename = os.path.basename(os.path.normpath(fs_path)) or "archive"
            zip_filename += ".zip"

            self.send_response(200)
            self.send_header("Content-Type", "application/zip")
            self.send_header("Content-Disposition", f'attachment; filename="{zip_filename}"')
            self.send_header("Content-Length", str(len(zip_data)))
            self.end_headers()
            self.wfile.write(zip_data)
            return

        # Otherwise default handler for files and folders
        super().do_GET()

    def create_zip_in_memory(self, folder_path):
        """Create a ZIP archive of the folder in memory and return bytes."""
        mem_zip = io.BytesIO()
        with zipfile.ZipFile(mem_zip, mode="w", compression=zipfile.ZIP_DEFLATED) as zf:
            for root, dirs, files in os.walk(folder_path):
                for file in files:
                    abs_filename = os.path.join(root, file)
                    rel_path = os.path.relpath(abs_filename, start=folder_path)
                    zf.write(abs_filename, arcname=rel_path)
        mem_zip.seek(0)
        return mem_zip.read()

    def list_directory(self, path):
        """Override directory listing to add [Download ZIP] links."""
        try:
            list = os.listdir(path)
        except OSError:
            self.send_error(404, "No permission to list directory")
            return None

        list.sort(key=lambda a: a.lower())
        r = []
        displaypath = urllib.parse.unquote(self.path)
        r.append(f'<!DOCTYPE html>\n<html>\n<head>\n<title>Directory listing for {displaypath}</title>\n')
        r.append('<meta charset="utf-8">')
        r.append('</head>\n<body>\n')
        r.append(f'<h2>Directory listing for {displaypath}</h2>\n')
        r.append('<hr>\n<ul>\n')

        # Parent directory link
        if displaypath != "/":
            parent = os.path.dirname(displaypath.rstrip('/'))
            if not parent.endswith('/'):
                parent += '/'
            r.append(f'<li><a href="{parent}">.. (parent directory)</a></li>\n')

        for name in list:
            fullname = os.path.join(path, name)
            display_name = link_name = name
            if os.path.isdir(fullname):
                display_name = name + "/"
                link_name = name + "/"
                # Add download zip link next to folder
                zip_link = urllib.parse.quote(link_name) + "?zip=1"
                r.append(f'<li><a href="{link_name}">{display_name}</a> '
                         f'- <a href="{zip_link}">[Download ZIP]</a></li>\n')
            else:
                r.append(f'<li><a href="{urllib.parse.quote(link_name)}">{display_name}</a></li>\n')

        r.append('</ul>\n<hr>\n</body>\n</html>\n')
        encoded = '\n'.join(r).encode('utf-8', 'surrogateescape')
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        return io.BytesIO(encoded)

class ReusableTCPServer(socketserver.TCPServer):
    allow_reuse_address = True

def serve(directory, port):
    os.chdir(directory)
    handler = DownloadableHTTPRequestHandler
    with ReusableTCPServer(("", port), handler) as httpd:
        local_ip = get_local_ip()
        url = f"http://{local_ip}:{port}/"

        print(f"Serving {os.path.abspath(directory)} at:")
        print(f"  {url}\n")
        print("Scan this QR code to open on your mobile device:\n")
        qrcode_terminal.draw(url)

        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down server...")
            httpd.shutdown()

def main():
    parser = argparse.ArgumentParser(description="Serve a folder over HTTP with downloadable folders as ZIPs.")
    parser.add_argument("folder", nargs="?", default=".", help="Folder to serve (default current directory)")
    parser.add_argument("-p", "--port", type=int, default=8080, help="Port number to serve on (default 8080)")

    args = parser.parse_args()
    serve(args.folder, args.port)

if __name__ == "__main__":
    main()
