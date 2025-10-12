# Documentation Organization Rules

## Date-Based Organization

- **All implementation docs must go in `docs/YYYY-MM-DD/` folders**
- **Create a new date folder for each day's documentation**
- **Never create documentation files in the project root** (except `README.md`)

---

## File Naming Convention

### Use Descriptive UPPERCASE Names

- ✅ `FEATURE_IMPLEMENTATION.md`
- ✅ `SERVICE_REFACTORING.md`
- ✅ `API_TESTING_GUIDE.md`
- ✅ `CLINIC_WORKFLOW_SUMMARY.md`
- ❌ `notes.md`
- ❌ `temp.md`
- ❌ `doc.md`
- ❌ `implementation.md` (too generic)

### Naming Guidelines

1. Use UPPERCASE with underscores
2. Be specific and descriptive
3. Include the topic/feature name
4. Include the document type (IMPLEMENTATION, GUIDE, SUMMARY, etc.)
5. Avoid generic names

---

## What Goes Where

### Dated Folders (`docs/YYYY-MM-DD/`)

Implementation documentation and status reports:

- ✅ Implementation summaries
- ✅ Status reports
- ✅ Feature guides
- ✅ API documentation
- ✅ Architecture decisions
- ✅ Migration guides
- ✅ Testing reports
- ✅ Refactoring documentation
- ✅ Configuration guides

### Features Folder (`docs/features/`)

Permanent feature specifications:

- ✅ Feature API specifications
- ✅ Endpoint documentation
- ✅ Request/response examples
- ✅ Feature workflows

### Docs Root (`docs/`)

High-level project documentation:

- ✅ User journey documents
- ✅ Technical requirement documents (TRDs)
- ✅ Feature specifications
- ✅ Project timelines
- ✅ System architecture overviews

### Project Root

Only essential files:

- ✅ `README.md` (main project readme)
- ✅ `.cursorrules` (Cursor AI rules)
- ❌ **NO other `.md` files**

---

## Example Structure

```
server/
├── README.md                          # Main project README
├── .cursorrules                       # Cursor AI rules (index)
│
├── rules/                             # Modular rule files
│   ├── 01-database.md
│   ├── 02-architecture.md
│   ├── 03-service-layer.md
│   ├── 04-repository-layer.md
│   ├── 05-api-development.md
│   ├── 06-documentation.md
│   └── 07-doc-organization.md
│
└── docs/
    ├── DOCUMENTATION_ORGANIZATION.md  # Organization guide
    │
    ├── 2025-10-12/                   # Dated folder
    │   ├── README.md                 # Date-specific index
    │   ├── SERVICE_LAYER_REFACTORING_COMPLETE.md
    │   ├── CLINIC_WORKFLOW_IMPLEMENTATION.md
    │   ├── API_TESTING_GUIDE.md
    │   └── ENUM_CONVENTION.md
    │
    ├── 2025-10-13/                   # Next day's docs
    │   ├── README.md
    │   └── NEW_FEATURE_IMPLEMENTATION.md
    │
    ├── features/                      # Feature specs
    │   ├── authentication-api.md
    │   ├── pet-management-api.md
    │   └── clinic-workflow-api.md
    │
    ├── user_onboarding_trd_v2.md    # TRDs
    ├── first_vet_visit_journey.md    # User journeys
    └── existing_user_new_vet_journey.md
```

---

## Creating New Documentation

### Step 1: Create Date Folder

```bash
# Create today's folder (if it doesn't exist)
mkdir -p docs/$(date +%Y-%m-%d)
```

### Step 2: Create Documentation File

```bash
# Create the documentation file with descriptive name
touch docs/$(date +%Y-%m-%d)/MY_FEATURE_IMPLEMENTATION.md
```

### Step 3: Add Content with Template

```markdown
# Feature/Implementation Name

**Date**: YYYY-MM-DD
**Status**: ✅ Complete / 🔄 In Progress / ⏳ Planned
**Author**: [Optional]

## Summary

Brief overview of what was implemented or documented.

## Problem

What problem does this solve? What was the motivation?

## Solution

How was it solved? What approach was taken?

## Changes Made

List of files/components modified:
- `app/services/my_service.py` - Added new method
- `app/routes/my_routes.py` - Added new endpoint
- `app/models/my_model.py` - Added new fields

## Usage

How to use the new feature or implementation:

```python
# Example code
```

## Testing

How to test the implementation:

```bash
# Test commands
```

## Related Documentation

- Link to related docs
- Link to issues/tickets
- Link to API specs
```

