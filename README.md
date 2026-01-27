# Installation & Setup Guide

Please follow these steps in the specific order listed to ensure the game runs correctly.

---

## 1. Prerequisites

Install the following tools before setting up the project:

* **Git:** Download and install from [git-scm.com](https://git-scm.com/install/).
* **PyCharm:** Download and install from [jetbrains.com](https://www.jetbrains.com/pycharm/download/?section=windows).
* **Python 3.13:**
    * **Windows:** Download the 64-bit installer from [python.org](https://www.python.org/downloads/windows/). 
    * **CRITICAL:** You must check the box **"Add Python 3.13 to PATH"** before clicking Install Now.
    * **macOS:** Run `brew install python@3.13` (install Homebrew first if needed).
    * **Linux:** Run `sudo add-apt-repository ppa:deadsnakes/ppa -y`, `sudo apt update`, and `sudo apt install python3.13 python3.13-venv python3.13-dev -y`.

---

## 2. Install the `uv` Package Manager

Open your terminal or PowerShell and run the command for your OS:

| OS | Command |
| :--- | :--- |
| **Windows** | `powershell -ExecutionPolicy Bypass -c "irm https://astral.sh/uv/install.ps1 \| iex"` |
| **macOS** | `curl -LsSf https://astral.sh/uv/install.sh \| sh` |
| **Linux** | `curl -LsSf https://astral.sh/uv/install.sh \| sh` |

---

## 3. Project Initialization

1.  **Clone the Repository:** Open PyCharm and select **Clone Repository**.
2.  **Environment Prompt:** If a "Create Virtual Environment" window appears, click **Cancel**.
3.  **Manual Venv Creation:** * Open the **Terminal** within PyCharm.
    * Type: `uv venv --python 3.13`.
    * *Note: If uv cannot find Python, provide the path: `uv venv --python /usr/bin/python3.13`*.

---

## 4. Activation & Dependencies

In the PyCharm Terminal, run the following based on your OS:

### **Windows**
* **Activate:** `.\.venv\Scripts\Activate.ps1` 
* **Install:** `uv pip install -r requirements.txt` 

### **macOS / Linux**
* **Activate:** `source .venv/bin/activate` 
* **Install:** `uv pip install -r requirements.txt` 

> **Note:** Wait for PyCharm to finish indexing all files before proceeding.

---

## 5. Configure Python Interpreter (Recommended)

To avoid errors and enable the Play button, configure the local interpreter:

1.  Open **Settings** and search for **"Python Interpreter"**.
2.  Click **Add Interpreter** -> **Add local interpreter**.
3.  Select **Existing**:
    * **Type:** Python.
    * **Python path:** Select the path to the `python` file inside your project's `.venv` folder (e.g., `...\.venv\Scripts\python`).
4.  Click **Apply** and **OK**.

---

## 6. Running the Game

### **Method A: PyCharm UI**
1.  Open `main.py`.
2.  Next to the green Play button at the top, click the **three dots** and select **Edit Configuration**.
3.  Ensure the **Working directory** path ends at the root of the project. If it includes `/Code`, delete that part from the path.
4.  Click the **green Play button**.

### **Method B: Terminal**
Run the following command in the PyCharm terminal:
`uv run python Code/main.py`
