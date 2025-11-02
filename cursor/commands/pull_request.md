# Create Pull Request

You are tasked with creating a pull request for the changes made during this session.

## Process:

1. **Gather information:**
   - Review the conversation history and understand what was accomplished
   - Run `git status` to see current changes
   - Run `git diff` to understand the modifications
   - Get the current branch name with `git branch --show-current`
   - Check if there's a JIRA ticket in the branch name
   - Reference any rules in `.cursor/rules/pull-request-summary.mdc` if applicable, but instructions in this file take precedence

2. **Create the PR summary:**
   - Write the PR summary to `./.scratch/pull-request/{jira-issue-key}-{short-description}.md`
   - Follow the template structure from `./github/pull_request_template.md`
   - Include all required sections: Overview, What this does, Notes, Demo/Screenshots, Testing Instructions
   - Use kebab-case for the filename short description
   - Always include the AI attribution line in italics at the end of the Overview section

3. **Present your plan to the user:**
   - Show the proposed filename for the PR summary
   - Display the complete PR summary content
   - Ask: "I plan to create this pull request summary. Shall I proceed?"

4. **Execute upon confirmation:**
   - Create the PR summary file in the `.plans` directory
   - Show the result with `ls -la .plans/` to confirm the file was created

## Required PR Summary Structure:

1. **Overview Section**
   - Brief description of the changes
   - Include: "*Code was written by {AI Agent} using {Model Name}.*" at the end (in italics)
   - Add Closes []() with JIRA ticket link if applicable
   - JIRA URL structure: https://whcc.atlassian.net/browse/{JIRA_TICKET_ID}

2. **What this does**
   - Bullet-pointed list of changes
   - Be specific about what was modified/added/removed

3. **Notes** (Optional)
   - Ancillary topics, caveats, alternative strategies
   - Implementation decisions and rationale
   - Backwards compatibility notes

4. **Demo / Screenshots** (Optional)
   - How to see the changes in action
   - Specific URLs or steps to reproduce

5. **Testing Instructions**
   - Specific testing steps for the feature
   - Browser testing requirements (Chrome, Safari, Firefox)
   - Mobile testing requirements
   - Unit/integration test commands
   - Include any relevant environment variables (e.g., `DESIGN_GRID_VNEXT_ENABLED=true`)

## Important:
- **NEVER add co-author information or Claude attribution in git commits**
- The AI attribution goes in the PR summary, not in git commits
- Do not include any "Generated with Claude" messages in git commits
- Write commit messages as if the user wrote them
- The PR summary should be comprehensive and helpful for reviewers
- Make sure that `./scratch` directory is in the `.gitignore` file
- Make sure that `./scratch/pull-request` directory is created

## Remember:
- You have the full context of what was done in this session
- The PR summary should be detailed enough for reviewers to understand the changes
- Include specific testing instructions and environment variables
- Always include the AI attribution line in the Overview section
- The user trusts your judgment - they asked you to create the PR summary

