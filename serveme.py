#!/usr/bin/env python3

import argparse
import http.server
import socket
import socketserver
import os
import urllib
import qrcode_terminal

def get_local_ip():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))
            return s.getsockname()[0]
    except Exception:
        return "127.0.0.1"

class DownloadableHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # If serving a file, add headers to force download
        if self.path and not self.path.endswith('/'):
            # Only add header if file exists
            file_path = self.translate_path(self.path)
            if os.path.isfile(file_path):
                self.send_header("Content-Disposition", "attachment; filename=%s" % os.path.basename(file_path))
        super().end_headers()

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
    parser = argparse.ArgumentParser(description="Serve a folder over HTTP with forced file downloads.")
    parser.add_argument("folder", nargs="?", default=".", help="Folder to serve (default current directory)")
    parser.add_argument("-p", "--port", type=int, default=8080, help="Port number to serve on (default 8080)")

    args = parser.parse_args()
    serve(args.folder, args.port)

if __name__ == "__main__":
    main()
