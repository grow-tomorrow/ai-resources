# Test

You are tasked with running tests for the codebase with options to run all tests or a targeted subset. This command provides an interactive way to execute tests based on the user's needs and current context.

## Initial Setup

When this command is invoked:

1. **Determine context** - Are you in an existing conversation or starting fresh?
   - If existing: Review what was implemented in this session
   - If fresh: Analyze recent changes to understand what might need testing

2. **Identify test scope**:
   - Check if specific files or features were recently modified
   - Look for test files that correspond to recent changes
   - Consider the current state of the codebase

3. **Discover project structure and test information**:
   ```bash
   # Check recent changes
   git status
   git diff --name-only HEAD~1..HEAD
   
   # Discover source code directories
   find . -type d -name "src" -o -name "lib" -o -name "app" -o -name "source" | head -10
   find . -name "*.py" -o -name "*.js" -o -name "*.ts" -o -name "*.java" -o -name "*.cs" | grep -v node_modules | head -10
   
   # Discover test directories and files
   find . -name "*test*" -type d | head -10
   find . -name "*test*" -type f | head -20
   find . -name "test_*" -type f | head -20
   find . -name "*.test.*" -type f | head -20
   find . -name "*.spec.*" -type f | head -20
   
   # Check test configuration files
   find . -name "jest.config.*" -o -name "pytest.ini" -o -name "pyproject.toml" -o -name "package.json" -o -name "Makefile" -o -name "*.csproj" -o -name "*.sln" | head -10
   ```

## Test Selection Process

### Step 1: Context Analysis

1. **Read any mentioned files** immediately and FULLY:
   - Test files mentioned by the user
   - Implementation files that need testing
   - Configuration files for test runners
   - **IMPORTANT**: Use the read_file tool WITHOUT limit/offset parameters to read entire files
   - **CRITICAL**: DO NOT use tools before reading these files yourself in the main context
   - **NEVER** read files partially - if a file is mentioned, read it completely

2. **Use parallel tool calls** to discover project and test structure:
   - Use codebase_search to find test patterns, configurations, and project structure
   - Use grep to find test files, test runners, and source code patterns
   - Use read_file to analyze test configuration files and package.json
   - Use run_terminal_cmd to discover available test commands and project structure
   - Focus on understanding the test ecosystem and source code organization

3. **Analyze recent changes**:
   - Identify what files were modified
   - Determine which tests are most relevant
   - Consider the scope of changes (unit, integration, e2e)

### Step 2: Interactive Test Selection

Present test options to the user:

```
I can help you run tests for this codebase. Based on my analysis, I found:

**Project Structure**:
- Source Code: [discovered directories like src/, lib/, app/, or root]
- Test Files: [discovered test directories and patterns]
- Test Framework: [pytest/jest/mocha/etc.]

**Available Test Commands**: 
- `make test` - Run all tests
- `npm test` - Run unit tests  
- `pytest [discovered_test_path]` - Run Python tests
- `jest --watch` - Run tests in watch mode

**Recent Changes**:
- Modified: [actual modified files from git diff]
- Added: [actual new files from git diff]

**Test Options**:
1. **Run All Tests** - Comprehensive test suite (recommended for CI/validation)
2. **Run Recent Changes Tests** - Focus on recently modified code
3. **Run Specific Test File** - Target a particular test file
4. **Run Test by Pattern** - Run tests matching a specific pattern
5. **Run Tests with Coverage** - Include coverage analysis

Which option would you prefer? (1-5)
```

### Step 3: Test Execution

Based on user selection:

#### Option 1: Run All Tests
```bash
# Execute comprehensive test suite
make test
# or: npm test
# or: pytest
# or: mvn test
```

#### Option 2: Run Recent Changes Tests
```bash
   # Find and run tests for recently modified files
   # Discover test files that correspond to modified source files
   git diff --name-only HEAD~1..HEAD | grep -E "\.(py|js|ts|java|go|rs|cs)$" | while read file; do
     # Find corresponding test files
     find . -name "*test*" -type f | grep -i "$(basename "$file" | sed 's/\.[^.]*$//')" | head -5
   done | xargs [discovered_test_runner]
```

