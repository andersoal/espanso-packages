# Manifest Versioning Rule

## Mandatory Manifest Version Bump

On **every change** made to any package in this repository (e.g. creating, updating, or deleting triggers, configs, documentation, or package files):

1. **Locate `_manifest.yml`** in the target package's directory (`<package>/_manifest.yml`).
2. **Update the `version`** field according to Semantic Versioning (`MAJOR.MINOR.PATCH`):
   - **MAJOR bump (`X.0.0`)**: For breaking changes (trigger removals, changing shortcut trigger strings that break muscle memory, breaking schema or structural changes).
   - **MINOR bump (`X.Y.0`)**: For non-breaking feature additions (adding new triggers, introducing new templates or capabilities; resets patch to `0`).
   - **PATCH bump (`X.Y.Z`)**: For backward-compatible bug fixes, minor typo corrections, formatting tweaks, or documentation updates.
3. Always include the updated `_manifest.yml` in the same commit/change.
