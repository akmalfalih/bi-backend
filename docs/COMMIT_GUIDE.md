# 🧾 Commit Message Guidelines — APN Riau Backend

## 📘 Overview
We use the **Conventional Commit** format for consistency and clarity.

A commit message consists of:
```
<type>(<scope>): <short summary>

[optional body]
[optional footer]
```

Example:
```
feat(middleware): add HTTP request logging with JWT username tracking
```

---

## 🧩 Commit Types

| Type | Description | Example |
|------|--------------|----------|
| **feat** | A new feature | `feat(auth): implement JWT authentication flow` |
| **fix** | A bug fix | `fix(database): resolve session rollback issue on commit` |
| **docs** | Documentation changes only | `docs(readme): add API usage examples for dashboard` |
| **style** | Code style (formatting, whitespace, missing semicolons, etc.) | `style(core): format config file according to PEP8` |
| **refactor** | Code change that neither fixes a bug nor adds a feature | `refactor(models): simplify user model relationships` |
| **perf** | Performance improvements | `perf(query): optimize dashboard summary aggregation` |
| **test** | Adding or updating tests | `test(auth): add token expiration unit tests` |
| **chore** | Maintenance tasks (dependencies, build, CI/CD, etc.) | `chore(deps): update FastAPI to 0.111.0` |
| **build** | Changes that affect the build system or dependencies | `build(docker): add Dockerfile for production deployment` |
| **ci** | Changes to CI/CD configuration | `ci(github): add workflow for pytest` |

---

## 🧠 Writing Good Commit Messages

### ✅ Summary line
- Use **present tense**: “add” not “added”
- Keep it **under 72 characters**
- Be **specific and action-oriented**

Example:
```
feat(dashboard): add summary and recent activities endpoints
```

---

### ✅ Body (optional)
Use the body to explain **why** the change was made, and what it impacts.

Example:
```
feat(middleware): add HTTP request logging with JWT username tracking

- Added FastAPI middleware to log all incoming HTTP requests
- Captures method, path, status code, duration, and client IP
- Extracts username from JWT token for authenticated users
- Logs stored in rotating file handler (logs/app.log)
```

---

### ✅ Footer (optional)
Use the footer for:
- Breaking changes
- Related issues

Example:
```
BREAKING CHANGE: removed deprecated /api/v1 prefix
Closes #42
```

---

## 🧪 Example Commit Flow

```bash
# Stage changes
git add app/main.py app/core/security.py

# Commit with message
git commit -m "feat(middleware): add HTTP request logging with JWT username tracking"
```

---

## 💡 Recommended Scopes

| Area | Scope Keyword | Example |
|-------|----------------|----------|
| Authentication | `auth` | `feat(auth): add refresh token support` |
| Dashboard | `dashboard` | `feat(dashboard): add dummy summary endpoint` |
| Middleware | `middleware` | `feat(middleware): add logging for all HTTP requests` |
| Database | `database` | `fix(database): resolve transaction rollback issue` |
| Config / Core | `core` | `chore(core): update app settings for production` |
| Models | `models` | `refactor(models): simplify user table relations` |
| Schemas | `schemas` | `style(schemas): add missing type hints` |

---

## ✨ Example Full Commit History

```
feat(auth): implement JWT authentication
feat(dashboard): add summary and activities endpoints
feat(middleware): add HTTP logging with JWT username tracking
fix(database): resolve session rollback issue
refactor(core): move settings to BaseSettings class
docs(readme): update setup instructions
```

---

## ✅ Summary
Follow this structure for clean, readable, and professional commit logs:
1. Use the correct type (feat, fix, chore, etc.)
2. Be specific in your summary
3. Use body text if the change is significant
4. Include scope to clarify where the change happened

> “Commit messages are your future self’s documentation.”
