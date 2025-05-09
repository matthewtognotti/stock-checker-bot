# bot.sh - Bash functions to launch the main bot and handle login for the target website.
# Usage: source this file in your shell, then run `bot` or `login`.

# Ensure SCRIPT_DIR is set (e.g. SCRIPT_DIR="$HOME/path/to/project_directory")
if [ -z "$SCRIPT_DIR" ]; then
  echo "Error: SCRIPT_DIR is not set. Please set it in your .bashrc"
  return 1
fi

# Function: bot
# Description: Activates the virtual environment and runs the main Python bot.
function bot() {
  cd "$SCRIPT_DIR/bash_scripts" || { echo "Directory not found"; return 1; }

  if [ -f "$SCRIPT_DIR/venv/bin/activate" ]; then
    source "$SCRIPT_DIR/venv/bin/activate"
  else
    echo "Virtual environment not found"
    return 1
  fi

  "$SCRIPT_DIR/venv/bin/python" "$SCRIPT_DIR/main.py" || { echo "Failed to run main.py"; return 1; }
}

export -f bot

# Function: login
# Description: Activates the virtual environment and runs the login script.
function login() {
  cd "$SCRIPT_DIR/bash_scripts" || { echo "Directory not found"; return 1; }

  if [ -f "$SCRIPT_DIR/venv/bin/activate" ]; then
    source "$SCRIPT_DIR/venv/bin/activate"
  else
    echo "Virtual environment not found"
    return 1
  fi

  "$SCRIPT_DIR/venv/bin/python" login.py || { echo "Failed to run login.py"; return 1; }
}

export -f login
