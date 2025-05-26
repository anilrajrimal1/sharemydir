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
import datetime

# Terminal colors (simple ANSI codes)
class TermColors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

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
        """Override directory listing to present a prettier HTML table with info."""
        try:
            entries = os.listdir(path)
        except OSError:
            self.send_error(404, "No permission to list directory")
            return None

        entries.sort(key=lambda a: a.lower())
        displaypath = urllib.parse.unquote(self.path)

        # HTML + CSS
        r = []
        r.append(f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Directory listing for {displaypath}</title>
<style>
  body {{ font-family: Arial, sans-serif; background: #f9f9f9; color: #333; padding: 20px; }}
  h2 {{ color: #444; }}
  table {{ border-collapse: collapse; width: 100%; max-width: 900px; }}
  th, td {{ text-align: left; padding: 8px; border-bottom: 1px solid #ddd; }}
  tr:hover {{ background-color: #f1f1f1; }}
  th {{ background-color: #4CAF50; color: white; }}
  a {{ color: #007bff; text-decoration: none; }}
  a:hover {{ text-decoration: underline; }}
  .icon {{ font-weight: bold; margin-right: 5px; }}
  .folder {{ color: #ffa500; }}
  .file {{ color: #555; }}
  .download-btn {{
    background-color: #28a745;
    color: white;
    padding: 4px 8px;
    text-decoration: none;
    border-radius: 4px;
    font-size: 0.9em;
  }}
  .download-btn:hover {{
    background-color: #218838;
  }}
</style>
</head>
<body>
<h2>Directory listing for {displaypath}</h2>
<table>
  <thead>
    <tr>
      <th>Name</th>
      <th>Size</th>
      <th>Last Modified</th>
      <th>Actions</th>
    </tr>
  </thead>
  <tbody>''')

        # Parent directory link
        if displaypath != "/":
            parent = os.path.dirname(displaypath.rstrip('/'))
            if not parent.endswith('/'):
                parent += '/'
            r.append(f'<tr><td colspan="4"><a href="{parent}">⬆️ Parent Directory</a></td></tr>')

        for name in entries:
            fullname = os.path.join(path, name)
            display_name = urllib.parse.quote(name)
            stat = os.stat(fullname)
            mod_time = datetime.datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M:%S')

            if os.path.isdir(fullname):
                size_display = "-"
                icon = '<span class="icon folder">📁</span>'
                # Download zip link for folder
                zip_link = urllib.parse.quote(name) + "/?zip=1"
                r.append(f'<tr>'
                         f'<td>{icon}<a href="{display_name}/">{name}/</a></td>'
                         f'<td>{size_display}</td>'
                         f'<td>{mod_time}</td>'
                         f'<td><a href="{zip_link}" class="download-btn">Download ZIP</a></td>'
                         f'</tr>')
            else:
                size_display = sizeof_fmt(stat.st_size)
                icon = '<span class="icon file">📄</span>'
                r.append(f'<tr>'
                         f'<td>{icon}<a href="{display_name}">{name}</a></td>'
                         f'<td>{size_display}</td>'
                         f'<td>{mod_time}</td>'
                         f'<td></td>'
                         f'</tr>')

        r.append('''
  </tbody>
</table>
<hr>
<footer style="font-size: 0.9em; color: #666;">serveme &copy; 2025</footer>
</body>
</html>''')

        encoded = '\n'.join(r).encode('utf-8', 'surrogateescape')
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        return io.BytesIO(encoded)

def sizeof_fmt(num, suffix="B"):
    # human-readable file size
    for unit in ["","K","M","G","T","P","E","Z"]:
        if abs(num) < 1024.0:
            return f"{num:3.1f} {unit}{suffix}"
        num /= 1024.0
    return f"{num:.1f} Y{suffix}"

class ReusableTCPServer(socketserver.TCPServer):
    allow_reuse_address = True

def serve(directory, port):
    os.chdir(directory)
    handler = DownloadableHTTPRequestHandler

    # CLI UI output with color & box
    local_ip = get_local_ip()
    url = f"http://{local_ip}:{port}/"
    folder_path = os.path.abspath(directory)

    # Pretty CLI display
    print(TermColors.OKGREEN + "┌" + "─" * 50 + "┐" + TermColors.ENDC)
    print(TermColors.OKGREEN + f"│ Serving folder: {TermColors.BOLD}{folder_path}".ljust(50) + " │" + TermColors.ENDC)
    print(TermColors.OKGREEN + f"│ URL: {TermColors.UNDERLINE}{url}".ljust(50) + " │" + TermColors.ENDC)
    print(TermColors.OKGREEN + f"│ Scan this QR code for mobile access:".ljust(50) + " │" + TermColors.ENDC)
    print(TermColors.OKGREEN + "└" + "─" * 50 + "┘" + TermColors.ENDC)
    qrcode_terminal.draw(url)

    with ReusableTCPServer(("", port), handler) as httpd:
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
