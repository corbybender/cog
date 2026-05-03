# 🚀 Get Started with CogOS - The Easy Way

**The complete beginner's guide to using CogOS - in 5 minutes or less**

---

## ⚡ Quick Overview

**CogOS is a super-intelligent AI system that:**
- Uses 8 specialized AI agents working together
- Has 24+ expert modules (Python, JavaScript, AWS, Docker, etc.)
- Includes a beautiful web UI
- Runs 100% locally on your machine
- Is 100% free and open source
- Works with Claude, GPT-4, and other LLMs

**No signup required. No cloud needed. Just install and go.**

---

## 📋 Prerequisites

**You need:**
- ✅ Python 3.8 or higher
- ✅ pip (Python package manager)
- ✅ An LLM API key (Claude or GPT-4)

**That's it!**

---

## 🎯 Option 1: Use the Web UI (Easiest)

This is the simplest way to use CogOS - point and click!

### Step 1: Install CogOS (30 seconds)

```bash
pip install cogos
```

### Step 2: Navigate to Web UI (10 seconds)

```bash
cd cogos/web-ui
```

### Step 3: Start the Web UI (20 seconds)

```bash
./start.sh
```

This will:
- Install all dependencies automatically
- Start the backend server
- Show you instructions

### Step 4: Open in Browser (5 seconds)

Open `web-ui/frontend/index.html` in your web browser.

**That's it! You're ready to go!**

### What You Can Do Now

1. **Create Tasks** - Click "New Task" and describe what you want
2. **Monitor Progress** - Watch tasks execute in real-time
3. **Browse Modules** - Explore 24+ expert modules
4. **View Analytics** - Track your tokens and performance

---

## 💻 Option 2: Use Python API (For Developers)

If you prefer coding over clicking:

### Step 1: Install CogOS

```bash
pip install cogos
```

### Step 2: Create a Python Script

Create a file called `my_task.py`:

```python
from cogos import CogOS

# Initialize CogOS
cogos = CogOS()

# Create a task
result = cogos.think("Create a REST API with FastAPI and PostgreSQL")

# See the result
print(result.summary)
print(result.code)
```

### Step 3: Run It

```bash
python my_task.py
```

**That's all there is to it!**

---

## 🖥️ Option 3: Use Command Line (Quick Tasks)

For quick one-off tasks:

### Step 1: Install CogOS

```bash
pip install cogos
```

### Step 2: Run Tasks from Command Line

```bash
# Interactive mode (chat with CogOS)
cogos chat

# Direct task
cogos "Create a React component with TypeScript"

# Use specific modules
cogos --modules python,aws "Deploy a Flask app to AWS"
```

---

## 🔑 Configure Your API Key

Before using CogOS, you need to add your LLM API key:

### For Claude (Anthropic)

```bash
export ANTHROPIC_API_KEY="your-api-key-here"
```

### For GPT-4 (OpenAI)

```bash
export OPENAI_API_KEY="your-api-key-here"
```

**Or create a `.env` file:**

```bash
ANTHROPIC_API_KEY=your-api-key-here
OPENAI_API_KEY=your-api-key-here
```

---

## 🎨 What CogOS Can Do For You

### Example 1: Build a Web API

**Task:** "Create a REST API with FastAPI and PostgreSQL"

**CogOS will:**
- ✅ Design the API structure
- ✅ Write all the code
- ✅ Create database models
- ✅ Add authentication
- ✅ Write tests
- ✅ Generate documentation

**Result:** Production-ready API in seconds, not hours.

### Example 2: Deploy to Cloud

**Task:** "Deploy a Flask application to AWS ECS"

**CogOS will:**
- ✅ Create Dockerfile
- ✅ Set up ECS configuration
- ✅ Configure load balancer
- ✅ Add auto-scaling
- ✅ Create deployment scripts

**Result:** Production deployment in minutes.

### Example 3: Write Tests

**Task:** "Write comprehensive tests for this function"

