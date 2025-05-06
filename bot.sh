function bot() {
  # Navigate to the directory containing the project
  cd ~/Desktop/Programming\ Projects\ 2025/python_web_bot/bash_scripts  || { echo "Directory not found"; return 1; }

  # Activate the virtual environment
  if [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
  else
    echo "Virtual environment not found"
    return 1
  fi

  # Run the Python script
  venv/bin/python || { echo "Failed to run main.py"; return 1; }
}

export -f bot

function login() {
  # Navigate to the directory containing the project
  cd ~/Desktop/Programming\ Projects\ 2025/python_web_bot/bash_scripts  || { echo "Directory not found"; return 1; }

  # Activate the virtual environment
  if [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
  else
    echo "Virtual environment not found"
    return 1
  fi

  # Run the Python script
  venv/bin/python login.py || { echo "Failed to run login.py"; return 1; }
}

export -f login