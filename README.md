# CyberMentorTok

TikTok-style cybersecurity education platform. Learn cybersecurity through short, engaging videos with Peter Griffin and Stewie Griffin dialogues.

## Architecture

```
backend/          FastAPI + PostgreSQL + Redis
frontend/         Flutter (Mobile/Web)
infrastructure/   Docker + Kubernetes + Terraform
```

## Quick Start

### Prerequisites
- Python 3.12+
- Flutter 3.19+
- Docker & Docker Compose
- PostgreSQL 16+

### Development Setup

```bash
# Clone and enter project
cd CyberMentorTok

# Start infrastructure
cd infrastructure/docker
docker-compose up -d

# Setup backend
cd ../../backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Seed knowledge graph
python -m scripts.seed_db

# Start API
uvicorn app.main:app --reload

# Setup frontend
cd ../frontend
flutter pub get
flutter run
```

### API Documentation
Once running, visit: http://localhost:8000/docs

## Project Structure

```
CyberMentorTok/
├── backend/
│   ├── app/
│   │   ├── api/v1/          # API routes
│   │   ├── core/            # Config, DB, security
│   │   ├── models/          # SQLAlchemy models
│   │   ├── schemas/         # Pydantic schemas
│   │   ├── services/        # Business logic
│   │   └── workers/         # Celery workers
│   ├── migrations/          # Alembic migrations
│   └── tests/               # Test suite
├── frontend/
│   └── lib/
│       ├── models/          # Dart models
│       ├── screens/         # UI screens
│       ├── widgets/         # Reusable widgets
│       ├── providers/       # State management
│       └── services/        # API client
├── infrastructure/
│   ├── docker/              # Docker Compose
│   ├── kubernetes/          # K8s manifests
│   └── terraform/           # IaC
└── scripts/                 # Utility scripts
```

## Knowledge Graph

The platform uses a graph-based knowledge structure where every concept has:
- Prerequisites (required and recommended)
- Difficulty level (1-6)
- Related concepts
- Next concepts

### Difficulty Levels
1. **Beginner** - Computer basics
2. **Elementary** - Networking fundamentals
3. **Intermediate** - Linux, Windows, Programming
4. **Advanced** - Blue/Red Team, Cloud
5. **Expert** - Detection Engineering, Threat Hunting
6. **Master** - Kernel, Exploit Dev, Reverse Engineering

## API Endpoints

### Authentication
- `POST /api/v1/auth/register` - Create account
- `POST /api/v1/auth/login` - Login
- `POST /api/v1/auth/refresh` - Refresh token

### Feed
- `GET /api/v1/videos/feed` - Personalized video feed
- `GET /api/v1/videos/feed/anonymous` - Anonymous feed

### Content
- `GET /api/v1/concepts/` - List concepts
- `GET /api/v1/concepts/graph` - Knowledge graph
- `GET /api/v1/lessons/` - List lessons
- `GET /api/v1/lessons/{id}/feed` - Lesson feed item

### Progress
- `GET /api/v1/progress/dashboard` - Learning dashboard
- `POST /api/v1/progress/lesson` - Update progress
- `GET /api/v1/progress/concept/{id}` - Concept mastery

### Quizzes
- `GET /api/v1/quizzes/lesson/{id}` - Get quizzes
- `POST /api/v1/quizzes/submit` - Submit answer

### Search
- `GET /api/v1/search/?q=query` - Search
- `GET /api/v1/search/autocomplete?q=query` - Autocomplete

### Admin
- `POST /api/v1/pipeline/generate-lesson` - Generate lesson
- `POST /api/v1/pipeline/validate/{id}` - Validate content
- `POST /api/v1/pipeline/render/{id}` - Start rendering

## Content Pipeline

1. **Knowledge Graph** → Concepts and prerequisites
2. **Lesson Generator** → AI generates structured lessons
3. **Dialogue Generator** → Creates Peter/Stewie dialogues
4. **Fact Validation** → Validates accuracy (>95% confidence)
5. **Voice Generation** → TTS with character voices
6. **Subtitle Generation** → Word-level timing
7. **Background Selection** → Random satisfying video
8. **Video Rendering** → Composite final video
9. **Quality Review** → Admin approval
10. **Publish** → Available in feed

## Development

### Running Tests
```bash
cd backend
pytest tests/ -v --cov=app
```

### Linting
```bash
cd backend
ruff check app/
mypy app/
```

### Building for Production
```bash
docker build -f infrastructure/docker/Dockerfile.backend -t cybermentortok-api .
docker build -f infrastructure/docker/Dockerfile.worker -t cybermentortok-worker .
```
