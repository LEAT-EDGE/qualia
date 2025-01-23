# Complete Guide to PDM (Python Development Master)

```{contents} Table of Contents
---
depth: 3
---
```

## 1. Introduction to PDM
PDM is a modern Python package manager that supports PEP 582 and uses pyproject.toml for dependency specification. It aims to bring modern Python packaging features to developers while maintaining ease of use.

[PDM official documentation](https://pdm-project.org/en/latest/)

### Key Features
- PEP 582 support (local package installation)
- Dependency resolution
- Virtual environment management
- Project-based dependencies
- Lock file for reproducible installations
- Plugin system

## 2. Installation

### System Installation
```bash
# Using pip
pip install pdm

# Using Homebrew (macOS)
brew install pdm

# Using Scoop (Windows)
scoop install pdm
```

### Verify Installation
```bash
pdm --version
```

## 3. Project Management

### Initialize a New Project
```bash
# Create a new project
pdm init

# Initialize in current directory
cd my_project
pdm init
```

### Project Structure
```
my_project/
├── pyproject.toml      # Project configuration
├── pdm.lock           # Lock file
├── __pypackages__/    # Local packages directory
├── src/               # Source code
│   └── my_project/
└── tests/             # Test files
```

### Configuration in pyproject.toml
```toml
[project]
name = "my-project"
version = "0.1.0"
description = "My Python project"
authors = [
    {name = "Your Name", email = "your.email@example.com"},
]
dependencies = [
    "requests>=2.25.0",
    "pandas>=1.2.0",
]
requires-python = ">=3.8"

[build-system]
requires = ["pdm-backend"]
build-backend = "pdm.backend"

[tool.pdm]
package-dir = "src"
```

## 4. Dependency Management

### Adding Dependencies
```bash
# Add a production dependency
pdm add requests

# Add a development dependency
pdm add -d pytest

# Add with specific version
pdm add "requests>=2.25.0"

# Add multiple packages
pdm add requests pandas numpy
```

### Removing Dependencies
```bash
# Remove a package
pdm remove requests

# Remove a dev dependency
pdm remove -d pytest
```

### Installing Dependencies
```bash
# Install all dependencies
pdm install

# Install only production dependencies
pdm install --prod

# Install with specific Python version
pdm install --python 3.9
```

### Updating Dependencies
```bash
# Update all packages
pdm update

# Update specific package
pdm update requests

# Update based on lock file
pdm sync
```

### Managing Groups
```bash
# Add a new dependency group
pdm add -G test pytest

# Install specific group
pdm install -G test

# Remove from group
pdm remove -G test pytest
```

## 5. Virtual Environment Handling

### Virtual Environment Management
```bash
# Create a new environment
pdm venv create

# Create with specific Python version
pdm venv create --python 3.9

# List environments
pdm venv list

# Remove environment
pdm venv remove <name>

# Activate environment
pdm venv activate
```

## 6. Publishing Packages

### Build Package
```bash
# Build distribution
pdm build

# Build specific format
pdm build --format wheel
```

### Publish Package
```bash
# Publish to PyPI
pdm publish

# Publish to custom repository
pdm publish -r custom
```

## 7. Best Practices

### Project Organization
- Use `src` layout for your packages
- Keep tests outside the main package
- Use dependency groups effectively
- Maintain a clean requirements structure

### Dependency Management
- Use specific versions in production
- Lock dependencies for reproducibility
- Regular security updates
- Use dependency groups for different environments

### Version Control
```bash
# Files to include in .gitignore
__pypackages__/
.pdm-python
.pdm.toml
dist/
```

## 8. Advanced Features

### Scripts Management
```toml
[tool.pdm.scripts]
test = "pytest tests/"
lint = "flake8 src/"
start = "python -m my_project"
```

### Using Scripts
```bash
# Run defined script
pdm run test

# Run arbitrary command
pdm run python -m pytest
```

### Plugin System
```bash
# Install plugin
pdm plugin add pdm-bump

# List plugins
pdm plugin list
```

### Lock File Management
```bash
# Generate lock file
pdm lock

# Update lock file
pdm lock --update

# Install from lock file
pdm sync
```

## Common Commands Reference

| Command | Description |
|---------|------------|
| `pdm init` | Initialize a project |
| `pdm install` | Install dependencies |
| `pdm add` | Add dependencies |
| `pdm remove` | Remove dependencies |
| `pdm update` | Update dependencies |
| `pdm run` | Run commands |
| `pdm build` | Build package |
| `pdm publish` | Publish package |

## Troubleshooting

### Common Issues

1. Dependency Resolution Conflicts
```bash
# Try updating the lock file
pdm lock --update

# Check for outdated packages
pdm update --dry-run
```

2. Virtual Environment Issues
```bash
# Remove and recreate environment
pdm venv remove default
pdm venv create
```

3. Build Issues
```bash
# Clean build files
pdm clean
pdm build --clean
```

### Tips for Success
1. Always use a lock file for production
2. Keep your PDM version updated
3. Use dependency groups effectively
4. Document your project's requirements
5. Regular security audits