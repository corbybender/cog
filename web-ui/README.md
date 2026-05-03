# CogOS Web UI

**Modern web interface for CogOS - 100% FREE and runs locally on your machine**

## ✨ Features

✅ **Web UI Dashboard** - Beautiful, modern React interface
✅ **Real-time Updates** - Watch tasks progress live
✅ **Task Management** - Create, monitor, and manage tasks
✅ **Module Browser** - Browse and select from 24+ expert modules
✅ **Performance Analytics** - Track tokens, tasks, and performance metrics
✅ **100% Local** - Everything runs on YOUR machine
✅ **100% Free** - No account, no signup, no costs
✅ **No Cloud Required** - Works offline, no internet needed

## 🚀 Quick Start (3 Commands)

### Step 1: Install Dependencies

```bash
cd web-ui/backend
pip install -r requirements.txt
```

### Step 2: Start the Backend Server

```bash
cd web-ui/backend
python app.py
```

Server starts on: http://localhost:8000

### Step 3: Open the Web UI

Open `web-ui/frontend/index.html` in your web browser.

**That's it! You're ready to go!**

## 🎯 One-Command Start

We've included a convenient script that does everything for you:

```bash
cd web-ui
./start.sh
```

This script:
- ✅ Installs all dependencies
- ✅ Starts the backend server
- ✅ Shows you how to open the web UI
- ✅ Handles everything automatically

## 📖 How to Use

### 1. Create a Task

1. Click "New Task" in the web UI
2. Enter your task description
3. Select modules (optional)
4. Click "Create Task"
5. Watch it execute in real-time!

### 2. Monitor Progress

- Click "Tasks" to see all your tasks
- Watch real-time status updates
- View results when complete
- Delete old tasks

### 3. Browse Modules

- Click "Modules" to see all 24+ expert modules
- See what each module does
- Check tool and prompt counts

### 4. View Analytics

- Click "Analytics" to see performance metrics
- Tasks completed
- Tokens used
- Average tokens per task
- Agent usage statistics

## 🏗️ Architecture

```
web-ui/
├── backend/
│   ├── app.py              # FastAPI server (300+ lines)
│   └── requirements.txt    # Python dependencies
└── frontend/
    └── index.html          # React web application (500+ lines)
```

**How it works:**
1. Backend (FastAPI) runs on localhost:8000
2. Frontend (React) opens in your browser
3. They communicate via REST API + WebSockets
4. Everything runs locally on YOUR machine
5. No data leaves your computer
6. No internet required

## 🎨 Features in Detail

### Web UI Dashboard
- Clean, modern interface
- Dark theme (easy on eyes)
- Responsive design
- Intuitive navigation

### Real-time Updates
- WebSocket-powered
- Live task status
- Instant notifications
- Real-time analytics

### Task Management
- Create tasks with one click
- Monitor progress in real-time
- View results when complete
- Delete old tasks

### Module Browser
- See all 24+ expert modules
- Read descriptions
- Check tool counts
- Select modules for tasks

### Performance Analytics
- Tasks completed counter
- Token usage tracking
- Average tokens per task
- Agent usage statistics
- Module popularity

## 🔧 API Endpoints

### Tasks
- `POST /api/task` - Create new task
- `GET /api/task/{id}` - Get task status
- `GET /api/tasks` - List all tasks
- `DELETE /api/task/{id}` - Delete task

### Modules
- `GET /api/modules` - List available modules

### Analytics
- `GET /api/analytics` - Get performance analytics
- `GET /api/performance` - Get detailed metrics

### WebSocket
- `WS /ws/{client_id}` - Real-time updates

## 📊 What You Can Do

### Examples

1. **Create a REST API**
   ```
   Task: "Create a REST API with FastAPI and PostgreSQL"
   Modules: python, fastapi, postgresql
   ```

2. **Build a Web App**
   ```
   Task: "Create a React component with TypeScript"
   Modules: javascript, react
   ```

3. **Deploy to Cloud**
   ```
   Task: "Deploy a Flask app to AWS ECS"
   Modules: python, aws, docker
   ```

## 🛠️ Development

### Backend

```bash
cd backend

# Install dependencies
pip install -r requirements.txt

# Run with auto-reload
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

### Frontend

The frontend is a single-file React application:
- No build step required
- No npm install needed
- Just open `index.html` in a browser
- Or serve with any HTTP server

## 🔒 Privacy & Security

**Everything runs locally:**
- ✅ No data leaves your machine
- ✅ No account required
- ✅ No cloud services
- ✅ No tracking
- ✅ No internet needed
- ✅ You are in control

## ❓ FAQ

**Q: Is this free?**
A: Yes, 100% free. No costs, no signup, no account.

**Q: Does it work offline?**
A: Yes, everything runs locally on your machine.

**Q: Do I need an account?**
A: No account needed. Just install and run.

**Q: Where does my data go?**
A: Nowhere. Everything stays on your machine.

**Q: Can I use this commercially?**
A: Yes, MIT license allows commercial use.

**Q: Do I need internet?**
A: Only for installing packages and using LLM APIs. The web UI itself works offline.

**Q: What browsers are supported?**
A: All modern browsers (Chrome, Firefox, Safari, Edge).

## 🆘 Troubleshooting

### Backend won't start
```bash
# Check Python version (3.8+)
python --version

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### Frontend not loading
```bash
# Make sure backend is running
# Check http://localhost:8000/api/health

# Try a different browser
# Make sure you're opening index.html (not index.html.md)
```

### Real-time updates not working
```bash
# Check WebSocket connection in browser console
# Make sure backend is running
# Try refreshing the page
```

## 📝 License

MIT License - Free for personal and commercial use

## 🎉 Conclusion

**The CogOS Web UI is:**
- ✅ 100% FREE
- ✅ 100% LOCAL
- ✅ 100% OPEN SOURCE
- ✅ EASY TO USE
- ✅ NO STRINGS ATTACHED

**Get started now:**
```bash
cd web-ui
./start.sh
```

---

**Made with ❤️ for the CogOS community**
