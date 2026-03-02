# CI/CD Pipeline Documentation

## Overview

This repository uses GitHub Actions for continuous integration and deployment. The pipeline automatically runs tests, checks code coverage, and performs quality checks on every push and pull request.

## Workflow: `ci.yml`

### Triggers

The CI pipeline runs on:
- **Push events** to branches:
  - `main`
  - `Week-*` (e.g., Week-3, Week-4)
  - `develop`
- **Pull request events** targeting:
  - `main`
  - `develop`

### Jobs

#### 1. Test Job
- **Purpose**: Run all tests with coverage analysis
- **Python versions**: 3.11, 3.12 (matrix strategy)
- **Steps**:
  1. Checkout code
  2. Set up Python environment
  3. Install dependencies from `requirements.txt`
  4. Run pytest with coverage
  5. Upload coverage reports to Codecov
  6. Upload HTML coverage report as artifact
  7. Verify coverage meets 80% threshold

**Coverage Requirements**:
- Minimum coverage: 80%
- Current coverage: 99%
- Pipeline fails if coverage drops below 80%

#### 2. Lint Job
- **Purpose**: Code quality and style checks
- **Checks**:
  - `flake8`: Python linting and complexity checks
  - `black`: Code formatting verification
  - `isort`: Import statement sorting
- **Note**: Linting failures are non-blocking (continue-on-error)

#### 3. Mutation Testing Job
- **Purpose**: Verify test quality through mutation testing
- **Runs**: After test job succeeds
- **Tests**:
  - Tag feature mutations
  - Version feature mutations
- **Note**: Non-blocking (continue-on-error)

#### 4. Build Status Job
- **Purpose**: Aggregate results and provide summary
- **Runs**: After test and lint jobs complete
- **Outputs**: Summary to GitHub Actions summary page

## Local Testing

### Run tests with coverage
```bash
cd backend
python -m pytest tests/ --cov=app --cov-report=term-missing --cov-fail-under=80 -v
```

### Run mutation tests
```bash
cd backend
python test_mutations_tags.py
python test_mutations_versions.py
```

### Run linting
```bash
cd backend
flake8 app/ tests/
black --check app/ tests/
isort --check-only app/ tests/
```

## Coverage Reports

Coverage reports are generated in multiple formats:
- **Terminal**: Displayed in CI logs
- **XML**: Uploaded to Codecov
- **HTML**: Available as downloadable artifact (retained for 7 days)

## Artifacts

The pipeline generates the following artifacts:
- `coverage-report`: HTML coverage report (Python 3.12 only)

## Status Badges

Add these badges to your README.md:

```markdown
![CI Pipeline](https://github.com/YOUR_USERNAME/YOUR_REPO/workflows/CI%20Pipeline/badge.svg)
[![codecov](https://codecov.io/gh/YOUR_USERNAME/YOUR_REPO/branch/main/graph/badge.svg)](https://codecov.io/gh/YOUR_USERNAME/YOUR_REPO)
```

## Troubleshooting

### Pipeline Fails on Coverage Check
If the pipeline fails with "Coverage below 80%":
1. Run tests locally: `pytest tests/ --cov=app --cov-report=term-missing`
2. Identify uncovered lines
3. Add tests to cover missing lines
4. Verify coverage: `pytest tests/ --cov=app --cov-fail-under=80`

### Linting Failures
Linting failures are non-blocking but should be addressed:
1. Run `black app/ tests/` to auto-format code
2. Run `isort app/ tests/` to sort imports
3. Fix any remaining flake8 issues manually

## Best Practices

1. **Always run tests locally** before pushing
2. **Maintain coverage above 80%** (current: 99%)
3. **Follow code style guidelines** (black, isort)
4. **Review mutation test results** to ensure test quality
5. **Keep dependencies updated** in requirements.txt

## Configuration Files

- `.github/workflows/ci.yml`: Main CI pipeline configuration
- `backend/requirements.txt`: Python dependencies
- `backend/pytest.ini`: Pytest configuration (if exists)
- `backend/.coveragerc`: Coverage configuration (if exists)
