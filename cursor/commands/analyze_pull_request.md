# Analyze PR Comments

You are tasked with analyzing pull request comments and providing actionable suggestions for improvements. This command uses the GitHub CLI to fetch PR comments and provides intelligent analysis with user validation prompts.

## Initial Setup

When this command is invoked:

1. **Check for PR context**:
   - If a PR number is provided as parameter, use it directly
   - If no parameter, check if we're in a git repository with an open PR
   - If no PR context found, ask user to provide PR number or URL

2. **Determine analysis scope**:
   - Review comments (general PR comments)
   - Review inline comments (code-specific feedback)
   - Analyze both if available

## Process Steps

### Step 1: Gather PR Information

1. **Get PR details**:
   ```bash
   # Get PR information
   gh pr view [PR_NUMBER] --json number,title,body,author,state,headRefName,baseRefName
   
   # Get PR comments
   gh pr view [PR_NUMBER] --json comments --jq '.comments[] | {body: .body, author: .author.login, createdAt: .createdAt, url: .url}'
   
   # Get inline comments (reviews)
   gh pr view [PR_NUMBER] --json reviews --jq '.reviews[] | {body: .body, author: .author.login, state: .state, createdAt: .createdAt, comments: [.comments[] | {body: .body, path: .path, line: .line, author: .author.login}]}'
   ```

2. **Analyze comment patterns**:
   - Identify recurring themes
   - Categorize feedback types (bugs, improvements, questions, approvals)
   - Note critical vs. minor issues
   - Identify conflicting feedback

### Step 2: Generate Suggestions

1. **Categorize suggestions**:
   - **Critical Issues**: Bugs, security concerns, breaking changes
   - **Code Quality**: Performance, maintainability, best practices
   - **Documentation**: Missing docs, unclear comments
   - **Testing**: Missing tests, test improvements
   - **Architecture**: Design patterns, structure improvements

2. **Prioritize suggestions**:
   - High priority: Critical issues that must be addressed
   - Medium priority: Important improvements
   - Low priority: Nice-to-have enhancements

### Step 3: Present Analysis with Validation

Present findings in this format:

```
## PR Analysis Summary

**PR**: #[PR_NUMBER] - [PR_TITLE]
**Author**: [AUTHOR]
**Status**: [STATUS]

### Comment Summary
- **Total Comments**: [COUNT]
- **Reviewers**: [LIST]
- **Critical Issues**: [COUNT]
- **Suggestions**: [COUNT]

### Key Findings

#### Critical Issues (Must Address)
1. **[Issue Type]**: [Description]
   - **Comment**: "[Original comment]"
   - **Suggested Action**: [Specific action]
   - **Impact**: [Why this matters]

#### Code Quality Improvements
1. **[Improvement Type]**: [Description]
   - **Comment**: "[Original comment]"
   - **Suggested Action**: [Specific action]
   - **Benefit**: [Why this helps]

#### Other Suggestions
[Additional categorized suggestions]

### Recommended Actions

1. **[Priority] Action**: [Description]
2. **[Priority] Action**: [Description]
3. **[Priority] Action**: [Description]

---

**Would you like me to help implement any of these suggestions?**

Please select which suggestions you'd like to work on:
- [ ] Address critical issues
- [ ] Implement code quality improvements  
- [ ] Add missing documentation
- [ ] Improve test coverage
- [ ] Other: [specify]

Or type 'all' to work on all suggestions, or 'none' to skip.
```

### Step 4: Handle User Selection

After user selects suggestions:

1. **Confirm selection**:
   ```
   I'll help you implement the following suggestions:
   - [List selected items]
   
   I'll work through these systematically. Shall I proceed?
   ```

2. **Implement selected suggestions**:
   - Create todo list for tracking progress
   - Read relevant files first
   - Implement changes with clear explanations
   - Validate changes work correctly

## Tool Usage Guidelines

### Effective Tool Usage:
- Use `run_terminal_cmd` to execute `gh` commands for PR data
- Use `codebase_search` to understand code context for suggestions
- Use `read_file` to analyze specific files mentioned in comments
- Use `grep` to find patterns or specific code sections
- Use `todo_write` to track implementation progress

### When to Use Each Tool:
- `run_terminal_cmd`: Execute GitHub CLI commands to fetch PR data
- `codebase_search`: Understand codebase structure and find relevant files
- `read_file`: Analyze specific files mentioned in PR comments
- `grep`: Find specific code patterns or implementations
- `todo_write`: Track which suggestions are being implemented

## Important Notes

- **Always validate with user**: Never implement changes without explicit user approval
- **Prioritize critical issues**: Address bugs and security concerns first
- **Provide context**: Explain why each suggestion matters
- **Be specific**: Give concrete, actionable recommendations
- **Respect reviewer feedback**: Acknowledge and address reviewer concerns appropriately

## Example Usage

```bash
# Analyze specific PR
/analyze_pr 123

# Analyze current PR (if in PR branch)
/analyze_pr

# Analyze PR from URL
/analyze_pr https://github.com/owner/repo/pull/123
```

## Error Handling

If GitHub CLI is not available or PR cannot be accessed:
```
Error: GitHub CLI not available or PR access denied.

Please ensure:
1. GitHub CLI is installed: https://cli.github.com/
2. You're authenticated: `gh auth login`
3. You have access to the repository
4. PR number/URL is correct

Would you like me to help you set up GitHub CLI access?
```

