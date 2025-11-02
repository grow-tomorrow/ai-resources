# Test Coverage

You are tasked with analyzing test coverage for recent changes and ensuring we maintain 90% coverage of use cases. This command works with git changes to identify what needs testing and can generate additional tests when needed.

## Initial Setup

When this command is invoked:

1. **Determine context** - Are you in an existing conversation or starting fresh?
   - If existing: Review what was implemented in this session
   - If fresh: Need to discover what was changed through git analysis

2. **Identify the scope**:
   - If plan path provided, use it to understand what should be tested
   - If no plan, analyze recent git changes to determine scope
   - Focus on new/modified files and their test coverage

3. **Discover project structure and gather coverage data**:
   ```bash
   # Check recent commits
   git log --oneline -n 10
   git diff HEAD~N..HEAD  # Where N covers recent changes
   
   # Discover source code directories
   find . -type d -name "src" -o -name "lib" -o -name "app" -o -name "source" | head -10
   find . -name "*.py" -o -name "*.js" -o -name "*.ts" -o -name "*.java" -o -name "*.cs" | grep -v node_modules | head -10
   
   # Discover test directories and files
   find . -name "*test*" -type d | head -10
   find . -name "*test*" -type f | head -20
   find . -name "test_*" -type f | head -20
   
   # Run coverage analysis (adapt based on discovered structure)
   cd $(git rev-parse --show-toplevel) && make test-coverage
   # or: npm run test:coverage
   # or: pytest --cov=[discovered_source_path] --cov-report=html
   # or: pytest --cov=. --cov-report=html  # if source is in root
   # or: dotnet test --collect:"XPlat Code Coverage"
   ```

## Coverage Analysis Process

### Step 1: Context Discovery

If starting fresh or need more context:

1. **Read the implementation plan** (if provided) to understand what should be tested
2. **Identify changed files**:
   - List all files that were modified/added
   - Note the scope of changes (new features, bug fixes, refactoring)
   - Identify key functionality that needs test coverage

3. **Use parallel tool calls** to discover project structure and analyze test coverage:
   - Use codebase_search to find existing tests, source code patterns, and project structure
   - Use grep to find test patterns, coverage markers, and source code files
   - Use read_file to analyze test files, configuration files, and their coverage
   - Use run_terminal_cmd to discover project structure and execute coverage tools
   - Focus on finding gaps in test coverage for the actual project structure

### Step 2: Coverage Assessment

For each modified file or feature:

1. **Check existing test coverage**:
   - Look for unit tests, integration tests, and end-to-end tests
   - Verify tests cover the new/modified functionality
   - Check if edge cases and error conditions are tested

2. **Run automated coverage analysis**:
   - Execute coverage tools to get current percentages
   - Identify specific lines/functions that lack coverage
   - Document coverage gaps with file:line references

3. **Assess test quality**:
   - Are tests meaningful and testing actual behavior?
   - Do tests cover both happy path and error cases?
   - Are there missing integration tests for new features?

4. **Calculate coverage percentage**:
   - Focus on new/modified code coverage
   - Consider both line coverage and branch coverage
   - Identify critical paths that must be tested

### Step 3: Coverage Report Generation

Create comprehensive coverage analysis:

```markdown
## Test Coverage Report: [Feature/Change Name]

### Coverage Summary
- Overall Coverage: 85% (Target: 90%)
- New Code Coverage: 78% (Target: 90%)
- Critical Path Coverage: 95% ✓
- Edge Case Coverage: 60% ⚠️

### Files Analyzed
- `[discovered_source_path]/feature/new_module.py` - 82% coverage
- `[discovered_source_path]/api/endpoints.py` - 91% coverage ✓
- `[discovered_source_path]/utils/helpers.py` - 45% coverage ❌

### Coverage Gaps Identified

#### High Priority (Critical functionality):
- `[discovered_source_path]/feature/new_module.py:45-67` - Error handling not tested
- `[discovered_source_path]/feature/new_module.py:89-102` - Edge case validation missing

#### Medium Priority (Important but not critical):
- `[discovered_source_path]/utils/helpers.py:23-45` - Utility functions need more test cases
- `[discovered_source_path]/api/endpoints.py:156-178` - Integration scenarios missing

#### Low Priority (Nice to have):
- `[discovered_source_path]/feature/new_module.py:120-135` - Performance edge cases

### Existing Test Quality
✓ Unit tests cover core functionality
✓ Integration tests verify API endpoints
⚠️ Missing error condition tests
❌ No performance/load tests

### Recommendations
1. Add error handling tests for critical paths
2. Create integration tests for new API endpoints
3. Add edge case validation tests
4. Consider adding performance tests for high-traffic code
```

### Step 4: Interactive Test Generation

If coverage is below 90%:

1. **Present coverage analysis to user**:
   ```
   Current test coverage is [X]%, which is below our 90% target.
   
   I've identified [N] areas that need additional test coverage:
   - [Critical gap 1] - [impact explanation]
   - [Critical gap 2] - [impact explanation]
   - [Other gaps] - [impact explanation]
   
   Would you like me to generate additional tests to improve coverage?
   ```

2. **If user agrees to add tests**:
   - Use codebase_search to find similar test patterns
   - Use read_file to analyze existing test structure
   - Generate appropriate test cases for identified gaps
   - Focus on critical functionality first
   - Follow existing test patterns and conventions

