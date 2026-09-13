# Automation

A collection of Windows desktop utilities that automate repetitive copy-paste and keyboard workflows between **Microsoft Excel** and any other application — web portals, forms, ERP systems, you name it.

Both tools are **general-purpose**: they are not tied to any specific website or form. If a task involves transferring rows of data from a spreadsheet into fields on the screen, or replaying a sequence of keystrokes, these tools handle it.

## Demo

Real-world use case: filling a purchase notice (*avis d'achat*) on the Moroccan public procurement portal **marchespublics.gov.ma** — 27 article lines transferred from Excel into the portal's article form, semi-automatically:

<video src="demo/demo.mp4" controls width="100%"></video>

([Download the demo video](demo/demo.mp4))

> In the demo, **LineByLinePaster** pastes each Excel row into the portal's *Ajouter un article* dialog (Numéro, Désignation, Caractéristiques, Unité de mesure, Quantité, TVA), while **Command Executor** replays the Alt+Tab / Tab / Enter keystrokes needed to navigate between windows and confirm each article.

## Tools

### 1. LineByLinePaster — `LineByLinePaster/LineByLinePaster.py`

Pastes an Excel selection into any application **one line at a time**, field by field.

- **Reads the current Excel selection directly** via the Excel COM API (`win32com`) — no manual copying needed
- For each row: pastes cell → `Tab` → next cell … → `Enter` to confirm the line
- Live preview of the current line and a progress counter (`Ready to paste line 3/27`)
- **Confirmation dialog before every line** — you stay in control of where data lands, safe against mis-clicks
- `Previous Line` to step back, `Stop` to abort at any moment
- Always-on-top window so the controls stay reachable

### 2. Command Executor (Switch3) — `Switch/Switch3.py`

A keyboard macro player with a neon UI. Records a sequence of keystrokes and replays it with per-command timing and repetition.

- Predefined commands: `Space`, `Enter`, `Ctrl+C`, `Ctrl+V`, `Tab`, `Alt+Tab`, `Alt+Tab+Tab`, `Alt+Tab+Tab+Tab` — plus fully custom hotkeys
- Configurable **duration** for every command and a global **repetition count**
- Reorder commands (Move Up / Down), save/load sequences (**Export / Import**)
- Compact **floating widget** for start/stop without leaving your target window
- Sound feedback on actions

## Typical workflow (the demo scenario)

1. Select the data block in Excel.
2. Start **LineByLinePaster** → it loads the selection and shows line 1.
3. Click into the first target field in your application, confirm the dialog — the row is pasted field by field and confirmed with `Enter`.
4. Repeat for each line (or let **Command Executor** replay the window-switching / confirming keystrokes automatically).
5. Stop anytime.

## Requirements

| Tool | Dependencies |
|---|---|
| LineByLinePaster | Python 3, `pyperclip`, `pyautogui`, `pywin32`, Microsoft Excel (Windows) |
| Command Executor | Python 3, `keyboard`, `pygame` |

```bash
pip install pyperclip pyautogui pywin32 keyboard pygame
```

## Build the executable

`Switch/Switch3.exe` is a ready-to-run Windows build. To rebuild it from source (requires [PyInstaller](https://pyinstaller.org/)):

```bash
cd Switch
pyinstaller Switch3.spec
```

## Notes

- Both tools simulate real keyboard input — they work with any app that accepts typing, no browser extension or API needed.
- Works on Windows only (Excel COM integration + global hotkeys).
