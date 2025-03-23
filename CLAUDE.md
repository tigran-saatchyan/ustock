# UStock Commands and Style Guide

## Build/Run/Test Commands
```bash
# Install dependencies
poetry install

# Run server
poetry run python src/manage.py runserver

# Run migrations
poetry run python src/manage.py migrate

# Run all tests
poetry run pytest

# Run specific test file
poetry run pytest src/apps/tickers/tests.py

# Run specific test function
poetry run pytest src/apps/tickers/tests.py::test_ticker_info_api
```

## Code Style Guide
- **Imports**: Standard library first, third-party second, local modules last. Alphabetize within groups.
- **Docstrings**: Google-style with Args/Returns sections and triple double-quotes.
- **Formatting**: 4-space indentation, ~88-100 character line limit.
- **Naming**: CamelCase for classes, snake_case for functions/variables, UPPER_SNAKE_CASE for constants.
- **Error Handling**: Use specific exceptions, proper logging, and return empty collections (not None).
- **Type Hints**: Document types in docstrings.
- **Testing**: pytest style with descriptive test names and assertions.