3. **Generate test files**:
   - Create unit tests for uncovered functions
   - Add integration tests for new features
   - Include error case and edge case tests
   - Ensure tests follow project conventions

### Step 5: Test Implementation

When generating new tests:

1. **Analyze existing test patterns**:
   - Use codebase_search to find similar test files
   - Use read_file to understand test structure and conventions
   - Follow established patterns for test organization

2. **Create comprehensive test cases**:
   ```python
   # Example test structure
   def test_new_feature_happy_path():
       """Test the main functionality works as expected."""
       # Arrange
       input_data = create_test_data()
       
       # Act
       result = new_feature(input_data)
       
       # Assert
       assert result.status == "success"
       assert result.data is not None
   
   def test_new_feature_error_handling():
       """Test error conditions are handled properly."""
       # Arrange
       invalid_input = create_invalid_data()
       
       # Act & Assert
       with pytest.raises(ValidationError):
           new_feature(invalid_input)
   
   def test_new_feature_edge_cases():
       """Test edge cases and boundary conditions."""
       # Test empty input
       # Test maximum values
       # Test concurrent access
   ```

3. **Verify test quality**:
   - Ensure tests are meaningful and test actual behavior
   - Include both positive and negative test cases
   - Add appropriate assertions and error checking
   - Follow naming conventions and documentation standards

### Step 6: Validation and Final Report

After generating tests:

1. **Run the new tests**:
   ```bash
   # Run specific test files (adapt based on discovered test runner)
   [discovered_test_runner] [discovered_test_path]/test_new_feature.py -v
   
   # Run coverage analysis again (adapt based on discovered structure)
   make test-coverage
   # or: npm run test:coverage
   # or: pytest --cov=[discovered_source_path] --cov-report=html
   # or: dotnet test --collect:"XPlat Code Coverage"
   ```

2. **Verify coverage improvement**:
   - Check that coverage has increased to target levels
   - Ensure new tests are passing
   - Verify no regressions in existing tests

3. **Generate final report**:
   ```markdown
   ## Test Coverage Final Report
   
   ### Coverage Improvement
   - Before: 78% → After: 92% ✓
   - New tests added: 15
   - Critical gaps addressed: 3/3 ✓
   
### Tests Generated
- `[discovered_test_path]/unit/test_new_module.py` - 8 new test cases
- `[discovered_test_path]/integration/test_api_endpoints.py` - 4 new test cases
- `[discovered_test_path]/unit/test_error_handling.py` - 3 new test cases

## .NET Coverage Tools

### Common .NET Coverage Tools:
- **dotnet test --collect** - Built-in coverage collection
- **Coverlet** - Cross-platform coverage tool
- **ReportGenerator** - HTML report generation
- **Codecov** - Coverage reporting service

### .NET Coverage Commands:
```bash
# Basic coverage collection
dotnet test --collect:"XPlat Code Coverage"

# With specific coverage format
dotnet test --collect:"XPlat Code Coverage" --settings coverlet.runsettings

# Generate HTML report
dotnet tool install -g dotnet-reportgenerator-globaltool
reportgenerator -reports:"coverage.cobertura.xml" -targetdir:"coverage-report" -reporttypes:"Html"

# Coverage with specific projects
dotnet test MyProject.Tests.csproj --collect:"XPlat Code Coverage"
```
   
   ### Validation Results
   ✓ All new tests pass
   ✓ Coverage target achieved (92%)
   ✓ No regressions detected
   ✓ Test quality meets standards
   ```

## Working with Existing Context

If you were part of the implementation:
- Review the conversation history for what was implemented
- Check your todo list for completed work
- Focus coverage analysis on work done in this session
- Be thorough about testing new functionality

## Important Guidelines

1. **Be thorough but practical** - Focus on meaningful test coverage
2. **Prioritize critical paths** - Test functionality that matters most
3. **Follow existing patterns** - Use established test conventions
4. **Think about edge cases** - Don't just test happy paths
5. **Consider maintainability** - Write tests that are easy to understand and maintain

## Coverage Checklist

Always verify:
- [ ] Coverage meets 90% target for new/modified code
- [ ] Critical functionality is thoroughly tested
- [ ] Error conditions and edge cases are covered
- [ ] Integration tests exist for new features
- [ ] Tests follow project conventions
- [ ] All new tests pass
- [ ] No regressions in existing tests

## Tool Usage Guidelines

### Effective Tool Usage:
- Use codebase_search to find existing test patterns
- Use grep to find specific test functions and coverage markers
- Use read_file to analyze test files and understand structure
- Use run_terminal_cmd to execute coverage tools and test commands
- Run multiple tools in parallel when analyzing different aspects

### When to Use Each Tool:
- codebase_search: Finding test patterns and similar implementations
- grep: Finding specific test functions, coverage markers, or test imports
- read_file: Analyzing complete test files for structure and patterns
- run_terminal_cmd: Executing coverage tools, running tests, checking results
- todo_write: Tracking coverage analysis progress and test generation tasks

## Relationship to Other Commands

Recommended workflow:
1. `/implement_plan` - Execute the implementation
2. `/test_coverage` - Analyze and improve test coverage
3. `/validate_plan` - Verify implementation correctness
4. `/commit` - Create atomic commits for changes

The test coverage command works best after implementation is complete, as it can analyze the actual code changes and ensure comprehensive testing.

Remember: Good test coverage catches bugs before they reach production and makes refactoring safer. Focus on meaningful tests that verify actual behavior, not just line coverage.

