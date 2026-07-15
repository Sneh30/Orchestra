# Contributing to Multi-Agent Research Orchestrator

Thank you for your interest in contributing! This document provides guidelines and instructions for contributing to this project.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [How to Contribute](#how-to-contribute)
- [Pull Request Process](#pull-request-process)
- [Coding Standards](#coding-standards)
- [Testing](#testing)
- [Documentation](#documentation)

## Code of Conduct

We are committed to providing a welcoming and inclusive experience for everyone. Please be respectful and constructive in all interactions.

## Getting Started

1. **Fork the Repository**
   - Click the "Fork" button on GitHub
   - Clone your fork locally:
     ```bash
     git clone https://github.com/YOUR_USERNAME/multi-agent-research-orchestrator.git
     cd multi-agent-research-orchestrator
     ```

2. **Set Up Development Environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   pip install -e ".[dev]"
   ```

3. **Configure Environment**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

4. **Run Tests**
   ```bash
   export LLM_PROVIDER=deterministic
   pytest
   ```

## Development Setup

### Prerequisites

- Python 3.11 or higher
- Docker and Docker Compose (for local development)
- PostgreSQL (or use Docker)

### Local Development

1. **Start the stack:**
   ```bash
   docker compose up --build
   ```

2. **Run the API locally (without Docker):**
   ```bash
   uvicorn research_orchestrator.main:app --reload --app-dir backend
   ```

3. **Access the API:**
   - API: http://localhost:8000
   - Swagger docs: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

### Code Quality Tools

```bash
# Linting
ruff check backend tests

# Type checking
mypy backend

# Format code
ruff format backend tests

# Run all checks
ruff check backend tests && mypy backend && pytest
```

## How to Contribute

### Reporting Bugs

1. Check existing issues to avoid duplicates
2. Create a new issue with:
   - Clear title and description
   - Steps to reproduce
   - Expected vs actual behavior
   - Environment details (Python version, OS, etc.)

### Suggesting Features

1. Check existing issues and discussions
2. Create a new issue with:
   - Clear title and description
   - Use case and motivation
   - Proposed solution (if any)

### Contributing Code

1. **Pick an Issue**
   - Look for issues labeled `good first issue` or `help wanted`
   - Comment on the issue to let others know you're working on it

2. **Create a Branch**
   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b fix/your-bug-fix
   ```

3. **Make Changes**
   - Follow coding standards (see below)
   - Write tests for new functionality
   - Update documentation if needed

4. **Commit Changes**
   ```bash
   git commit -m "feat: add new feature"  # or
   git commit -m "fix: resolve bug in X"
   ```

5. **Push and Create PR**
   ```bash
   git push origin feature/your-feature-name
   ```

## Pull Request Process

1. **Before Submitting**
   - Ensure all tests pass: `pytest`
   - Run linting: `ruff check backend tests`
   - Run type checking: `mypy backend`
   - Update documentation if needed

2. **PR Description**
   - Clear title describing the change
   - Reference related issues (e.g., "Closes #123")
   - Describe what changed and why
   - Include screenshots for UI changes

3. **Review Process**
   - At least one maintainer approval required
   - All CI checks must pass
   - Address review feedback promptly

4. **After Approval**
   - Squash and merge (maintainer will do this)
   - Delete your feature branch

## Coding Standards

### Python Style

- Follow PEP 8 style guide
- Use type hints for all functions
- Maximum line length: 100 characters
- Use `ruff` for linting and formatting

### Code Organization

- Keep functions focused and small
- Use descriptive variable and function names
- Add docstrings for public functions and classes
- Group imports: standard library, third-party, local

### Git Commit Messages

Follow [Conventional Commits](https://www.conventionalcommits.org/):

- `feat:` for new features
- `fix:` for bug fixes
- `docs:` for documentation changes
- `style:` for formatting changes
- `refactor:` for code refactoring
- `test:` for adding tests
- `chore:` for maintenance tasks

Examples:
```
feat: add source credibility scoring
fix: resolve async timeout in research service
docs: update API documentation with examples
test: add unit tests for evaluation metrics
```

## Testing

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=research_orchestrator --cov-report=term-missing

# Run specific test file
pytest tests/unit/test_scoring.py

# Run specific test
pytest tests/unit/test_scoring.py::test_domain_for_normalizes_www
```

### Writing Tests

- Place tests in appropriate directories:
  - `tests/unit/` for unit tests
  - `tests/integration/` for integration tests
  - `tests/e2e/` for end-to-end tests
- Use descriptive test names
- Test both success and failure cases
- Use fixtures for common setup

### Test Environment

- Use `LLM_PROVIDER=deterministic` for tests that don't need real APIs
- Use `DeterministicLLMProvider` and `FakeSearchTool` for testing
- Tests should be isolated and not depend on external services

## Documentation

### Code Documentation

- Add docstrings to all public functions and classes
- Use type hints for all parameters and return values
- Keep comments up-to-date with code changes

### Project Documentation

- Update README.md for new features or setup changes
- Update API documentation in `docs/api-design.md`
- Add examples for new functionality

### Documentation Style

- Use clear, concise language
- Include code examples where helpful
- Keep formatting consistent

## Questions?

If you have questions about contributing, feel free to:
- Open a discussion on GitHub
- Check existing documentation in `docs/`
- Review the [README](README.md) for project overview

Thank you for contributing!
