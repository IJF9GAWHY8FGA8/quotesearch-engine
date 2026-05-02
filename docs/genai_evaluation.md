# GenAI Critical Evaluation

This coursework is in the Green Category, so GenAI can be used if it is declared
and critically evaluated.

## Tools Used

GenAI was used as a development assistant to:

- plan a clear project structure
- identify edge cases from the coursework brief
- suggest testing categories
- review how the video should cover the marking criteria

## How It Helped

GenAI helped turn the coursework brief into an implementation checklist. This was
useful because the assessment is not only about code. It also includes tests,
Git practice, the compiled index file, a video demonstration, and a critical
evaluation. GenAI also helped identify edge cases such as empty queries,
special-character input, missing index files, damaged JSON files, and network
request failures.

## Limitations and Corrections

GenAI suggestions still needed checking. The crawler design needed manual
attention because the coursework requires a six-second politeness window. A
simple implementation could make the tests wait for a long time, so the final
code injects a `sleep_func`. Production code uses `time.sleep`, while tests pass
a fake function to verify the delay without slowing the test suite.

The indexing and search logic also needed validation. It was not enough to build
a dictionary of words to pages. The final implementation stores both frequency
and positions so that multi-word queries can be ranked more intelligently.

## Impact on Learning

GenAI saved time in planning and helped reduce the chance of missing assessment
requirements. However, it did not replace understanding the code. The final work
was validated through unit tests, CLI tests, coverage reporting, and a real build
against the target website. The most useful learning came from explaining why an
inverted index is appropriate, why positions are stored, and how crawler tests
can verify politeness without making live network requests.

## Academic Integrity Statement

All GenAI use should be declared in the video and any required submission notes.
The submitted code should only be included if the student can explain its
purpose, behavior, and design trade-offs.

