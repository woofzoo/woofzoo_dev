# WoofZoo Server - Coding Rules

This directory contains modular coding rules and best practices for the WoofZoo server project.

---

## Rule Files

### [01-database.md](01-database.md) - Database & Models
- Enum handling (never create database ENUMs)
- Migration guidelines
- String columns for enum-like fields

### [02-architecture.md](02-architecture.md) - Architecture & Code Organization
- Clean architecture principles
- Layer responsibilities (models → repositories → services → controllers → routes)
- Dependency injection
- Separation of concerns

### [03-service-layer.md](03-service-layer.md) - Service Layer Rules
- **NEVER inject `Session` into services**
- Service responsibilities
- Business logic patterns
- Testing services

### [04-repository-layer.md](04-repository-layer.md) - Repository Layer Rules
- BaseRepository usage
- Domain-specific query methods
- Repository patterns
- What belongs in repositories

### [05-api-development.md](05-api-development.md) - API Development & Security
- Role-based access control (RBAC)
- Input validation with Pydantic
- Error handling
- Logging security actions
- Security best practices

### [06-documentation.md](06-documentation.md) - Code Documentation Standards
- Function docstrings
- Schema documentation
- Inline comments
- API route documentation
- Module-level documentation

### [07-doc-organization.md](07-doc-organization.md) - Documentation Organization
- Date-based folder structure (`docs/YYYY-MM-DD/`)
- File naming conventions
- What goes where
- Creating new documentation

---

## Quick Reference

### Most Important Rules

1. **Never inject `Session` into services** ([03-service-layer.md](03-service-layer.md))
   - Services only call repository methods
   - All database access through repositories

2. **Never create database ENUMs** ([01-database.md](01-database.md))
   - Store enums as strings (`String(50)`)
   - Define enums in Python code only

3. **All docs go in dated folders** ([07-doc-organization.md](07-doc-organization.md))
   - Create `docs/YYYY-MM-DD/` folders
   - Use UPPERCASE file names
   - Never create docs in project root

4. **Follow clean architecture** ([02-architecture.md](02-architecture.md))
   - Don't bypass layers
   - Keep business logic in services
   - Controllers handle HTTP only

5. **Enforce RBAC at route level** ([05-api-development.md](05-api-development.md))
   - Use FastAPI dependencies
   - Role checks in route signatures
   - Log security actions

---

## Rule Categories

### 🗄️ Database & Data Access
- [01-database.md](01-database.md) - Database conventions
- [04-repository-layer.md](04-repository-layer.md) - Data access layer

### 🏗️ Architecture & Structure
- [02-architecture.md](02-architecture.md) - Overall architecture
- [03-service-layer.md](03-service-layer.md) - Business logic layer

### 🔐 API & Security
- [05-api-development.md](05-api-development.md) - API development and security

### 📝 Documentation
- [06-documentation.md](06-documentation.md) - Code documentation
- [07-doc-organization.md](07-doc-organization.md) - File organization

---

## How to Use These Rules

### For Developers

1. **Read relevant rules before starting work**
   - Working on services? Read [03-service-layer.md](03-service-layer.md)
   - Creating APIs? Read [05-api-development.md](05-api-development.md)
   - Adding docs? Read [07-doc-organization.md](07-doc-organization.md)

2. **Reference during code reviews**
   - Check if code follows architecture rules
   - Verify database conventions
   - Ensure documentation is complete

3. **Update rules when patterns evolve**
   - Submit PRs for rule improvements
   - Discuss architectural decisions
   - Keep rules current

### For Cursor AI

Cursor AI automatically reads these rules from `.cursorrules` and applies them when:
- Generating code
- Suggesting changes
- Creating documentation
- Refactoring code

---

## Finding Information

### By Topic

| Topic | File |
|-------|------|
| Enums | [01-database.md](01-database.md#enum-handling) |
| Session injection | [03-service-layer.md](03-service-layer.md#critical-rules) |
| RBAC | [05-api-development.md](05-api-development.md#role-based-access-control-rbac) |
| Docstrings | [06-documentation.md](06-documentation.md#function-documentation) |
| File naming | [07-doc-organization.md](07-doc-organization.md#file-naming-convention) |
| Repository patterns | [04-repository-layer.md](04-repository-layer.md#repository-patterns) |
| Clean architecture | [02-architecture.md](02-architecture.md#clean-architecture) |

### Search All Rules

```bash
# Search for specific topic
grep -r "Session" rules/

# Find examples
grep -r "```python" rules/

# List all rule files
ls -1 rules/*.md
```

---

## Rule File Structure

Each rule file follows this structure:

1. **Title and Overview**
2. **Critical Rules** (if applicable)
3. **Examples** (✅ Correct and ❌ Wrong)
4. **Detailed Guidelines**
5. **Patterns and Anti-Patterns**
6. **Best Practices**
7. **Testing** (if applicable)

---

## Benefits of Modular Rules

### ✅ Easier to Navigate
- Find specific rules quickly
- Focus on relevant topics
- Jump directly to examples

### ✅ Easier to Maintain
- Update one file at a time
- Clear ownership of topics
- Version control friendly

### ✅ Better Organization
- Logical grouping by topic
- Numbered for learning order
- Cross-references between files

### ✅ More Reusable
- Link to specific rule files
- Share relevant rules
- Reference in documentation

### ✅ Scalable
- Add new rule files as needed
- Split large files easily
- Keep files focused

---

## Contributing to Rules

### Adding New Rules

1. Determine which file the rule belongs to
2. Add the rule with examples
3. Update this README if needed
4. Submit PR with explanation

### Modifying Existing Rules

1. Update the relevant rule file
2. Add rationale for change
3. Update examples if needed
4. Submit PR with context

### Creating New Rule Files

1. Follow naming convention: `0X-topic.md`
2. Use existing files as template
3. Add to this README index
4. Update `.cursorrules` to reference it

---

## Maintenance

- **Review**: Monthly review of all rules
- **Updates**: Keep examples current with codebase
- **Cleanup**: Remove obsolete rules
- **Improve**: Add clarity based on feedback

---

## Quick Links

- [Main Project README](../README.md)
- [Documentation Organization](../docs/DOCUMENTATION_ORGANIZATION.md)
- [API Testing Guide](../docs/2025-10-12/API_TESTING_GUIDE.md)
- [Service Layer Refactoring](../docs/2025-10-12/SERVICE_LAYER_REFACTORING_COMPLETE.md)

---

**Last Updated**: October 12, 2025  
**Total Rule Files**: 7  
**Status**: ✅ Active and Enforced

