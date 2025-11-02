# 9 Advanced: The TDD Comeback in AI-Powered Development

## 9.1 Why TDD is Making a Comeback

### The AI-TDD Synergy

### Example Prompt:
```
Create a TDD implementation plan for comprehensive unit tests for this user authentication service:

1. Read all context files FULLY (authentication service code, existing tests, API specifications, security requirements)
2. Research the codebase using parallel tool calls to discover:
   - Current authentication implementation patterns
   - Existing test structure and frameworks
   - Security requirements and validation rules
   - Similar test suites to model after
3. Ask focused questions only for items you cannot determine through code investigation
4. Break the work into small, sequential phases following TDD (test-first approach) with:
   - Clear description of test scenarios (success cases, failure cases, edge cases, security scenarios)
   - Specific file paths and code references
   - Success criteria (separate automated vs manual verification)
   - Tests to write FIRST for each phase (unit tests covering business logic, error conditions, security scenarios)
   - Implementation changes needed AFTER tests pass
   - Suggested manual testing steps for each phase
5. Use Test-Driven Development: for each phase, specify that tests must be written FIRST and fail, then implementation makes them pass
6. Ensure each phase includes generating comprehensive tests before implementation—don't defer testing to later phases
7. Write the plan to `thoughts/shared/plans/YYYY-MM-DD-authentication-service-tests.md`
8. Iterate based on feedback until the plan is complete and actionable

Be skeptical, thorough, and work iteratively. No open questions should remain in the final plan.
```

## 9.2 AI-Powered TDD: Faster, Smarter, More Reliable

### The Enhanced TDD Cycle

### Red Phase (Write Failing Test)

### Example Prompt:
```
Create a TDD implementation plan for a user registration API endpoint (Red Phase - failing tests first):

1. Read all context files FULLY (API specifications, existing endpoints, authentication patterns, rate limiting config)
2. Research the codebase using parallel tool calls to discover:
   - Current API endpoint patterns and structure
   - Existing test framework and utilities
   - Database schema and user model patterns
   - Rate limiting implementation approach
   - Input validation patterns used elsewhere
3. Ask focused questions only for items you cannot determine through code investigation
4. Break the work into small, sequential phases following TDD (test-first approach) with:
   - Clear description of test scenarios for each phase:
     * Successful registration with valid data
     * Rejection of duplicate emails
     * Password strength validation
     * Input sanitization
     * Rate limiting behavior
   - Specific file paths and code references
   - Success criteria (separate automated vs manual verification)
   - Failing tests to write FIRST for each phase (tests that fail until implementation exists)
   - Implementation changes needed AFTER tests are written
   - Suggested manual testing steps for each phase
5. Use Test-Driven Development: for each phase, specify that failing tests must be written FIRST, then implementation makes them pass
6. Ensure each phase includes writing failing tests before any implementation—don't defer testing to later phases
7. Write the plan to `thoughts/shared/plans/YYYY-MM-DD-user-registration-api.md`
8. Iterate based on feedback until the plan is complete and actionable

Be skeptical, thorough, and work iteratively. No open questions should remain in the final plan.
```

### Green Phase (Make Tests Pass)

### Example Prompt:
```
Implement phase [N] of @reference_implementation_plan for the user registration service:

1. Read the plan completely and check existing checkmarks
2. Read all files mentioned in the phase fully (never use limit/offset)
3. Create a todo list to track progress
4. Implement the phase fully to make the failing tests pass:
   - Focus on making tests green, not perfect architecture
   - Follow the plan's intent while adapting to what you find in the codebase
   - Implement incrementally if the phase is large
5. Verify success criteria (run tests to confirm they pass: `make test` or equivalent)
6. Update checkboxes in the plan as you complete sections
7. If something doesn't match the plan, STOP and clearly explain:
   - What the plan expected
   - What you found
   - Why this matters
   - How to proceed

Follow the plan's intent while adapting to what you find. The goal is green tests, then we can refactor.
```

### Refactor Phase (Improve Code)

### Example Prompt:
```
Create a refactoring implementation plan for improving readability and maintainability:

1. Read all context files FULLY (code to refactor, existing tests, related files, refactoring constraints)
2. Research the codebase using parallel tool calls to discover:
   - Current code structure and dependencies
   - Existing refactoring patterns and conventions
   - All test files that cover this code
   - Integration points and dependencies
   - Similar refactored code examples
3. Ask focused questions only for items you cannot determine through code investigation
4. Break the refactoring into small, sequential phases with:
   - Clear description of changes (readability improvements, maintainability enhancements)
   - Specific file paths and code references
   - Success criteria (separate automated vs manual verification):
     * All existing tests continue to pass
     * No functionality changes (behavior-preserving refactor)
     * Code quality improvements verified
   - Tests to run for each phase (full test suite to ensure nothing breaks)
   - Suggested manual verification steps for each phase
5. Use incremental refactoring: ensure each phase maintains test coverage and can be verified independently
6. Ensure each phase includes running all tests before and after changes—don't defer verification
7. Write the plan to `thoughts/shared/plans/YYYY-MM-DD-code-refactoring.md`
8. Iterate based on feedback until the plan is complete and actionable

Be skeptical, thorough, and work iteratively. The refactoring must be behavior-preserving—all tests must continue to pass. No open questions should remain in the final plan.
```

### Amplify Phase (Enhance Tests)

### Example Prompt:
```
Analyze test coverage and suggest improvements for these tests:

1. Read all test files and related implementation code FULLY (test files, source code being tested, existing test patterns)
2. Research the codebase using parallel tool calls to discover:
   - Current test coverage levels and gaps
   - Existing test patterns and conventions
   - Implementation code being tested
   - Similar test suites for reference
   - Error handling patterns in the code
3. Run test coverage analysis to identify:
   - Current coverage percentage (target: 90%+)
   - Specific functions/lines lacking coverage
   - Missing edge cases and error conditions
   - Critical paths that need more testing
4. Analyze test quality and identify gaps:
   - Missing error condition tests
   - Uncovered edge cases and boundary conditions
   - Integration scenarios not tested
   - Security and validation cases missing
5. Generate suggestions for additional test cases with:
   - Specific test scenarios (edge cases, error conditions, boundary tests)
   - Priority levels (critical, important, nice-to-have)
   - File paths and code references for where to add tests
   - Examples following existing test patterns
6. Provide actionable recommendations:
   - List of missing test cases with descriptions
   - Coverage improvement estimate
   - Test implementation suggestions

Focus on edge cases and error conditions that might have been missed. Be specific about what's missing and why it matters.
```

