# Testing Guide - Bob Onboarding Accelerator

## Overview

This guide provides comprehensive instructions for running all test suites in the Bob Onboarding Accelerator project.

## Test Infrastructure

### Backend Testing
- **Framework**: pytest with pytest-asyncio
- **Coverage Tool**: pytest-cov
- **Mocking**: pytest-mock, unittest.mock
- **Target Coverage**: 80%+

### Frontend Testing
- **Framework**: Vitest with React Testing Library
- **E2E Testing**: Playwright
- **Coverage Tool**: Vitest coverage (c8)

## Running Tests

### Backend Unit Tests

Run all unit tests with coverage:
```bash
python -m pytest backend/tests/ -v --cov=backend --cov-report=html --cov-report=term-missing -m "not integration and not security and not e2e and not performance"
```

Run specific test file:
```bash
python -m pytest backend/tests/test_bob_client.py -v
python -m pytest backend/tests/test_repo_reader.py -v
python -m pytest backend/tests/test_prompt_templates.py -v
python -m pytest backend/tests/test_main.py -v
```

### Backend Integration Tests

Run integration tests (requires real repository access):
```bash
python -m pytest backend/tests/integration/ -v -m integration
```

### Backend Security Tests

Run security vulnerability tests:
```bash
python -m pytest backend/tests/security/ -v -m security
```

### Frontend Unit Tests

Run frontend tests:
```bash
cd frontend
pnpm test
```

Run with coverage:
```bash
cd frontend
pnpm test:coverage
```

### End-to-End Tests

Run E2E tests with Playwright:
```bash
cd frontend
pnpm test:e2e
```

Run E2E tests in headed mode (see browser):
```bash
cd frontend
pnpm test:e2e:headed
```

### Performance Tests

Run load tests with Locust:
```bash
# Start backend first
cd backend
python main.py

# In another terminal, run Locust
cd backend/tests/performance
locust -f test_load.py --host=http://localhost:8000
```

Then open http://localhost:8089 to configure and run load tests.

## Test Coverage Reports

### Backend Coverage

After running tests with `--cov-report=html`, open:
```
htmlcov/index.html
```

### Frontend Coverage

After running `pnpm test:coverage`, open:
```
frontend/coverage/index.html
```

## Current Test Status

### Unit Tests ✅
- **Backend**: 64 tests passing, 77% coverage
  - `test_bob_client.py`: 12 tests (100% coverage)
  - `test_repo_reader.py`: 16 tests (100% coverage)
  - `test_prompt_templates.py`: 18 tests (100% coverage)
  - `test_main.py`: 18 tests (100% coverage)

- **Frontend**: 427 lines of test code
  - `api.test.js`: API client tests
  - `App.test.jsx`: Component integration tests

### Integration Tests 🔄
- Full repository analysis flow
- Real GitHub repository cloning
- End-to-end API testing

### E2E Tests 🔄
- User journey testing
- Cross-browser testing (Chromium, Firefox, WebKit)
- Mobile device emulation

### Security Tests 🔄
- SQL injection prevention
- XSS attack prevention
- Command injection prevention
- Input validation
- OWASP Top 10 coverage

### Performance Tests 🔄
- Load testing scenarios
- Concurrent user simulation
- Response time validation

## Test Markers

Tests are organized using pytest markers:

- `@pytest.mark.integration`: Integration tests
- `@pytest.mark.security`: Security tests
- `@pytest.mark.e2e`: End-to-end tests
- `@pytest.mark.performance`: Performance tests
- `@pytest.mark.slow`: Slow-running tests

## Continuous Integration

Tests run automatically on:
- Every push to main branch
- Every pull request
- Scheduled daily runs

See `.github/workflows/ci.yml` for CI/CD configuration.

## Troubleshooting

### Common Issues

**Issue**: ModuleNotFoundError
```bash
# Solution: Install dependencies
pip install -r requirements.txt
cd frontend && pnpm install
```

**Issue**: Tests fail with "marker not found"
```bash
# Solution: Check pytest.ini has all markers defined
```

**Issue**: Coverage below 80%
```bash
# Solution: Run only unit tests (integration/security tests are separate)
python -m pytest backend/tests/ -m "not integration and not security and not e2e and not performance"
```

**Issue**: Frontend tests fail
```bash
# Solution: Ensure pnpm is installed and dependencies are up to date
npm install -g pnpm
cd frontend && pnpm install
```

## Best Practices

1. **Run unit tests frequently** during development
2. **Run integration tests** before committing
3. **Run E2E tests** before creating pull requests
4. **Run security tests** before deploying
5. **Run performance tests** after major changes
6. **Check coverage reports** to identify untested code
7. **Keep tests fast** - unit tests should run in seconds
8. **Mock external dependencies** in unit tests
9. **Use real services** in integration tests
10. **Test edge cases** and error conditions

## Test Data

### Mock Repositories
- Small repo: < 10 files
- Medium repo: 10-50 files
- Large repo: 50+ files

### Test Fixtures
Located in `backend/tests/fixtures/`:
- Sample repository structures
- Mock API responses
- Test configuration files

## Next Steps

1. ✅ Unit tests implemented and passing
2. 🔄 Run integration tests with real repositories
3. 🔄 Run E2E tests in CI/CD pipeline
4. 🔄 Run security tests and fix vulnerabilities
5. 🔄 Run performance tests and optimize
6. 🔄 Achieve 80%+ coverage across all modules

## Resources

- [pytest Documentation](https://docs.pytest.org/)
- [Vitest Documentation](https://vitest.dev/)
- [Playwright Documentation](https://playwright.dev/)
- [Locust Documentation](https://docs.locust.io/)
- [Testing Best Practices](https://testingjavascript.com/)