# 🚀 Getting Started with CogOS

Welcome to CogOS! This guide will get you up and running with super-intelligent AI in 5 minutes.

**Important:** CogOS is 100% FREE and runs locally on your machine. No signup, no account, no cloud required.

## What You'll Learn

- ✅ How to install CogOS (one command)
- ✅ **Option 1: Use the Web UI (easiest)**
- ✅ Option 2: Use Python API (for developers)
- ✅ Option 3: Use Command Line (quick tasks)
- ✅ How to configure your API key
- ✅ Common workflows

---

## ⚡ Quick Install (One Command)

```bash
pip install cogos && cd /path/to/project && python install_cogos.py
```

That's it! CogOS is now integrated into your project.

---

## 📋 Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- An LLM API key (Claude, GPT-4, or compatible)

**That's all you need!**

---

## 🎨 Option 1: Use the Web UI (EASIEST)

This is the simplest way to use CogOS - no coding required!

### Step 1: Navigate to Web UI

```bash
cd cogos/web-ui
```

### Step 2: Start the Web UI

```bash
./start.sh
```

This will:
- Install all dependencies automatically
- Start the backend server
- Show you instructions

### Step 3: Open in Browser

Open `web-ui/frontend/index.html` in your web browser.

**That's it! You can now:**
- Create tasks by clicking
- Monitor progress in real-time
- Browse all 40+ modules
- View performance analytics

**Full Web UI Guide:** [web-ui/README.md](../web-ui/README.md)

---

## 💻 Option 2: Use Python API (For Developers)

If you prefer coding over clicking:

### Configure Your LLM First

```bash
# Set your API key as environment variable
export ANTHROPIC_API_KEY="your-api-key"  # For Claude
export OPENAI_API_KEY="your-api-key"     # For GPT-4
```

Or create a `.env` file:
```bash
ANTHROPIC_API_KEY=your-api-key
OPENAI_API_KEY=your-api-key
```

### Basic Usage

```python
from cogos import CogOS

# Initialize CogOS
cogos = CogOS()

# Create a task
result = cogos.think("Build a REST API with FastAPI and PostgreSQL")

# See the result
print(result.summary)
print(result.code)
```

---

## 🖥️ Option 3: Use Command Line (Quick Tasks)

```bash
cogos --version
```

You should see: `CogOS v1.0.0`

---

## 🎯 Your First Task

### Interactive Mode (Easiest)

```bash
cogos chat
```

Then type:
```
Create a Python function that fetches data from an API and caches the results in Redis
```

CogOS will:
1. Research best practices
2. Write production code
3. Add comprehensive tests
4. Document everything
5. Optimize performance

### Programmatic Usage

```python
from cogos import CogOS

# Initialize CogOS
cogos = CogOS(llm="claude-3.5-sonnet")

# Execute a task
result = cogos.think("Build a REST API with FastAPI and PostgreSQL")

# Access the result
print(result.summary)      # High-level summary
print(result.code)         # Generated code
print(result.tests)        # Test suite
print(result.docs)         # Documentation
```

### Command Line

```bash
# Direct task
cogos "Create a React component with TypeScript"

# Use specific modules
cogos --modules python,aws "Deploy a Flask app to AWS"

# Save output to file
cogos "Build a microservice" > output.md
```

---

## 🧩 Using Expert Modules

CogOS has 40+ expert modules for different technologies:

### Auto-Detection (Default)

CogOS automatically detects which modules to use:

```python
# This will use the Python, PostgreSQL, and Redis modules
cogos.think("Build a FastAPI app with PostgreSQL and Redis caching")
```

### Manual Selection

```python
# Specify which modules to use
cogos.think(
    "Create a web application",
    modules=["javascript", "react", "mongodb"]
)
```

### Available Modules

**Web**: CSS, HTML
**Languages**: JavaScript, Python, Java, C#, Ruby, PHP, Rust
**Backend**: Node.js, Express, Fastify, NestJS
**Databases**: MySQL, PostgreSQL, MongoDB, Redis, Elasticsearch
**OS**: Windows, Mac, Linux
**Cloud**: AWS, Azure, GCP
**Containers**: Docker, Kubernetes
**Tools**: Git

---

## 📚 Common Workflows

### 1. Build a Complete Feature

```python
result = cogos.think("""
Create a user authentication system with:
- REST API (FastAPI)
- PostgreSQL database
- JWT tokens
- Password hashing
- Unit tests
- Docker deployment
""")
```

