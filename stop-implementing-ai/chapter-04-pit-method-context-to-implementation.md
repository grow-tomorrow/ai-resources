# 4 PIT™: Context to Implementation

## 4.2 Step 2 (Plan) – Research

### Example Prompt:
```
Research [topic/question] in this codebase:

1. Read any directly mentioned files FULLY first (tickets, docs, JSON files)
2. Break down the research question into specific areas to investigate
3. Use parallel tool calls to research comprehensively:
   - Use codebase_search to discover project structure and find relevant components
   - Use grep to find specific patterns and implementations
   - Use read_file to analyze key files and configuration
   - Run multiple searches in parallel when exploring different aspects
4. Wait for ALL tool calls to complete before synthesizing
5. Synthesize findings with specific file paths and line number references
6. Create a research document at `thoughts/shared/research/YYYY-MM-DD-ENG-XXXX-description.md`
7. Include concrete examples, architecture insights, and cross-component connections

Focus on finding actual code patterns and usage, not just definitions. Prioritize live codebase findings over historical documents.
```

## 4.3 Step 3 (Plan) – Create the Plan

### Example Prompt:
```
Create an implementation plan for [feature/bug/ticket]:

1. Read all context files FULLY (ticket, research docs, related plans)
2. Research the codebase using parallel tool calls to discover:
   - Current implementation patterns
   - Relevant files and modules
   - Integration points and dependencies
   - Similar features to model after
3. Ask focused questions only for items you cannot determine through code investigation
4. Break the work into small, sequential phases that is clear for an LLM to follow with:
   - Clear description of changes
   - Specific file paths and code references
   - Success criteria (separate automated vs manual verification)
   - Tests to generate for each phase (unit, integration, Postman if API)
   - Suggested manual testing steps for each phase
5. Use a Test-Driven Development (TDD) approach: for each phase, specify that tests should be written first, then implementation to make them pass
6. Ensure each phase includes generating necessary tests and manual testing suggestions as it progresses—don't defer testing to later phases
7. Write the plan to `thoughts/shared/plans/YYYY-MM-DD-ENG-XXXX-description.md`
8. Iterate based on feedback until the plan is complete and actionable

Be skeptical, thorough, and work iteratively. No open questions should remain in the final plan.
```

## 4.4 Step 4 (Plan) – Review via "Hats"

### Example Prompt:
```
Review @reference_implementation_plan wearing the [architect/senior developer/performance engineer/etc.] hat:

1. Read the entire plan and understand the full context
2. Adopt the perspective of your assigned role—think like that professional would
3. Critically evaluate the plan from this perspective, looking for:
   - Structural issues, dependencies, or design flaws
   - Maintainability and clarity concerns
   - Whether phases are broken down correctly
   - Missing considerations or edge cases
   - Opportunities for improvement
4. Provide specific, actionable feedback with explanations
5. Suggest concrete improvements or alternatives where appropriate

Use reflection to critique the plan from this specialized viewpoint. The goal is to catch issues before implementation begins.
```

## 4.5 Step 5 (Implement) – Build in Phases

### Example Prompt:
```
Implement phase [N] of @reference_implementation_plan:

1. Read the plan completely and check existing checkmarks
2. Read all files mentioned in the phase fully (never use limit/offset)
3. Create a todo list to track progress
4. Implement the phase fully before moving to the next
5. Verify success criteria (usually `make check test` or equivalent)
6. Update checkboxes in the plan as you complete sections
7. If something doesn't match the plan, STOP and clearly explain:
   - What the plan expected
   - What you found
   - Why this matters
   - How to proceed

Follow the plan's intent while adapting to what you find in the codebase.
```

## 4.6 Step 6 (Implement) – Validate the Build

### Example Prompt:
```
Validate that this implementation matches the original plan:
- Check that all phases marked complete are actually done
- Verify automated tests pass
- Ensure code follows existing patterns
- Confirm no regressions were introduced
- Validate error handling is robust
- Check that documentation was updated if needed

Provide a validation report with:
- Implementation status for each phase
- Automated verification results
- Any deviations from the plan
- Potential issues identified
- Manual testing steps required
```

## 4.7 Step 7 (Test) – Validate Testing

### Example Prompt:
```
Run tests to validate the implementation:

1. Discover project structure and identify test framework
2. Run the full test suite to ensure all tests pass
3. If tests fail, analyze failures and identify root causes
4. For APIs, include Postman/shell script validation
5. Report test results with pass/fail status and any issues

Focus on validating that all tests generated during implementation phases are passing.
```

### Example Prompt:
```
Analyze test coverage for the feature that was just built:

1. Identify files/modules that were changed for this feature
2. Run coverage analysis for those specific files
3. Check if coverage meets target (90% or higher)
4. Identify any coverage gaps in the feature code
5. Generate a coverage report showing what's covered and what's not

Focus only on the feature that was implemented, not the entire codebase. If coverage gaps exist, generate additional tests to close them.
```

## 4.8 Step 8 (Test) – Human Validation

### Example Prompt:
```
Validate that the implementation matches @reference_implementation_plan:

1. Read the implementation plan completely
2. For each phase marked complete, verify the actual code matches:
   - Check that all planned files were modified/created
   - Run automated verification commands (build, test, lint)
   - Verify success criteria were met (automated and manual)
3. Identify any deviations from the plan:
   - What matches the plan exactly
   - What differs from the plan (and whether it's an improvement or issue)
   - Any missing functionality or incomplete phases
4. Check for potential issues:
   - Error handling and edge cases
   - Performance considerations
   - Regressions in existing functionality
5. Generate a validation report with:
   - Implementation status for each phase
   - Automated verification results
   - Deviations and potential issues
   - Manual testing steps required

Be thorough but practical. Focus on what matters for ensuring the implementation solves the original problem.
```

