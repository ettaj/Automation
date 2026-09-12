# Automation

Small automation utilities.

## Projects

### LineByLinePaster
Pastes text line by line, one at a time. See [LineByLinePaster/LineByLinePaster.py](LineByLinePaster/LineByLinePaster.py).

### Switch
Desktop utility (`Switch3.py`) packaged with PyInstaller.
- `Switch3.exe` — ready-to-run Windows executable
- `Switch3.py` — source code
- `Switch3.spec` — PyInstaller spec
- `Portail.json` — configuration

## Build

Rebuilding the executable from source (requires [PyInstaller](https://pyinstaller.org/)):

```
pyinstaller Switch3.spec
```