**Result**: Production-ready code with tests, docs, and deployment config.

### 2. Debug and Fix Code

```python
result = cogos.think("""
This code is throwing a 500 error. Find and fix the bug:
[paste your code here]
""")
```

**Result**: Detailed analysis of the bug and fixed code.

### 3. Refactor Code

```python
result = cogos.think("""
Refactor this code for better performance:
[paste your code here]
""")
```

**Result**: Optimized code with explanation of improvements.

### 4. Write Tests

```python
result = cogos.think("""
Write comprehensive tests for this function:
[paste your function here]
""")
```

**Result**: Full test suite with edge cases and error handling.

### 5. Generate Documentation

```python
result = cogos.think("""
Generate documentation for this API:
[paste your API code here]
""")
```

**Result**: Complete documentation with examples and usage.

---

## 🎨 What CogOS Actually Does

When you give CogOS a task, it deploys 10 specialized AI agents:

1. **🔬 Research Agent** - Researches best practices and patterns
2. **💻 Code Agent** - Writes production code
3. **🧪 Test Agent** - Creates comprehensive tests
4. **📝 Document Agent** - Writes clear documentation
5. **🎨 Architect Agent** - Designs system architecture
6. **🔍 Critique Agent** - Reviews and identifies issues
7. **✅ Validate Agent** - Verifies requirements are met
8. **⚡ Optimize Agent** - Optimizes performance and costs

These agents **collaborate, debate, and vote** to produce superior results.

---

## 💡 Pro Tips

### 1. Be Specific

❌ Bad: "Make a website"
✅ Good: "Create a React website with TypeScript, Tailwind CSS, and authentication"

### 2. Provide Context

❌ Bad: "Fix this bug"
✅ Good: "This Flask route returns a 500 error when the database is empty. Fix it."

### 3. Use Modules

```python
# Tell CogOS which technologies to use
cogos.think("Build a microservice", modules=["python", "aws", "kubernetes"])
```

### 4. Iterate

```python
# Start with a basic version, then refine
result1 = cogos.think("Create a REST API")
result2 = cogos.think("Add caching to the previous API", context=result1)
```

### 5. Review and Tweak

CogOS provides explanations for all decisions. Review them and ask for changes if needed.

---

## 🎯 Next Steps

### Learn More

- 📖 [Read the Architecture](architecture/README_SUPER_INTELLIGENCE.md)
- 🧩 [Explore Modules](architecture/modules.md)
- 🔧 [API Reference](api/python.md)
- 💡 [Examples](examples/)

### Advanced Usage

- [Creating Custom Modules](guides/custom_modules.md)
- [Performance Optimization](guides/performance.md)
- [Production Deployment](guides/deployment.md)

### Get Involved

- ⭐ [Star on GitHub](https://github.com/corbybender/cog)
- 🐛 [Report Issues](https://github.com/corbybender/cog/issues)
- 🤝 [Contribute](../CONTRIBUTING.md)

---

## 🆘 Troubleshooting

### Installation Issues

**Problem**: `pip install cogos` fails
```bash
# Try upgrading pip
pip install --upgrade pip
pip install cogos
```

### API Key Issues

**Problem**: "API key not found"
```bash
# Make sure your environment variables are set
echo $ANTHROPIC_API_KEY  # Should show your key
```

### Module Not Found

**Problem**: "Module not available"
```bash
# List all available modules
cogos modules

# Update to latest version
pip install --upgrade cogos
```

### Performance Issues

**Problem**: Responses are slow
```bash
# Enable caching (enabled by default)
cogos.config.cache_enabled = True

# Use faster model
cogos = CogOS(llm="claude-3-haiku")  # Faster but less capable
```

---

## 📞 Need Help?

- **Documentation**: [docs/](.)
- **GitHub Issues**: [github.com/corbybender/cog/issues](https://github.com/corbybender/cog/issues)
- **Examples**: [docs/examples/](examples/)

---

## 🎉 You're Ready!

You now have CogOS installed and ready to go. Try it out:

```bash
cogos chat
```

Or in Python:

```python
from cogos import CogOS
cogos = CogOS()
result = cogos.think("Your task here")
print(result.summary)
```

**Happy coding! 🚀**

---

**Next**: [Learn about the Multi-Agent System](architecture/multi_agent.md)
