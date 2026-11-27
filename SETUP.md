# Arcane Systems Archive — v3 setup

## Install
1. Copy the contents of this folder into the root of the `Shade555` profile repository (the repository must be named `Shade555` for GitHub to render it as the profile README).
2. Keep the `assets/`, `scripts/`, and `.github/workflows/` folders beside `README.md`.
3. Commit and push the files to the default branch.
4. In **Settings → Actions → General**, allow GitHub Actions to create and approve pull requests / write repository contents, or ensure workflow permissions allow read and write access.
5. Run **Actions → Refresh the Arcane Observatory → Run workflow** once. The workflow also runs every 12 hours.

## Data sources
- GitHub: authenticated GitHub GraphQL API using the workflow's `GITHUB_TOKEN` / `GH_TOKEN`.
- LeetCode: public GraphQL profile endpoint for `shade555`. Public endpoint availability and schema can change; if it fails, the SVG shows an unavailable state instead of invented values.

## Notes
- The first commit includes custom-designed SVG artwork and honest “awaiting first observation” statistic panels. The workflow replaces those panels when it successfully retrieves data.
- GitHub profile README rendering does not support arbitrary HTML/CSS layouts. This implementation uses tables, images, and SVG assets for reliable rendering.
- SVG animation support can vary by client. The stained-glass panels use subtle SMIL shimmer; the rest of the design remains legible if animation is disabled.
- The profile banner uses `assets/banner.gif`, copied from the image supplied for this revision. The supplied GIF currently contains one frame, so it renders as a still banner; replace it with a multi-frame GIF whenever you have an animated export.
- Every SVG in `assets/` includes lightweight SMIL motion accents. GitHub and other SVG renderers may disable SMIL animation; the static artwork remains complete when motion is unsupported.
