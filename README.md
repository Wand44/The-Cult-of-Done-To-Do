# The Cult of Done To-Do App

A minimalist desktop to-do list inspired by [The Cult of Done Manifesto](https://cultofdone.org/).

Built with Python and tkinter(`customtkinter`).

## Features

- **Add, Complete and Delete tasks**
- **7-day countdown** - each task shows time remaining. Based on the fifth principle. When the week is up, the task shows an abandon message.
- **Rotating principles** - a random Cult of Done principle appears at the bottom of the window, cycling every 60 seconds
- **Storage** - tasks are saved to `tasks.json` and loaded on startup

<img width="300" height="450" alt="image" src="https://github.com/user-attachments/assets/fef6caaf-89c3-44e1-a478-7c41a2eb1d00" />

## The Principles

```text
There are three states of being. Not knowing, action and completion.
Accept that everything is a draft. It helps to get it done.
There is no editing stage.
Done is the engine of more.
...
```

All 13 principles are displayed throughout the app.

## Getting Started

```bash
pip install customtkinter
python main.py
```

On Linux you may also need `python3-tk`:

```bash
sudo apt install python3-tk
```

## Project Structure

| File | Purpose |
|------|---------|
| `main.py` | Application logic and UI |
| `principles.py` | The 14 manifesto principles |
| `settings.py` | Colors, fonts, and constants |
| `countdown.py` | 7-day countdown calculation |
| `tasks.json` | Persistent task storage |
| `empty.ico` | Window icon |
