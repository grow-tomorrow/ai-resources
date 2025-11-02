# 7 Cookbook: Four PIT™ Scenarios You Can Run Tomorrow

## 7.1 Backend Bug Fix: Stabilize Order Intake

### Example Prompt:
```
Create an implementation plan for fixing the order insertion bug in our Node.js API:
[Insert additional context based on chapter 4]

1. Read all context files FULLY (error logs, relevant code files, any related tickets)
2. Research the codebase using parallel tool calls to discover:
   - Current order insertion implementation patterns
   - Database schema and transaction handling
   - Error handling patterns used elsewhere
   - Similar bugs or fixes in the codebase
3. Ask focused questions only for items you cannot determine through code investigation
4. Break the work into small, sequential phases with:
   - Clear description of changes
   - Specific file paths and code references
   - Success criteria (separate automated vs manual verification)
   - Tests to generate for each phase (unit tests for error scenarios, integration tests for database operations)
   - Suggested manual testing steps for each phase
5. Use a Test-Driven Development (TDD) approach: for each phase, specify that tests should be written first, then implementation to make them pass
6. Ensure each phase includes generating necessary tests and manual testing suggestions—don't defer testing to later phases
7. Write the plan to `thoughts/shared/plans/YYYY-MM-DD-order-insertion-fix.md`
8. Iterate based on feedback until the plan is complete and actionable

Be skeptical, thorough, and work iteratively. No open questions should remain in the final plan. Wait for approval before generating code.
```

## 7.2 Frontend Unit Tests: Lock In Checkout Quality

### Example Prompt:
```
Create an implementation plan for adding comprehensive unit tests to our React checkout form:
[Insert additional context based on chapter 4 - component code, existing test patterns, testing framework setup]

1. Read all context files FULLY (checkout component code, existing test files, testing configuration, related components)
2. Research the codebase using parallel tool calls to discover:
   - Current testing patterns and conventions
   - Existing test utilities and helpers
   - Component dependencies and integration points
   - Similar components with comprehensive test coverage
3. Ask focused questions only for items you cannot determine through code investigation
4. Break the work into small, sequential phases with:
   - Clear description of changes (specific behaviors to test per phase)
   - Specific file paths and code references
   - Success criteria (separate automated vs manual verification)
   - Tests to generate for each phase (unit tests for validation, user interactions, state changes, error handling)
   - Suggested manual testing steps for each phase
5. Use a Test-Driven Development (TDD) approach: for each phase, specify that tests should be written first, then confirm code supports them
6. Ensure each phase includes generating necessary tests and manual testing suggestions—don't defer testing to later phases
7. Write the plan to `thoughts/shared/plans/YYYY-MM-DD-checkout-unit-tests.md`
8. Iterate based on feedback until the plan is complete and actionable

Be skeptical, thorough, and work iteratively. No open questions should remain in the final plan. Wait for approval before generating tests.
```

## 7.3 Feature Expansion: Add "Save for Later"

### Example Prompt:
```
Create an implementation plan for adding a "Save for Later" button to our product detail page:
[Insert additional context based on chapter 4 - product component code, wishlist API specification, existing button patterns, analytics setup]

1. Read all context files FULLY (product detail component, wishlist API documentation, existing button components, analytics patterns)
2. Research the codebase using parallel tool calls to discover:
   - Current wishlist API implementation (POST /api/wishlist/{productId})
   - Existing button component patterns
   - State management approaches used in similar features
   - Analytics tracking patterns
   - Similar feature implementations
3. Ask focused questions only for items you cannot determine through code investigation
4. Break the work into small, sequential phases with:
   - Clear description of changes (UI element, API integration, state management, analytics)
   - Specific file paths and code references
   - Success criteria (separate automated vs manual verification)
   - Tests to generate for each phase (component rendering tests, API call tests, state change tests, error handling tests)
   - Suggested manual testing steps for each phase
5. Use a Test-Driven Development (TDD) approach: for each phase, specify that tests should be written first, then implementation to make them pass
6. Ensure each phase includes generating necessary tests and manual testing suggestions—don't defer testing to later phases
7. Write the plan to `thoughts/shared/plans/YYYY-MM-DD-save-for-later-feature.md`
8. Iterate based on feedback until the plan is complete and actionable

Be skeptical, thorough, and work iteratively. No open questions should remain in the final plan. Wait for approval before generating code.
```

## 7.4 Greenfield Build: PTO Tracker MVP

### Example Prompt:
```
Create an implementation plan for building a Django PTO Manager project from scratch:
[Insert additional context based on chapter 4 - business requirements, authentication needs, reporting requirements, deployment constraints]

1. Read all context files FULLY (requirements document, existing Django patterns if applicable, deployment constraints, authentication requirements)
2. Research the codebase using parallel tool calls to discover:
   - Existing Django project structure and patterns (if extending an existing project)
   - Authentication and authorization patterns
   - Testing framework setup and conventions
   - Database migration patterns
   - Similar Django applications as reference
3. Ask focused questions only for items you cannot determine through code investigation
4. Break the work into small, sequential phases with:
   - Clear description of changes (project scaffolding, model definitions, migrations, CRUD views, admin interface, permissions, reporting)
   - Specific file paths and code references
   - Success criteria (separate automated vs manual verification)
   - Tests to generate for each phase (model tests, view tests, permission tests, integration tests)
   - Suggested manual testing steps for each phase
5. Use a Test-Driven Development (TDD) approach: for each phase, specify that tests should be written first, then implementation to make them pass
6. Ensure each phase includes generating necessary tests and manual testing suggestions—don't defer testing to later phases
7. Write the plan to `thoughts/shared/plans/YYYY-MM-DD-pto-manager-mvp.md`
8. Iterate based on feedback until the plan is complete and actionable

Be skeptical, thorough, and work iteratively. No open questions should remain in the final plan. Wait for approval before generating code for Phase 1.
```

## 7.5 Complex Codebase Navigation: Adding Features to Unfamiliar Systems

### Example Prompt:
```
Create an implementation plan for adding cancellation support to this Rust codebase:
[Insert additional context based on chapter 4 - workspace loaded, execution model requirements, cancellation requirements, backward compatibility needs]

1. Read all context files FULLY (codebase structure, execution model code, related modules, any existing cancellation patterns)
2. Research the codebase using parallel tool calls to discover:
   - Codebase structure and relevant modules
   - Current execution model implementation
   - Integration points for cancellation logic
   - Existing patterns for similar features (timeouts, interrupts, etc.)
   - Testing patterns and frameworks used
3. Create a research document at `thoughts/shared/research/YYYY-MM-DD-rust-cancellation-research.md` that documents findings
4. Ask focused questions only for items you cannot determine through code investigation
5. Break the work into small, sequential phases with:
   - Clear description of changes (cancellation token implementation, integration points, backward compatibility)
   - Specific file paths and code references
   - Success criteria (separate automated vs manual verification)
   - Tests to generate for each phase (unit tests for cancellation logic, integration tests for different execution contexts, backward compatibility tests)
   - Suggested manual testing steps for each phase
6. Use a Test-Driven Development (TDD) approach: for each phase, specify that tests should be written first, then implementation to make them pass
7. Ensure each phase includes generating necessary tests and manual testing suggestions—don't defer testing to later phases
8. Write the plan to `thoughts/shared/plans/YYYY-MM-DD-rust-cancellation-support.md`
9. Iterate based on feedback until the plan is complete and actionable

Be skeptical, thorough, and work iteratively. No open questions should remain in the final plan. Provide the research document first, then the implementation plan, then wait for approval before implementation.
```

