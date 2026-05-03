#!/bin/bash

# CogOS Web UI Launcher

echo "🚀 Starting CogOS Web UI..."
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed."
    exit 1
fi

# Get script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
BACKEND_DIR="$SCRIPT_DIR/backend"

# Install backend dependencies
echo "📦 Installing backend dependencies..."
cd "$BACKEND_DIR"
pip install -q -r requirements.txt

if [ $? -ne 0 ]; then
    echo "❌ Failed to install dependencies"
    exit 1
fi

echo "✅ Dependencies installed"
echo ""

# Start backend server
echo "🔧 Starting backend server on http://localhost:8000"
echo "📱 Open web-ui/frontend/index.html in your browser"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Start server
python3 app.py
