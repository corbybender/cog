# CogOS Web UI

Modern web interface for CogOS with real-time collaboration, task management, and performance analytics.

## Features

✅ **Web UI Dashboard** - Modern React-based interface
✅ **Real-time Updates** - WebSocket-powered live updates
✅ **Task Management** - Create, monitor, and manage tasks
✅ **Module Browser** - Browse and select expert modules
✅ **Performance Analytics** - Track tokens, tasks, and performance
✅ **Custom Agent Creation** - API support for custom agents

## Quick Start

### Backend

```bash
cd web-ui/backend

# Install dependencies
pip install -r requirements.txt

# Start server
python app.py
```

Server runs on: http://localhost:8000

### Frontend

```bash
cd web-ui/frontend

# Open in browser
open index.html
```

Or use a simple HTTP server:

```bash
python -m http.server 3000
```

Then open: http://localhost:3000

## API Endpoints

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

## Features in Detail

### 1. Web UI Dashboard

Modern, responsive interface with:
- Task creation and management
- Real-time status updates
- Module selection
- Results display
- Dark theme

### 2. Real-time Collaboration

WebSocket-powered features:
- Live task updates
- Multi-user support
- Instant notifications
- Status broadcasting

### 3. Custom Agent Creation

Create custom agents via API:
```python
POST /api/agent
{
  "name": "my-agent",
  "description": "My custom agent",
  "agents": [...],
  "workflow": {...}
}
```

### 4. Performance Analytics

Track metrics:
- Tasks completed
- Tokens used
- Agent usage
- Module popularity
- Average tokens per task

## Architecture

```
web-ui/
├── backend/
│   ├── app.py              # FastAPI server
│   └── requirements.txt    # Python dependencies
└── frontend/
    └── index.html          # React application
```

## Development

### Backend

```bash
cd backend

# Install dependencies
pip install -r requirements.txt

# Run with auto-reload
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

### Frontend

The frontend is a single-file React application that can be:
1. Opened directly in a browser
2. Served with any HTTP server
3. Integrated into a build system

## Usage

1. Start the backend server
2. Open frontend in browser
3. Create a task
4. Monitor real-time updates
5. View analytics

## Next Steps

- [ ] Add user authentication
- [ ] Implement custom agent UI
- [ ] Add export functionality
- [ ] Create agent templates
- [ ] Add collaboration features

## License

MIT