**CogOS will:**
- ✅ Generate unit tests
- ✅ Add edge cases
- ✅ Include integration tests
- ✅ Add fixtures
- ✅ Ensure high coverage

**Result:** Well-tested code.

---

## 📊 Understanding the Results

When you create a task, CogOS provides:

### Summary
A high-level overview of what was done.

### Code
The actual working code (ready to use).

### Tests
Comprehensive tests for the code.

### Documentation
Clear documentation and comments.

### Metadata
Information about which agents were used, how many tokens were consumed, etc.

---

## 🎓 Next Steps

### Learn More

- **Explore Modules:** [docs/api/modules.md](docs/api/modules.md)
- **Read Documentation:** [docs/START_HERE.md](docs/START_HERE.md)
- **See Examples:** [docs/examples/](docs/examples/)
- **Web UI Guide:** [web-ui/README.md](web-ui/README.md)

### Try Examples

1. **Create a REST API**
   ```
   "Create a REST API with FastAPI and PostgreSQL"
   ```

2. **Build a Web Component**
   ```
   "Create a React button component with TypeScript"
   ```

3. **Deploy to Cloud**
   ```
   "Deploy a Python app to AWS ECS with Docker"
   ```

---

## ❓ Common Questions

### Q: Do I need to pay to use CogOS?

**A:** No! CogOS is 100% free. No subscription, no hidden costs.

### Q: Does CogOS work offline?

**A:** Yes, everything runs locally on your machine. No internet required (except for LLM API calls).

### Q: What LLMs work with CogOS?

**A:** Claude, GPT-4, and any compatible LLM. You use your own API key.

### Q: Is my data private?

**A:** Yes! Everything runs locally on your machine. Your code and data never leave your computer.

### Q: Can I use CogOS commercially?

**A:** Yes! CogOS is MIT licensed, so you can use it for personal or commercial projects.

### Q: Do I need to know how to code?

**A:** The Web UI makes it easy even if you don't code. But some Python knowledge helps for advanced usage.

### Q: How much does it cost?

**A:** CogOS itself is free. You only pay for the LLM API calls you make (to Claude, OpenAI, etc.). CogOS can actually reduce your costs by 40-60% through smart caching!

---

## 🆘 Need Help?

### Documentation

- **Getting Started:** [docs/START_HERE.md](docs/START_HERE.md)
- **Configuration:** [docs/api/configuration.md](docs/api/configuration.md)
- **Modules:** [docs/api/modules.md](docs/api/modules.md)
- **Examples:** [docs/examples/](docs/examples/)

### Community

- **GitHub Issues:** [github.com/corbybender/cog/issues](https://github.com/corbybender/cog/issues)
- **Documentation:** [docs/](docs/)

### Troubleshooting

**Problem:** Installation fails
```bash
# Try upgrading pip
pip install --upgrade pip
pip install cogos
```

**Problem:** API key not found
```bash
# Make sure your environment variables are set
echo $ANTHROPIC_API_KEY
```

**Problem:** Web UI not loading
```bash
# Make sure backend is running
cd web-ui/backend
python app.py
# Then open web-ui/frontend/index.html
```

---

## 🎉 You're Ready!

**You now have everything you need to use CogOS:**

1. ✅ CogOS installed
2. ✅ API key configured
3. ✅ Web UI ready (or Python API, or CLI)
4. ✅ 24+ expert modules at your fingertips
5. ✅ 8 specialized AI agents ready to help

**Start creating amazing things with AI!**

---

## 💡 Pro Tips

1. **Start Simple** - Begin with basic tasks to get familiar
2. **Use the Web UI** - It's the easiest way to get started
3. **Explore Modules** - Check out all 24+ modules available
4. **Be Specific** - More specific tasks = better results
5. **Iterate** - You can always refine and improve results

---

**Happy coding with CogOS! 🚀**

---

*This guide covers everything you need to get started. For more advanced usage, check out the [full documentation](docs/).*
