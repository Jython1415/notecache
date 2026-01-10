# Claude.ai Development Guide for notecache

This document provides guidance for Claude.ai (or other AI assistants) when working on the `notecache` project.

## Project Overview

**notecache** is a Python package for persistent, state-dependent caching of objects in Jupyter notebooks. It enables expensive computations to be cached across notebook sessions and only recomputed when their input state changes.

### Core Concept

The package solves a common problem in data science workflows: expensive computations (like large DataFrame transformations) need to be cached, but traditional caching doesn't handle:
- Persistence across notebook sessions
- State-dependent invalidation
- Automatic recomputation when inputs change

### Key Features

- Single-function API: `notecache.load(state, generate, unique_id, **options)`
- State-based cache invalidation
- Persistent storage using pickle
- Support for custom state comparison functions
- Flexible cache organization with custom folders and hash functions

## Architecture

### Core Components

1. **`cache.py`**: Main module with the `load()` function
   - Handles state comparison, file I/O, and cache management
   - Uses pickle for object serialization
   - Implements SHA-512 hashing for unique file names

2. **Type System**:
   - Generic types using `TypeVar` for flexibility
   - `StorageObject`: NamedTuple wrapping (state, object) pairs
   - `Load`: NamedTuple return value with metadata (object, path, generated, state_change, error)

3. **State Comparison**:
   - Default: Uses `!=` operator
   - Special handling: Detects `.equals()` method (for pandas DataFrames)
   - Customizable: Accepts user-defined `reload` function

### Design Patterns

- **Lazy Evaluation**: Objects generated only when needed
- **Memoization**: Results cached with state-based invalidation
- **Strategy Pattern**: Pluggable state comparison and hash functions

## Development Guidelines

### Code Style

- Uses type hints throughout
- Follows PEP 8 conventions
- pylint-compliant (with selective disables)
- Docstrings use reStructuredText format

### Testing Approach

- Property-based testing with Hypothesis
- Tests cover:
  - Various object types (primitives, DataFrames, dicts)
  - State comparison logic
  - unique_id collision avoidance
  - Custom reload functions
  - Folder isolation
  - Force update behavior

### Dependencies

**Runtime**: None (pure Python with stdlib only)

**Development**:
- `pytest`: Test runner
- `hypothesis`: Property-based testing
- `numpy`, `pandas`: Test fixtures
- `pylint`: Linting
- `twine`, `build`: Publishing

## Common Tasks

### Adding New Features

When adding features, consider:

1. **Backward Compatibility**: This is a caching library - breaking changes affect saved cache files
2. **Type Safety**: Maintain generic type variables for flexibility
3. **Test Coverage**: Add property-based tests when possible
4. **Documentation**: Update README.md with examples

### Testing

```bash
# Activate virtual environment
source .venv/bin/activate

# Run unit tests
pytest tests/unit

# Run with coverage
pytest tests/unit --cov=src/notecache
```

### Common Edge Cases

1. **Pickle Errors**: Corrupted cache files are deleted and regenerated
2. **State Comparison Failures**: Falls back to `!=` if `.equals()` raises exception
3. **Hash Collisions**: Uses last 5 chars of SHA-512 hash + normalized unique_id
4. **Missing Folders**: No automatic creation - will raise error if folder doesn't exist

## Known Limitations & Considerations

### Security

- **Pickle vulnerability**: Deserializing untrusted cache files can execute arbitrary code
- Users should only use notecache with trusted data sources
- Consider documenting this security consideration in user-facing docs

### Performance

- **No compression**: Large objects stored as-is
- **No size limits**: Could fill disk with cached data
- **No cleanup mechanism**: Old cache files persist indefinitely

### Functionality Gaps

- No TTL (time-to-live) for cache entries
- No cache size management or LRU eviction
- No cache statistics or introspection
- No parallel-safe locking for concurrent access

## File Structure

```
notecache/
├── src/notecache/
│   ├── __init__.py          # Public API exports
│   └── cache.py             # Core implementation
├── tests/unit/
│   └── test_cache.py        # Property-based tests
├── scripts/
│   ├── initialize.sh        # Developer setup
│   ├── publish.sh           # PyPI publishing
│   └── publish-test.sh      # TestPyPI publishing
├── pyproject.toml           # Build configuration
├── requirements.txt         # Dev dependencies
└── README.md                # User documentation
```

## Best Practices for AI-Assisted Development

### When Adding Features

1. Read existing code first to understand patterns
2. Maintain the simple, focused API design
3. Add comprehensive tests (prefer property-based when applicable)
4. Update docstrings and README
5. Consider backward compatibility with existing cache files

### When Fixing Bugs

1. Understand the caching semantics before changing behavior
2. Add regression tests
3. Consider impact on existing cached data
4. Document breaking changes clearly

### When Refactoring

1. Preserve the public API (`load` function signature)
2. Maintain type annotations
3. Keep the implementation simple and readable
4. Ensure all tests pass

## Project Status

- **Version**: 0.0.1.dev1 (Alpha)
- **Python Support**: 3.9+
- **License**: MIT
- **Maintenance**: Active development

## Contributing

This project follows standard GitHub workflow:
1. Fork and clone
2. Create feature branch
3. Make changes with tests
4. Submit pull request with description

For questions or issues, contact the maintainer or open a GitHub issue.
