# 5-Minute Video Script

Keep the final recording under five minutes. Aim for about 4 minutes 40 seconds.

## 0:00-0:20 Project Introduction

This is QuoteSearch Engine, a Python command-line search tool for
`quotes.toscrape.com`. It crawls the quote listing pages, builds an inverted
index, saves it as JSON, and supports `build`, `load`, `print`, and `find`.

## 0:20-2:00 Live Demonstration

Run:

```bash
python3 src/main.py build
python3 src/main.py load
python3 src/main.py print nonsense
python3 src/main.py find indifference
python3 src/main.py find good friends
python3 src/main.py find
python3 src/main.py find xyznotreal
python3 src/main.py find '!!!'
```

Say:

- `build` takes longer because the crawler deliberately waits six seconds
  between requests.
- `load` confirms the saved index can be retrieved.
- `print` shows the posting list for one word.
- `find` supports single-term and multi-term queries.
- The empty, missing, and special-character examples show boundary handling.

## 2:00-3:20 Code Walkthrough

Show these files:

- `src/crawler.py`: uses Requests and BeautifulSoup, follows pagination, catches
  request errors, and injects `sleep_func` so tests can verify politeness without
  actually waiting.
- `src/indexer.py`: tokenizes text to lower case and builds an inverted index
  with frequency and positions.
- `src/search.py`: searches for pages containing all query terms, checks phrase
  matches using positions, and ranks results.
- `src/storage.py`: saves and loads the compiled JSON index.
- `src/main.py`: provides the four required CLI commands.

Key design point:

The index stores positions as well as frequency. Frequency helps ranking, and
positions allow phrase-aware matching for queries like `good friends`.

## 3:20-3:50 Testing

Run:

```bash
python3 -m pytest --cov=src --cov-report=term-missing
```

Say:

The tests cover crawler behavior, indexing, search, storage, and CLI commands.
Network requests and sleep are mocked, so the tests are fast and reliable while
still verifying the six-second politeness logic.

## 3:50-4:15 Git History

Run:

```bash
git log --oneline --graph
```

Say:

The commits are split by responsibility: project setup, crawler, indexing,
search and CLI, tests, documentation, and compiled index.

## 4:15-4:45 GenAI Critical Evaluation

Say:

I used GenAI to help plan the project structure, think through edge cases, and
review the testing strategy. It was useful for identifying missing cases such as
empty queries, special characters, and invalid index files. However, I still had
to check the implementation manually. For example, the six-second politeness
window needed careful handling so that production code waits but tests do not
become slow. I validated the code by running tests, checking coverage, and
inspecting the generated index. I understand and can explain each module and the
trade-offs behind the data structure.