#### Option 3: Run Specific Test File
```bash
# Run specific test file (adapt based on discovered test runner)
[discovered_test_runner] [path_to_specific_test_file]
# Examples:
# pytest tests/test_specific_feature.py
# npm test -- tests/specific.test.js
# mvn test -Dtest=TestClassName
# go test ./path/to/test
```

#### Option 4: Run Test by Pattern
```bash
# Run tests matching pattern
pytest -k "test_api_endpoints"
# or: npm test -- --grep "authentication"
```

#### Option 5: Run Tests with Coverage
```bash
# Run tests with coverage analysis (adapt based on discovered structure)
[discovered_test_runner] --cov=[discovered_source_path] --cov-report=html
# Examples:
# pytest --cov=src --cov-report=html
# pytest --cov=. --cov-report=html  # if source is in root
# npm test -- --coverage
# mvn test jacoco:report
```

### Step 4: Test Execution and Monitoring

1. **Execute the selected test command**:
   - Use run_terminal_cmd to execute the chosen test command
   - Monitor output for failures and warnings
   - Capture test results and timing information

2. **Handle test execution**:
   - If tests pass: Report success and summary
   - If tests fail: Analyze failures and provide guidance
   - If tests are slow: Suggest optimizations or subset options

3. **Provide real-time feedback**:
   ```
   Running tests for recent changes...
   
   ✓ tests/test_new_feature.py::test_happy_path PASSED
   ✓ tests/test_new_feature.py::test_error_handling PASSED
   ⚠ tests/test_integration.py::test_api_endpoint WARNING (slow)
   ❌ tests/test_edge_cases.py::test_boundary_condition FAILED
   
   Test Summary:
   - Total: 15 tests
   - Passed: 14
   - Failed: 1
   - Warnings: 1
   - Duration: 2.3s
   ```

### Step 5: Test Results Analysis

After test execution:

1. **Analyze test results**:
   - Identify failed tests and their causes
   - Note any warnings or performance issues
   - Check for flaky or intermittent failures

2. **Provide actionable feedback**:
   ```
   ## Test Results Analysis
   
   ### ✅ Passing Tests (14/15)
   - All unit tests for new feature passed
   - Integration tests working correctly
   - API endpoint tests successful
   
   ### ❌ Failed Tests (1/15)
   - `test_boundary_condition` - AssertionError: Expected 100, got 99
   - **Cause**: Off-by-one error in boundary calculation
   - **Fix**: Check the boundary logic in `src/feature/calculator.py:45`
   
   ### ⚠️ Warnings (1/15)
   - `test_api_endpoint` - Slow test (2.1s)
   - **Suggestion**: Consider mocking external API calls
   
   ### Recommendations
   1. Fix the boundary condition bug
   2. Optimize slow integration test
   3. Consider adding more edge case tests
   ```

3. **Suggest next steps**:
   - If tests fail: Provide specific fixes or debugging steps
   - If tests pass: Suggest additional test scenarios
   - If tests are slow: Recommend performance optimizations

### Step 6: Follow-up Actions

Based on test results:

1. **If tests failed**:
   - Offer to help debug specific failures
   - Suggest fixes for identified issues
   - Recommend additional test cases

2. **If tests passed**:
   - Suggest running additional test scenarios
   - Recommend performance or integration tests
   - Offer to run tests with different configurations

3. **If user wants to run different tests**:
   - Return to Step 2 for new test selection
   - Remember previous context and choices
   - Provide more targeted options

## Working with Existing Context

If you were part of the implementation:
- Review the conversation history for what was implemented
- Check your todo list for completed work
- Focus test selection on recently implemented features
- Consider running tests that validate the implementation

## Important Guidelines

