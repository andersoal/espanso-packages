# Espanso Packages Repository Guidelines

## Package Manifest Versioning Rule

Whenever any modification, addition, or deletion is made to files within a package (such as `package.yml`, `_manifest.yml`, `README.md`, or any files within a package directory):

**You MUST update the package's `_manifest.yml` `version` field according to Semantic Versioning (`MAJOR.MINOR.PATCH`):**

1. **MAJOR version bump (`X.0.0`)**:
   - Apply when introducing breaking changes, removing triggers, renaming existing triggers, changing trigger behavior in a way that breaks existing user workflows/shortcuts, or major package structural overhauls.
   - Example: `1.4.2` -> `2.0.0`

2. **MINOR version bump (`X.Y.0`)**:
   - Apply when adding new triggers, adding new features, expanding templates with new functionality, or making backward-compatible enhancements.
   - Example: `1.4.2` -> `1.5.0` (reset patch to 0)

3. **PATCH version bump (`X.Y.Z`)**:
   - Apply for backward-compatible bug fixes, minor typo corrections, formatting tweaks, documentation fixes, or small prompt refinements.
   - Example: `1.4.2` -> `1.4.3`

### Instructions for Agent:
- Always locate `<package-name>/_manifest.yml`.
- Inspect the current `version`.
- Increment the appropriate **MAJOR**, **MINOR**, or **PATCH** version component.
- Ensure the `_manifest.yml` is updated as part of the same change / commit.
