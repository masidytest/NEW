# Web UI for AI Platform

## Files

- **index.html** - Dashboard with stats and navigation
- **chat.html** - Chat interface
- **goals.html** - Goals management
- **capabilities.html** - Capabilities browser

## Usage

1. Make sure the API server is running:
   ```bash
   python app.py
   ```

2. Open any HTML file in your browser:
   ```bash
   # Windows
   start web/index.html
   
   # Mac
   open web/index.html
   
   # Linux
   xdg-open web/index.html
   ```

3. Or use a local server:
   ```bash
   cd web
   python -m http.server 8080
   # Then open http://localhost:8080
   ```

## Features

### Dashboard (index.html)
- Real-time stats
- Navigation to all features
- Server status indicator

### Chat (chat.html)
- Full cognitive loop
- Real-time responses
- Response time tracking
- Error handling

### Goals (goals.html)
- Add new goals
- View all goals
- Status tracking
- Progress notes

### Capabilities (capabilities.html)
- Browse capabilities
- View capability gaps
- See plugin proposals
- Tag-based organization

## Requirements

- Modern web browser
- API server running on localhost:8000
- CORS enabled (already configured in app.py)
