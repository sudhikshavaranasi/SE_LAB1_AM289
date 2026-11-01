# Lab 5 — Static Code Analysis

## 1. Issues Identified and Fixed

| Issue | Tool | Description | Fix |
|---|---|---|---|
| Mutable default argument | Pylint | Shared mutable list used as default | Replaced with None |
| Global statement | Pylint | Function directly modified global variable | Used mutable revenue state |
| Bare exception | Pylint, Flake8, Bandit | Exception was silently ignored | Added explicit validation |
| Unsafe eval | Pylint, Bandit | Dynamically executed expression | Replaced with numeric calculation |
| Weak MD5 hash | Bandit | Weak hashing algorithm | Replaced with SHA-256 |
| Insecure random generator | Bandit | Standard random unsuitable for security-sensitive PINs | Used secrets module |
| Shell execution | Bandit | Shell command could introduce injection | Removed os.system |
| Hardcoded secret | Bandit | API secret embedded in source code | Used environment variable |
| Missing encoding | Pylint | File opened without encoding | Specified UTF-8 |
| Unused import and variables | Pylint, Flake8 | Unnecessary declarations | Removed unused declarations |
| Naming violations | Pylint | Functions used camelCase | Changed to snake_case |
| Formatting violations | Flake8 | Long lines and missing final newline | Reformatted source |

## 2. Reflection

### Q1. What is static code analysis?

Static code analysis examines source code without executing the program. It helps identify potential bugs, security vulnerabilities, and coding-style violations.

### Q2. What is the difference between Pylint, Bandit, and Flake8?

- Pylint checks code quality, naming conventions, programming practices, and potential logical problems.
- Bandit identifies common security vulnerabilities in Python programs.
- Flake8 checks formatting and compliance with Python style conventions.

### Q3. Which issue was most important to fix?

The use of eval() was particularly important because it could execute arbitrary expressions. Replacing it with numeric surcharge calculation made the program safer.

### Q4. How did static analysis improve the program?

It helped identify unsafe operations, weak hashing, insecure random generation, poor exception handling, unused variables, and formatting problems. Fixing these issues improved code quality, security, and maintainability.

### Q5. Why is static analysis useful in software development?

It helps developers identify problems early, before deployment. It also improves consistency, readability, maintainability, and security.

## 3. Conclusion

Static code analysis using Pylint, Bandit, and Flake8 helped identify and correct quality, security, and formatting issues in the flight reservation system. The corrected program was reanalysed to verify the improvements.