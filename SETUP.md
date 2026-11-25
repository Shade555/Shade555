# Setup

1. Create a **public** repository named exactly `Shade555` (same as your GitHub username).
2. Put `README.md` at the repository root.
3. Add your uploaded city artwork to `assets/gothic-cyberpunk-banner.png`.
4. Copy `.github/workflows/update-metrics.yml` into the same path in that repository.
5. Open **Settings → Actions → General** and allow workflow read/write access to repository contents.
6. Run **Actions → Update Arcane Profile Metrics → Run workflow** once. It generates `assets/metrics.svg` and refreshes it daily.
7. To show the generated metrics panel, add this where you want it in README:
   `<img src="assets/metrics.svg" width="100%" alt="Live GitHub metrics"/>`

The README also embeds live third-party cards for GitHub stats, streak, activity graph, visitor count, skill icons, and LeetCode. Third-party services can rate-limit or change availability.

The LeetCode card currently assumes your LeetCode handle is `Shade555`. Replace that username in the `leetcard.jacoblin.cool` URL if your handle differs.
