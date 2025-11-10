# Contributing to AI Chat Assistant

Thank you for your interest in contributing to the AI Chat Assistant project! This document provides guidelines and instructions for contributing.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [How to Contribute](#how-to-contribute)
- [Coding Standards](#coding-standards)
- [Testing Guidelines](#testing-guidelines)
- [Pull Request Process](#pull-request-process)
- [Bug Reports](#bug-reports)
- [Feature Requests](#feature-requests)

## Code of Conduct

### Our Pledge

We are committed to providing a welcoming and inspiring community for all. Please be respectful and constructive in your interactions.

### Expected Behavior

- Be respectful and inclusive
- Exercise empathy and kindness
- Focus on what is best for the community
- Accept constructive criticism gracefully

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone <your-fork-url>`
3. Add upstream remote: `git remote add upstream <original-repo-url>`
4. Create a new branch: `git checkout -b feature/your-feature-name`

## Development Setup

### Prerequisites

- Python 3.8+
- Node.js 14+
- OpenAI API key

### Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Frontend Setup

```bash
cd frontend
npm install
```

See [SETUP_GUIDE.md](SETUP_GUIDE.md) for detailed instructions.

## How to Contribute

### Types of Contributions

- **Bug fixes**: Fix existing bugs
- **Features**: Implement new features
- **Documentation**: Improve docs
- **Tests**: Add or improve tests
- **Performance**: Optimize code
- **Refactoring**: Improve code quality

### Contribution Workflow

1. **Find or create an issue** - Check existing issues or create a new one
2. **Discuss** - Comment on the issue to discuss your approach
3. **Branch** - Create a feature branch from `main`
4. **Code** - Implement your changes
5. **Test** - Add tests and ensure all tests pass
6. **Commit** - Make atomic commits with clear messages
7. **Push** - Push to your fork
8. **Pull Request** - Open a PR to the main repository

## Coding Standards

### Python (Backend)

Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/):

```python
# Good
def calculate_response_time(start_time, end_time):
    """Calculate the response time in milliseconds."""
    return (end_time - start_time) * 1000

# Bad
def calcRespTime(st,et):
    return (et-st)*1000
```

**Key Points:**
- Use 4 spaces for indentation
- Max line length: 88 characters (Black formatter)
- Use descriptive variable names
- Add docstrings to functions and classes
- Type hints are encouraged

**Tools:**
- `black` for formatting
- `flake8` for linting
- `mypy` for type checking

```bash
pip install black flake8 mypy
black .
flake8 .
mypy .
```

### JavaScript/React (Frontend)

Follow standard JavaScript/React conventions:

```javascript
// Good
const ChatMessage = ({ message, sender, timestamp }) => {
  const formatTime = (timestamp) => {
    return new Date(timestamp).toLocaleTimeString();
  };

  return (
    <div className="message">
      {message}
    </div>
  );
};

// Bad
function ChatMessage(props) {
  return <div>{props.message}</div>
}
```

**Key Points:**
- Use functional components with hooks
- Use descriptive component and variable names
- Add PropTypes or TypeScript types
- Follow React best practices
- Use ES6+ features

**Tools:**
- ESLint for linting
- Prettier for formatting

```bash
npm run lint
npm run format
```

### Commit Messages

Follow [Conventional Commits](https://www.conventionalcommits.org/):

```
feat: add typing indicator to chat interface
fix: resolve OpenAI API timeout issue
docs: update API documentation
test: add unit tests for chat service
refactor: simplify context management logic
style: format code with black
chore: update dependencies
```

**Format:**
```
<type>(<scope>): <subject>

<body>

<footer>
```

**Examples:**

```
feat(chat): add message editing capability

- Allow users to edit their messages
- Update backend API to handle edits
- Add edit button to message component

Closes #123
```

```
fix(api): handle OpenAI rate limit errors

When OpenAI API returns 429 status, implement
exponential backoff retry logic.

Fixes #456
```

## Testing Guidelines

### Backend Tests

Write tests for:
- API endpoints
- Business logic
- Database operations
- Error handling

```python
# test_example.py
import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_chat_endpoint():
    """Test chat endpoint returns valid response."""
    response = client.post(
        "/api/chat",
        json={"message": "Hello"}
    )
    assert response.status_code == 200
    assert "response" in response.json()
```

**Run tests:**
```bash
cd backend
pytest
pytest --cov=. --cov-report=html
```

### Frontend Tests

Write tests for:
- Component rendering
- User interactions
- API integration
- State management

```javascript
// Example.test.js
import { render, screen, fireEvent } from '@testing-library/react';
import ChatMessage from './ChatMessage';

test('renders message content', () => {
  render(<ChatMessage message="Hello" sender="user" />);
  expect(screen.getByText('Hello')).toBeInTheDocument();
});
```

**Run tests:**
```bash
cd frontend
npm test
npm test -- --coverage
```

### Test Requirements

- All new features must include tests
- Maintain or improve test coverage
- Tests must pass before submitting PR
- Add integration tests for critical paths

## Pull Request Process

### Before Submitting

- [ ] Code follows project style guidelines
- [ ] All tests pass locally
- [ ] New tests added for new features
- [ ] Documentation updated if needed
- [ ] Commit messages follow conventions
- [ ] No merge conflicts with main branch

### PR Description Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
Describe testing performed

## Screenshots (if applicable)
Add screenshots for UI changes

## Checklist
- [ ] Tests pass
- [ ] Documentation updated
- [ ] Code follows style guidelines
- [ ] Self-review completed

## Related Issues
Closes #123
```

### Review Process

1. **Automated checks** - CI/CD runs tests and linting
2. **Code review** - Maintainers review your code
3. **Feedback** - Address any requested changes
4. **Approval** - Once approved, PR will be merged
5. **Merge** - Maintainer merges to main branch

### After Merge

- Delete your feature branch
- Pull latest main branch
- Update your fork

## Bug Reports

### Before Submitting

- Check existing issues
- Update to latest version
- Try to reproduce consistently

### Bug Report Template

```markdown
## Bug Description
Clear description of the bug

## Steps to Reproduce
1. Go to '...'
2. Click on '...'
3. See error

## Expected Behavior
What should happen

## Actual Behavior
What actually happens

## Environment
- OS: [e.g., Windows 10]
- Browser: [e.g., Chrome 120]
- Backend version: [e.g., 1.0.0]
- Frontend version: [e.g., 1.0.0]

## Screenshots
If applicable

## Additional Context
Any other relevant information
```

## Feature Requests

### Feature Request Template

```markdown
## Feature Description
Clear description of the feature

## Problem it Solves
What problem does this address?

## Proposed Solution
How should it work?

## Alternatives Considered
Other approaches you've thought about

## Additional Context
Screenshots, mockups, or examples
```

## Development Tips

### Local Development

1. **Use separate terminals** for backend and frontend
2. **Enable hot reload** for faster development
3. **Check logs** regularly for errors
4. **Use debug mode** when troubleshooting

### Backend Tips

```python
# Enable debug logging
import logging
logging.basicConfig(level=logging.DEBUG)

# Use debugger
import pdb; pdb.set_trace()
```

### Frontend Tips

```javascript
// Console logging
console.log('Debug:', data);

// React DevTools
// Install browser extension for component inspection
```

### Common Issues

**Import errors:**
```bash
# Backend
pip install -r requirements.txt

# Frontend
npm install
```

**Port conflicts:**
```bash
# Use different ports
PORT=8001 python main.py
PORT=3001 npm start
```

## Project Structure

Maintain this structure for consistency:

```
chat-bot/
├── backend/           # Python FastAPI backend
├── frontend/          # React frontend
├── docs/             # Additional documentation
├── .gitignore        # Git ignore rules
└── README.md         # Main documentation
```

## Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [React Documentation](https://react.dev/)
- [OpenAI API Documentation](https://platform.openai.com/docs)
- [Python PEP 8](https://www.python.org/dev/peps/pep-0008/)
- [React Best Practices](https://react.dev/learn)

## Questions?

If you have questions:
- Open a discussion on GitHub
- Check existing issues
- Read the documentation

## Recognition

Contributors will be recognized in:
- README.md contributors section
- Release notes
- Project acknowledgments

Thank you for contributing! 🎉

