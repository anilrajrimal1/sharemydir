# serveme

Instantly serve any folder over HTTP with zero configuration, mobile-friendly access, and downloadable folders.

![demo](https://user-images.githubusercontent.com/placeholder/demo.gif)

## Features

- Serve any folder instantly over HTTP
- Automatically detects local IP address
- Prints QR code in terminal for mobile access
- Download entire folders as ZIP files
- Download individual files via browser
- Zero configuration CLI tool
- Clean web UI and terminal output

## Installation

Install the required package:

```bash
pip install qrcode-terminal
```

Clone this repository:

```bash
git clone https://github.com/anilrajrimal1/serveme.git
cd serveme
```

Or install directly from PyPI:

```bash
pip install serveme
```

## Usage

From the root of the directory you want to serve:

```bash
serveme
```

Or specify a folder and a port:

```bash
serveme /path/to/folder -p 9000
```

### Output:

```text
+------------------------------------------------------------+
| Serving folder: /home/anil/demo/serveme-demo               |
| URL: http://192.168.1.42:9000/                             |
| Scan this QR code for mobile access:                       |
+------------------------------------------------------------+
```

Then open the URL in any browser or scan the QR code.

## Web UI

- Clean table view of files/folders
- Download buttons for each file and folder
- Mobile responsive layout

## CLI Options

| Option         | Description                         |
|----------------|-------------------------------------|
| `FOLDER`       | Folder to serve (default is `.`)    |
| `-p`, `--port` | Port to use (default is `8080`)     |

## Graceful Shutdown

Press `Ctrl+C` to stop the server cleanly.

## Development

To run locally:

```bash
python serveme.py
```

## License

MIT License. ©️ 2025 Anil Raj Rimal
