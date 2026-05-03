# 🚀 CogOS Setup - Step-by-Step Tutorial

## Follow These Exact Steps

### Step 1: Navigate to the CogOS Directory
```bash
cd /home/corbybender/Projects/cog
```

### Step 2: Install CogOS
```bash
pip install -e .
```

**Expected Output:**
```
Successfully installed cogos-0.1.0
```

### Step 3: Verify Installation
```bash
cog --help
```

**Expected Output:**
```
usage: cog [-h] [--modules MODULES] [--memory MEMORY] [--provider PROVIDER]
           [--model MODEL] [--memory-backend MEMORY_BACKEND]
           {init,run,chat,memory,status,modules,install,search,publish,verify} ...
```

### Step 4: Check System Status
```bash
cog status
```

**Expected Output:**
```
CogOS Status
  Modules: 8 active / 8 discovered
  Tools: filesystem.read, filesystem.write, filesystem.list, filesystem.search, shell.execute, web.fetch, web.search, aws.s3.list, aws.s3.upload, aws.s3.download, aws.ec2.list, aws.ec2.start, aws.ec2.stop, aws.lambda.invoke, python.lint, python.test, cargo.build, cargo.test, cargo.check, rust.clippy, rust.fmt, postgres.query, postgres.dump, postgres.restore, postgres.schema, git.status, git.log, git.diff, git.branch, tool.dry_run
  Verifiers: shell.dry_run, file.exists, test.runner, aws.connectivity, python.syntax, rust.syntax, postgres.connectivity
```

### Step 5: Test Basic Functionality
```bash
cog run "List the files in the current directory"
```

**Expected Output:**
```
Result: SUCCESS
Tokens: XXX | Iterations: X | Cost: $X.XX

Here are the files and directories in the current directory (.)
[List of files...]
```

---

## 🔧 Configuration (Optional but Recommended)

### Create/Edit Configuration File
```bash
# Create config if it doesn't exist
cog init --output cog.yaml

# Edit the config file
nano cog.yaml
```

### Basic Configuration
```yaml
# cog.yaml
provider: openai
model: gpt-4o
base_url: https://api.openai.com/v1
api_key: YOUR_OPENAI_API_KEY_HERE

memory_backend: sqlite
memory_path: cog_memory.db
modules_path: modules
max_agent_iterations: 20
```

### Save and Test
```bash
# Test your configuration
cog run "Say hello and tell me what you can do"
```

---

## 🎯 Basic Usage Examples

### Example 1: File Operations
```bash
# Read a file
cog run "Read cog/agent.py and summarize what it does"

# List Python files
cog run "Find all Python files in the cog directory"

# Search for specific code
cog run "Search for 'class Agent' in all Python files"
```

### Example 2: Code Analysis
```bash
# Analyze code quality
cog run "Analyze cog/tools/filesystem.py for improvements"

# Find bugs
cog run "Look for potential bugs in cog/agent.py"

# Explain code
cog run "Explain how the caching system works in cog/cache.py"
```

### Example 3: Development Tasks
```bash
# Run tests
cog run "Run pytest and report any failures"

# Fix linting issues
cog run "Run ruff on all Python files and fix issues"

# Git operations
cog run "Show git status and recent commits"
```

---

## 💬 Interactive Chat Mode

### Start Chat Mode
```bash
cog chat
```

### Example Conversation
```
you> What files are in the cog directory?
cog> [Lists and describes files]

you> Read the agent.py file and tell me how it works
cog> [Explains the agent system]

you> Can you identify any improvements?
cog> [Analyzes and suggests improvements]

you> exit
```

---

## 🧠 Memory System

### Add Memories
```bash
cog memory add --content "The agent uses caching to improve performance" --tags "performance,cache"
```

### Search Memory
```bash
cog memory search "performance"
```

### List All Memories
```bash
cog memory list
```

---

## 🛠️ Module System

### List Available Modules
```bash
cog modules
```

### Search for Modules
```bash
cog search "python"
cog search "rust"
cog search "aws"
```

### Install New Modules
```bash
cog install cog-code-python
```

---

## 🧪 Testing and Verification

### Run Tests
```bash
# Run all tests
python -m pytest tests/ -v

# Run specific test
python -m pytest tests/test_agent.py -v
```

### Verify Code
```bash
# Check Python syntax
cog verify python.syntax cog/agent.py

# Verify file exists
cog verify file.exists cog.yaml

# Run test suite
cog verify test.runner "pytest tests/"
```

---

## 🎨 Advanced Usage

### Dry Run (Preview Mode)
```bash
cog run "Refactor all Python files" --dry-run
```

### JSON Output (For Automation)
```bash
cog run "Analyze codebase" --json
```

### Specify Working Directory
```bash
cog run "Test this project" --path /path/to/other/project
```

### Disable Streaming
```bash
cog run "Long running task" --no-stream
```

---

## 🔍 Troubleshooting

### Problem: Command Not Found
```bash
# Solution: Reinstall
pip install -e .
```

### Problem: API Key Error
```bash
# Solution: Check your cog.yaml file
cat cog.yaml

# Make sure api_key is set correctly
```

### Problem: Modules Not Loading
```bash
# Solution: Check modules directory
ls modules/

# Should see: code-core, language-core, tool-core, etc.
```

### Problem: Tests Failing
```bash
# Solution: Clear cache and reinstall
rm -rf .pytest_cache __pycache__
pip install -e . --force-reinstall
```

---

## 📚 Next Steps

1. **Explore More Commands**: Run `cog --help`
2. **Read Full Guide**: Open `SETUP_GUIDE.md`
3. **Quick Reference**: Check `QUICK_REFERENCE.md`
4. **Try Examples**: Use the examples in this guide

---

## 🎉 You're Ready!

**System Status:**
- ✅ 8 modules active
- ✅ 33 tools available
- ✅ 7 verifiers ready
- ✅ 100% test coverage

**Start Simple:**
```bash
cog run "List all Python files in the current directory"
```

**Then Try:**
```bash
cog run "Analyze the codebase and suggest one improvement"
```

**Have Fun Exploring!** 🚀

---

**Need Help?**
- Run: `cog --help`
- Check: `SETUP_GUIDE.md`
- Reference: `QUICK_REFERENCE.md`
