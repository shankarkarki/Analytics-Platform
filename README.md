# Analytics Platform 📊

A real-time analytics platform built with FastAPI. Track events, analyze user behavior, and get instant insights.

> 🚧 **Status**: Currently in Step 1 - Basic implementation with in-memory storage

## ✨ Current Features

- ✅ **Event Ingestion** - POST `/events` to track user actions
- ✅ **Basic Analytics** - GET `/analytics/summary` for insights  
- ✅ **REST API** - Clean, documented endpoints
- ✅ **Auto Documentation** - Swagger UI at `/docs`
- ✅ **Test Coverage** - Comprehensive test suite

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip

### Installation

```bash
# Clone and setup
git clone https://github.com/shankarkarki/analytics-platform.git
cd analytics-platform

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Run the server
python main.py
```

Server runs at: **http://localhost:8000**

## 🔥 Try It Out

### 1. Check if it's running:
```bash
curl http://localhost:8000
```

### 2. Send your first event:
```bash
curl -X POST "http://localhost:8000/events" \
  -H "Content-Type: application/json" \
  -d '{
    "event_name": "user_signup",
    "user_id": "user123", 
    "properties": {"source": "landing_page"}
  }'
```

### 3. Get analytics:
```bash
curl http://localhost:8000/analytics/summary
```

### 4. View API docs:
Visit: http://localhost:8000/docs

## 📊 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Health check |
| `POST` | `/events` | Send event data |
| `GET` | `/events` | Get recent events |
| `GET` | `/analytics/summary` | Analytics overview |

## 🧪 Testing

```bash
# Run tests
pytest

# Run with details
pytest -v

# Test specific file
pytest test_main.py
```

## 📁 Project Structure

```
analytics-platform/
├── main.py              # 🚀 FastAPI app
├── test_main.py         # 🧪 Tests  
├── requirements.txt     # 📦 Dependencies
├── .env.example        # ⚙️  Config template
└── README.md           # 📖 This file
```

## 🛣️ Roadmap

### ✅ Phase 1: Foundation (Current)
- [x] Basic FastAPI setup
- [x] Event ingestion
- [x] Simple analytics
- [x] Test coverage

### 🔄 Phase 2: Database (Next)
- [ ] PostgreSQL integration
- [ ] Data persistence
- [ ] Event history

### 🚀 Phase 3: Advanced Features
- [ ] Real-time dashboards
- [ ] User authentication
- [ ] Advanced analytics

## 🤔 Why This Project?

- **API Design** - RESTful endpoints with FastAPI
- **Data Processing** - Event ingestion and analytics
- **Testing** - Comprehensive test coverage
- **Documentation** - Clear API docs and README
- **Industry Practices** - Proper project structure



---
⭐ **Like this project? Give it a star!** ⭐