---

## Documentation Types

### Implementation Summary

Document a completed implementation:
- What was built
- Why it was built
- How it works
- How to use it
- Testing approach

**Example**: `SERVICE_LAYER_REFACTORING_COMPLETE.md`

### Status Report

Track progress of ongoing work:
- Current status
- What's complete
- What's pending
- Blockers
- Next steps

**Example**: `IMPLEMENTATION_STATUS.md`

### Feature Guide

Explain how to use a feature:
- Feature overview
- Use cases
- Step-by-step guide
- Examples
- Troubleshooting

**Example**: `CLINIC_WORKFLOW_GUIDE.md`

### API Documentation

Document API endpoints:
- Endpoint list
- Request/response schemas
- Authentication
- Examples with curl
- Error codes

**Example**: `API_TESTING_GUIDE.md`

### Architecture Decision

Document significant decisions:
- Decision context
- Options considered
- Decision made
- Rationale
- Consequences

**Example**: `REPOSITORY_PATTERN_DECISION.md`

### Migration Guide

Guide for breaking changes:
- What changed
- Why it changed
- Migration steps
- Before/after examples
- Rollback procedure

**Example**: `MIGRATION_STATUS_TO_STRING.md`

---

## Date Folder README

Each dated folder should have a `README.md` index:

```markdown
# Documentation Archive - [Month Day, Year]

This folder contains all implementation documentation created on [date].

## Files in This Archive

### Category 1
- `FILE_1.md` - Brief description
- `FILE_2.md` - Brief description

### Category 2
- `FILE_3.md` - Brief description

## Related Documentation

Links to related docs in other folders or dates.

---

**Archive Date**: YYYY-MM-DD
**Total Documents**: X
**Status**: ✅ Organized and Archived
```

---

## Best Practices

### DO

- ✅ Create documentation as you work
- ✅ Use descriptive file names
- ✅ Include examples and code snippets
- ✅ Link to related documentation
- ✅ Add a README to each dated folder
- ✅ Keep documentation up to date
- ✅ Document breaking changes clearly

### DON'T

- ❌ Don't create docs in the project root
- ❌ Don't use generic file names
- ❌ Don't forget to date your documentation
- ❌ Don't leave documentation incomplete
- ❌ Don't duplicate information across files
- ❌ Don't forget to update the date folder README

---

## Finding Documentation

### By Date

```bash
# List all docs from a specific date
ls -1 docs/2025-10-12/

# View the date-specific index
cat docs/2025-10-12/README.md
```

### By Topic

```bash
# Search for specific topic across all docs
grep -r "service layer" docs/

# Find files with specific keyword in name
find docs/ -name "*CLINIC*"
```

### By Content

```bash
# Search all documentation for specific content
grep -r "repository pattern" docs/

# Search with context (5 lines before and after)
grep -r -A 5 -B 5 "Session injection" docs/
```

---

## Maintenance

### Weekly

- Review documentation for accuracy
- Update links if files moved
- Archive obsolete documentation

### Monthly

- Consolidate related documentation
- Update README files in dated folders
- Create summary documents if needed

### Quarterly

- Review old documentation for relevance
- Archive very old documentation
- Update main DOCUMENTATION_ORGANIZATION.md guide

---

## Automation Ideas

### Future Enhancements

- [ ] Script to create today's folder automatically
- [ ] Template generator for common doc types
- [ ] Link checker to find broken internal links
- [ ] Search tool for documentation
- [ ] Coverage metrics (docs per feature)

---

## Benefits of This System

1. **Clean Project Root**
   - Only essential files in root
   - Easy to find core documentation
   - Professional appearance

2. **Chronological History**
   - Track project evolution over time
   - See what was implemented when
   - Historical context preserved

3. **Easy Discovery**
   - Quick date-based search
   - Categorized in folder READMEs
   - Searchable across all docs

4. **Scalability**
   - No limit to documentation growth
   - New folders created as needed
   - Self-organizing system

5. **AI-Friendly**
   - Clear rules for Cursor AI
   - Consistent structure
   - Automated compliance

---

## Compliance

This documentation organization system is **mandatory** for all new documentation.

Cursor AI will enforce these rules based on the `.cursorrules` configuration.

**Last Updated**: October 12, 2025

