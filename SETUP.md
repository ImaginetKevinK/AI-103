# Running AI-103 in VS Code

## One-time setup

1. **Open the folder** — `File → Open Folder...` → pick `C:\Projects\AI-103`
2. **Install the Python extension** if you haven't (Microsoft's official one)
3. **Select the interpreter** — `Ctrl+Shift+P` → `Python: Select Interpreter` → pick `.\.venv\Scripts\python.exe`. VS Code remembers this per-workspace

After that, any new terminal you open in VS Code auto-activates `.venv`.

## Three ways to run

### 1. Terminal (most flexible — required for picking examples)

Open the integrated terminal via `View → Terminal` (or `Ctrl+Shift+P` → `Toggle Terminal`), then:

```pwsh
python main.py        # interactive menu
python main.py 17     # jump straight to example 17
python main.py 7      # run the interactive chat loop
```

The `.venv` is already active so `python` resolves correctly.

### 2. Run button (top-right of editor)

Open `main.py` and click the **▶ Run Python File** triangle. This runs `python main.py` with no args, so it'll print the menu and wait for input in the terminal panel below.

### 3. Debugger with arguments (`F5`)

For interactive debugging with breakpoints, create `.vscode/launch.json`:

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "AI-103: menu",
      "type": "debugpy",
      "request": "launch",
      "program": "${workspaceFolder}/main.py",
      "console": "integratedTerminal",
      "cwd": "${workspaceFolder}"
    },
    {
      "name": "AI-103: pick example",
      "type": "debugpy",
      "request": "launch",
      "program": "${workspaceFolder}/main.py",
      "args": ["${input:exampleNumber}"],
      "console": "integratedTerminal",
      "cwd": "${workspaceFolder}"
    }
  ],
  "inputs": [
    {
      "id": "exampleNumber",
      "type": "promptString",
      "description": "Example number (1-17) or module name",
      "default": "17"
    }
  ]
}
```

Then `F5` → pick **"AI-103: pick example"** → it prompts you for the number and runs.

`"console": "integratedTerminal"` is important — without it, `input()` calls in the interactive chat-loop examples (7, 16) won't work.
