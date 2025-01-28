# Contributing to Legislation Tracker

First off, thank you for considering contributing to Legislation Tracker! It's people like you that make this tool better for everyone. This document provides guidelines and steps for contributing.

## Table of Contents
- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Process](#development-process)
- [Pull Request Process](#pull-request-process)
- [Coding Standards](#coding-standards)
- [Reporting Bugs](#reporting-bugs)
- [Suggesting Enhancements](#suggesting-enhancements)

## Code of Conduct

This project and everyone participating in it is governed by our Code of Conduct. By participating, you are expected to uphold this code. Please report unacceptable behavior to [project maintainers].

## Getting Started

1. Fork the repository on GitHub
2. Clone your fork locally:
   ```bash
   git clone https://github.com/your-username/legislation-tracker.git
   cd legislation-tracker
   ```
3. Set up your development environment:
   ```bash
   # Backend setup
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt

   # Frontend setup
   cd ../frontend
   npm install
   ```
4. Create a new branch for your work:
   ```bash
   git checkout -b feature/your-feature-name
   ```

## Development Process

1. **Local Development**
   - Backend runs on `http://localhost:8000`
   - Frontend runs on `http://localhost:3000`
   - Use the development scripts in the `scripts/` directory

2. **Testing**
   ```bash
   # Backend tests
   cd backend
   pytest

   # Frontend tests
   cd frontend
   npm test
   ```

3. **Code Style**
   - Backend: Follow PEP 8
   - Frontend: Use ESLint configuration
   - Run linters before committing:
     ```bash
     # Backend
     flake8 .
     
     # Frontend
     npm run lint
     ```

## Pull Request Process

1. **Before Submitting**
   - Update documentation if needed
   - Add tests for new features
   - Ensure all tests pass
   - Update the README.md if needed
   - Follow the commit message format: `type(scope): description`
     - Types: feat, fix, docs, style, refactor, test, chore
     - Example: `feat(scraper): add support for California legislature`

2. **Submitting**
   - Push to your fork
   - Submit a pull request to the main repository
   - Fill out the pull request template
   - Link any relevant issues

3. **After Submitting**
   - Respond to reviewer comments
   - Make requested changes
   - Keep your PR updated with the main branch

## Coding Standards

### Python (Backend)
```python
# Use descriptive variable names
user_count = 42  # Good
uc = 42         # Bad

# Use type hints
def get_legislation(bill_id: str) -> Dict[str, Any]:
    pass

# Use docstrings
def fetch_state_bills(state: str) -> List[Dict]:
    """
    Fetch bills from a specific state.
    
    Args:
        state: Two-letter state code
        
    Returns:
        List of dictionaries containing bill information
    """
    pass
```

### JavaScript/React (Frontend)
```javascript
// Use functional components
const LegislationCard = ({ legislation }) => {
  // ...
};

// Use proper prop types
LegislationCard.propTypes = {
  legislation: PropTypes.shape({
    id: PropTypes.string.required,
    title: PropTypes.string.required,
    // ...
  }).isRequired,
};

// Use hooks appropriately
const useLegislation = (id) => {
  const [data, setData] = useState(null);
  // ...
};
```

## Reporting Bugs

1. **Before Reporting**
   - Check existing issues
   - Check if the bug is reproducible
   - Update to the latest version

2. **Writing Bug Reports**
   - Use the bug report template
   - Include:
     - Your environment details
     - Steps to reproduce
     - Expected vs actual behavior
     - Screenshots if applicable
     - Error messages

## Suggesting Enhancements

1. **Before Suggesting**
   - Check existing issues and pull requests
   - Review documentation to ensure the feature doesn't exist

2. **Writing Enhancement Suggestions**
   - Use the feature request template
   - Include:
     - Clear use case
     - Expected behavior
     - Potential implementation approach
     - Why this enhancement would be useful

## Communication

- Use GitHub Issues for bug reports and feature requests
- Use Pull Requests for code changes
- Join our [community chat/forum] for discussions

## Additional Notes

### Git Commit Messages
- Use the present tense ("Add feature" not "Added feature")
- Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
- Limit the first line to 72 characters
- Reference issues and pull requests after the first line

### Branch Naming
- Feature branches: `feature/description`
- Bug fix branches: `fix/description`
- Documentation branches: `docs/description`

### Version Numbers
We use [Semantic Versioning](https://semver.org/):
- MAJOR version for incompatible API changes
- MINOR version for backwards-compatible functionality
- PATCH version for backwards-compatible bug fixes

## Recognition

Contributors will be recognized in:
- The project's README.md
- Our contributors page
- Release notes

Thank you for contributing to Legislation Tracker!
