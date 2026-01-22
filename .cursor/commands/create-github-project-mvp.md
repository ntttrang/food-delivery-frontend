# create-github-project-mvp

Create EPICs, User Stories (US), and Tasks for the Online Food Ordering System MVP GitHub Project with proper parent-child relationships base on the MVP_Sprint_Plan_with_Review.md file.

## Requirements

- **EPICs**: Top-level issues (11 total)
- **User Stories**: Sub-issues of EPICs (48 total) - linked using GitHub sub-issues API
- **Tasks**: Sub-issues of Sprint issues (195 total) - linked using GitHub sub-issues API
- **Sprints**: Create Sprint issues first (Sprint 0-8), then Tasks as their sub-issues
- **GitHub Project**: Uses Scrum template
- **Relationships**:
  - US → EPIC (parent-child via `addSubIssue` mutation)
  - Tasks → Sprint (parent-child via `addSubIssue` mutation)

## Implementation

Use gh command to create the project and issues.
