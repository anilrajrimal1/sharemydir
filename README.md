<div align="center">
  <h1>ShareMyDir</h1>
  <p>Effortlessly serve any folder over HTTP with zero configuration.</p>
  <p>Mobile-friendly interface, QR code access, and downloadable folders as ZIP files.</p>
</div>

</br>

<!-- prettier-ignore-start -->
<div align="center">

| **PyPI**                                                                                  | **Python Version**                                                                     | **License**                                                                                                     | **GitHub Release**                                                                                                     | **Downloads**                                                                        |
| ----------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------ |
| [![PyPI](https://img.shields.io/pypi/v/sharemydir?color=blue)](https://pypi.org/project/sharemydir/) | [![Python Version](https://img.shields.io/pypi/pyversions/sharemydir)](https://pypi.org/project/sharemydir/) | [![License](https://img.shields.io/github/license/anilrajrimal1/sharemydir?color=green)](https://github.com/anilrajrimal1/sharemydir/blob/main/LICENSE) | [![GitHub Release](https://img.shields.io/github/v/release/anilrajrimal1/sharemydir?color=purple)](https://github.com/anilrajrimal1/sharemydir/releases) | [![Downloads](https://img.shields.io/pypi/dm/sharemydir?color=orange)](https://pypi.org/project/sharemydir/) |

</div>


## Features

- **Instant HTTP Server**: Serve any folder with a single command.
- **Automatic IP Detection**: Works seamlessly on your local network.
- **Mobile-Friendly**: Access via QR code or URL on any device.
- **Download Folders as ZIP**: Easily share entire directories.
- **Individual File Downloads**: Grab single files directly from the browser.
- **Clean Web UI**: Responsive, intuitive interface for all devices.
- **Zero Config CLI**: No setup, just run and share.
- **Elegant Terminal Output**: Clear URLs and QR codes for quick access.

## Demo
![sharemydir-demo](https://github.com/user-attachments/assets/1585ee4b-0d05-48b7-bd55-862650a96ed8)

## Installation

Install `sharemydir` directly from PyPI:

```bash
pip install sharemydir
```

Alternatively, clone the repository for development:

```bash
git clone https://github.com/anilrajrimal1/sharemydir.git
cd sharemydir
```
### Dependencies

- Requires `qrcode` for QR code generation:
  ```bash
  pip install qrcode
  ```

## Usage

Serve the current directory:

```bash
sharemydir
```

Serve a specific folder on a custom port:

```bash
sharemydir /path/to/folder -p 9000
```

### Example Output

```text
+------------------------------------------------------------+
| Serving folder: /home/anil/demo/sharemydir-demo               |
| URL: http://192.168.1.42:9000/                             |
| Scan this QR code for mobile access:                       |
+------------------------------------------------------------+
```

Open the URL in a browser or scan the QR code on your mobile device.

## Web Interface

- **Table View**: Clean, organized display of files and folders.
- **Download Options**: Buttons for downloading files or entire folders as ZIP.
- **Responsive Design**: Optimized for desktops, tablets, and phones.

## CLI Options

| Option         | Description                           | Default       |
|----------------|---------------------------------------|---------------|
| `FOLDER`       | Folder to serve                       | Current (`.`) |
| `-p`, `--port` | Port for the server                   | `8080`        |

## Graceful Shutdown

Stop the server cleanly with `Ctrl+C`.

## Development

To run locally for development:

```bash
python sharemydir.py
```

### Contributing

We welcome contributions! To get started:

1. Fork the repository.
2. Create a feature branch (`git checkout -b feat/name-your-feature`).
3. Commit your changes (`git commit -m 'add amazing feature'`).
4. Push to the branch (`git push origin feat/name-your-feature`).
5. Open a Pull Request.

## Releases

Check out the [Releases](https://github.com/anilrajrimal1/sharemydir/releases) page for the latest updates, changelogs, and version history.

- **Latest Release**: [v1.0.3](https://github.com/anilrajrimal1/sharemydir/releases/latest)
- Available on [PyPI](https://pypi.org/project/sharemydir/).

## License

Distributed under the MIT License. © 2025 Anil Raj Rimal. See [LICENSE](LICENSE) for more information.

## Acknowledgments

- Built with 💖 by [Anil Raj Rimal](https://github.com/anilrajrimal1).
- Powered by Python and open-source libraries.
