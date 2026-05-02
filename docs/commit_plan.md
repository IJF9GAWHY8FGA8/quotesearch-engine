# Recommended Commit Plan

Use these logical commits for the final Git history:

```bash
git add .gitignore requirements.txt pyproject.toml src/__init__.py
git commit -m "chore: set up Python search project"

git add src/crawler.py
git commit -m "feat: add polite quotes crawler"

git add src/indexer.py src/storage.py
git commit -m "feat: build and persist inverted index"

git add src/search.py src/main.py
git commit -m "feat: add required search CLI commands"

git add tests
git commit -m "test: cover crawler index search storage and CLI"

git add README.md docs
git commit -m "docs: add usage guide and assessment notes"

git add data/index.json
git commit -m "data: add compiled quote search index"
```

This history shows incremental development without pretending that the work was
done on separate days.
