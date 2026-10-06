# Setup

1. Create a public GitHub repository named exactly your GitHub username.
2. Edit `profile.json` with your real identity, links, and stack.
3. Put your photo at `assets/portrait.jpg` if you want the ASCII portrait.
4. Install dependencies and generate the portrait:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r scripts/requirements.txt
python scripts/prep_photo.py assets/portrait.jpg assets/source-prepped.png
python scripts/fetch_contributions.py
python scripts/generate_all.py
```

5. Replace the placeholders in `README.md`.
6. Commit and push.
7. In GitHub: Settings → Actions → General → Workflow permissions → Read and write permissions.
8. Run **Actions → Update profile artwork → Run workflow** once.

The workflow then refreshes the contribution graph daily. It uses GitHub's public contribution calendar, including the tooltip text for each day, so no personal access token is required. Square color follows the real count: a day with zero contributions stays empty.

If GitHub changes the contribution-calendar HTML, update the selectors in `scripts/fetch_contributions.py`.
