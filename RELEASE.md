# Release guide

1. Bump version
- Edit `src/bt_recover/__version__.py` and set the new version (semantic versioning).
- Commit the change.

2. Push to main
- Create a PR and merge to `main`.
- This triggers Docker image publish to `ghcr.io/kevinobytes/bt-recover` (latest).

3. Tag a release
- Create and push a tag matching the version (e.g., `v1.2.3`).
- Tag push triggers:
  - Docker publish with the version tag and commit sha.
  - PyPI publish via trusted publishing.

4. Post-release
- Set GHCR package visibility to Public (one-time step in GitHub Packages, after first publish).
- Create a GitHub release from the tag and include release notes.

## Commands
```bash
# 1) bump version
$EDITOR src/bt_recover/__version__.py

git add -A
git commit -m "chore: bump version to x.y.z"

git push origin main  # or open a PR and merge it

# 3) tag
git tag -a vX.Y.Z -m "Release vX.Y.Z"
git push origin vX.Y.Z
```

Note: Ensure PyPI trusted publishing is configured for this repo in the PyPI project settings.