1. **Be thorough but efficient** - Run the right tests for the context
2. **Provide clear feedback** - Explain what tests are running and why
3. **Handle failures gracefully** - Help debug issues when tests fail
4. **Consider performance** - Suggest optimizations for slow tests
5. **Be interactive** - Let users choose their testing approach

## Test Execution Checklist

Always verify:
- [ ] Correct test command is executed
- [ ] Test results are captured and analyzed
- [ ] Failures are properly diagnosed
- [ ] Performance issues are identified
- [ ] User gets actionable feedback
- [ ] Follow-up options are provided

## Project Structure Discovery

Before running tests, always discover the actual project structure:

### Common Project Patterns:
- **Source Code**: `src/`, `lib/`, `app/`, `source/`, or root directory
- **Tests**: `tests/`, `test/`, `spec/`, `__tests__/`, or co-located with source files
- **Configuration**: `package.json`, `pytest.ini`, `jest.config.js`, `Makefile`, `pyproject.toml`, `*.csproj`, `*.sln`
- **Languages**: Look for `.py`, `.js`, `.ts`, `.java`, `.go`, `.rs`, `.cs` files

### Discovery Commands:
```bash
# Find source directories
find . -type d -name "src" -o -name "lib" -o -name "app" -o -name "source"

# Find test directories and files
find . -name "*test*" -type d
find . -name "*test*" -type f -o -name "test_*" -o -name "*.test.*" -o -name "*.spec.*"

# Find configuration files
find . -name "package.json" -o -name "pytest.ini" -o -name "jest.config.*" -o -name "Makefile" -o -name "*.csproj" -o -name "*.sln"
```

## Tool Usage Guidelines

### Effective Tool Usage:
- Use codebase_search to find test patterns, configurations, and project structure
- Use grep to find specific test files, test functions, and source code patterns
- Use read_file to analyze test files, configuration files, and project structure
- Use run_terminal_cmd to execute test commands, discover project structure, and capture results
- Run multiple tools in parallel when analyzing different aspects

### When to Use Each Tool:
- codebase_search: Finding test patterns, configurations, test structure, and project organization
- grep: Finding specific test files, test functions, test imports, and source code patterns
- read_file: Analyzing complete test files, configuration files, and project structure
- run_terminal_cmd: Executing test commands, discovering project structure, checking test status, running coverage
- todo_write: Tracking test execution progress and results

## Common Test Commands by Language

### Python (pytest)
```bash
# All tests
pytest

# Specific file
pytest tests/test_feature.py

# Specific test
pytest tests/test_feature.py::test_specific_function

# With coverage
pytest --cov=src --cov-report=html

# Verbose output
pytest -v

# Stop on first failure
pytest -x
```

### JavaScript/Node.js (jest)
```bash
# All tests
npm test

# Watch mode
npm test -- --watch

# Specific file
npm test -- tests/feature.test.js

# With coverage
npm test -- --coverage

# Update snapshots
npm test -- --updateSnapshot
```

### Java (Maven/Gradle)
```bash
# Maven
mvn test

# Specific test class
mvn test -Dtest=TestClassName

# Gradle
./gradlew test

# Specific test
./gradlew test --tests TestClassName
```

### .NET (dotnet test)
```bash
# All tests
dotnet test

# Specific project
dotnet test MyProject.Tests.csproj

# Specific test class
dotnet test --filter "ClassName=MyTestClass"

# Specific test method
dotnet test --filter "MethodName=TestMethod"

# With coverage
dotnet test --collect:"XPlat Code Coverage"

# Verbose output
dotnet test --verbosity normal

# Run tests in watch mode
dotnet watch test
```

## Relationship to Other Commands

Recommended workflow:
1. `/implement_plan` - Execute the implementation
2. `/test` - Run tests to validate implementation
3. `/test_coverage` - Analyze and improve test coverage
4. `/validate_plan` - Verify implementation correctness
5. `/commit` - Create atomic commits for changes

The test command works well as a quick validation step during development and as part of the comprehensive validation process.

Remember: Good testing practices catch issues early and make development more confident. Focus on running the right tests for the current context and providing clear feedback on results.

