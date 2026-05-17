# 🛠️ Setup Guide

## Bob Onboarding Accelerator - Development Environment Setup

### Prerequisites

- **Python:** 3.11+
- **Node.js:** 18+
- **pnpm:** 8.0+ (install with `npm install -g pnpm`)
- **Git:** Latest version

---

## Quick Setup

### 1. Install Python Dependencies

```bash
# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Install Frontend Dependencies

```bash
# Install pnpm globally if not already installed
npm install -g pnpm

# Install frontend dependencies
cd frontend
pnpm install
cd ..
```

### 3. Configure Environment Variables

```bash
# Copy example environment file
cp .env.example .env.local

# Edit .env.local and add your Bob API credentials:
# BOB_API_ENDPOINT=https://api.ibm.com/bob/v1/chat
# BOB_API_KEY=your-api-key-here
```

---

## Running Tests

### Backend Tests

```bash
# Ensure virtual environment is activated
# Run all tests with coverage
pytest --cov=backend --cov-report=html

# Run specific test file
pytest backend/tests/test_bob_client.py -v

# Run without integration tests (faster)
pytest -m "not integration"

# Run only unit tests
pytest backend/tests/test_*.py -v
```

### Frontend Tests

```bash
cd frontend

# Run unit tests
pnpm test

# Run with coverage
pnpm test:coverage

# Run with UI
pnpm test:ui
```

### E2E Tests

```bash
# Install Playwright browsers (first time only)
cd frontend
pnpm exec playwright install

# Run E2E tests
pnpm test:e2e

# Run with UI
pnpm test:e2e:ui

# Run in headed mode (see browser)
pnpm test:e2e:headed
```

### Integration Tests

```bash
# Requires Bob API credentials in .env.local
pytest -m integration -v
```

### Performance Tests

```bash
# Install Locust if not already installed
pip install locust

# Run performance tests
locust -f tests/performance/locustfile.py --host=http://localhost:8000
```

### Security Tests

```bash
# Run security tests
pytest -m security -v

# Run security scans
bandit -r backend/
safety check
```

---

## Running the Application

### Development Mode

**Backend:**
```bash
# Ensure virtual environment is activated
cd backend
python main.py
# Or with uvicorn directly:
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Frontend:**
```bash
cd frontend
pnpm dev
```

### With Docker

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

---

## Troubleshooting

### Python Import Errors

If you see `ModuleNotFoundError`, ensure:

1. Virtual environment is activated:
   ```bash
   # Windows
   venv\Scripts\activate
   # macOS/Linux
   source venv/bin/activate
   ```

2. Dependencies are installed:
   ```bash
   pip install -r requirements.txt
   ```

3. You're running from the project root directory

### Frontend Module Errors

If you see module not found errors:

```bash
cd frontend
rm -rf node_modules pnpm-lock.yaml
pnpm install
```

### Playwright Browser Issues

```bash
cd frontend
pnpm exec playwright install --with-deps
```

### Port Already in Use

If port 8000 or 5173 is already in use:

```bash
# Find process using port (Windows)
netstat -ano | findstr :8000

# Kill process (Windows)
taskkill /PID <PID> /F

# On macOS/Linux
lsof -ti:8000 | xargs kill -9
```

---

## Project Structure

```
bob-onboarding/
├── backend/                 # Python FastAPI backend
│   ├── tests/              # Backend tests
│   │   ├── integration/    # Integration tests
│   │   └── security/       # Security tests
│   ├── bob_client.py       # Bob API client
│   ├── main.py            # FastAPI app
│   ├── prompt_templates.py # Prompt generation
│   └── repo_reader.py     # Repository cloning
├── frontend/               # React frontend
│   ├── src/
│   │   ├── __tests__/     # Frontend tests
│   │   └── components/    # React components
│   └── package.json
├── e2e/                   # E2E tests
├── tests/performance/     # Performance tests
├── k8s/                   # Kubernetes manifests
├── monitoring/            # Monitoring configs
├── scripts/               # Deployment scripts
├── docs/                  # Documentation
├── pytest.ini            # Pytest configuration
├── vitest.config.js      # Vitest configuration
├── playwright.config.js  # Playwright configuration
├── Dockerfile            # Docker image
├── docker-compose.yml    # Docker Compose
└── requirements.txt      # Python dependencies
```

---

## Next Steps

1. ✅ Install dependencies (Python + pnpm)
2. ✅ Configure environment variables
3. ✅ Run tests to verify setup
4. ✅ Start development servers
5. ✅ Read [API Documentation](docs/API_DOCUMENTATION.md)
6. ✅ Review [Deployment Runbook](docs/DEPLOYMENT_RUNBOOK.md)

---

## Common Commands Reference

```bash
# Backend
pytest --cov=backend --cov-report=html    # Run tests with coverage
python backend/main.py                     # Start backend server
bandit -r backend/                         # Security scan

# Frontend
pnpm test                                  # Run unit tests
pnpm test:e2e                             # Run E2E tests
pnpm dev                                   # Start dev server
pnpm build                                 # Build for production

# Docker
docker-compose up -d                       # Start all services
docker-compose logs -f backend            # View backend logs
docker-compose down                        # Stop all services

# Deployment
./scripts/smoke-test.sh http://localhost:8000  # Run smoke tests
kubectl apply -f k8s/                      # Deploy to Kubernetes
```

---

## Support

- **Documentation:** See `docs/` directory
- **Issues:** Create GitHub issue
- **Questions:** Contact team lead

---

**Last Updated:** 2026-05-17