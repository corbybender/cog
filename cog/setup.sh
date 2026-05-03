#!/bin/bash

# CogOS Quick Setup Script
# This script will set up CogOS and verify everything works

echo "🚀 CogOS Setup Script"
echo "====================="
echo ""

# Step 1: Check prerequisites
echo "📋 Step 1: Checking prerequisites..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed."
    exit 1
fi
echo "✅ Python 3 found: $(python3 --version)"

if ! command -v pip &> /dev/null; then
    echo "❌ pip is required but not installed."
    exit 1
fi
echo "✅ pip found"
echo ""

# Step 2: Install CogOS
echo "📦 Step 2: Installing CogOS..."
pip install -e . -q
if [ $? -eq 0 ]; then
    echo "✅ CogOS installed successfully"
else
    echo "❌ Installation failed"
    exit 1
fi
echo ""

# Step 3: Check if cog.yaml exists
echo "📝 Step 3: Checking configuration..."
if [ ! -f "cog.yaml" ]; then
    echo "⚠️  cog.yaml not found. Creating example..."
    cat > cog.yaml << 'EOF'
# CogOS Configuration
provider: openai
model: gpt-4o
base_url: https://api.openai.com/v1
api_key: YOUR_API_KEY_HERE

# Memory settings
memory_backend: sqlite
memory_path: cog_memory.db

# Module settings
modules_path: modules

# Agent settings
max_agent_iterations: 20
log_level: INFO
EOF
    echo "✅ Example cog.yaml created"
    echo "⚠️  Please edit cog.yaml and add your API key!"
else
    echo "✅ cog.yaml found"
fi
echo ""

# Step 4: Verify installation
echo "🔍 Step 4: Verifying installation..."
cog --help > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "✅ 'cog' command is available"
else
    echo "❌ 'cog' command not found. Try: pip install -e ."
    exit 1
fi
echo ""

# Step 5: Check system status
echo "📊 Step 5: Checking system status..."
cog status > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "✅ CogOS is operational!"
    cog status | grep -E "(Modules|Tools|Verifiers)" | head -3
else
    echo "⚠️  CogOS has issues. Check your configuration."
fi
echo ""

# Step 6: Run tests
echo "🧪 Step 6: Running tests..."
python -m pytest tests/ -q > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "✅ All tests passing"
else
    echo "⚠️  Some tests failing. Run: pytest tests/ -v"
fi
echo ""

echo "🎉 Setup Complete!"
echo "================"
echo ""
echo "Next Steps:"
echo "1. Edit cog.yaml and add your API key"
echo "2. Try: cog run 'Say hello'"
echo "3. Explore: cog --help"
echo "4. Read: SETUP_GUIDE.md"
echo ""
echo "Quick Test:"
echo "  cog run 'List the files in current directory'"
echo ""
