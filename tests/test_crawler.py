from __future__ import annotations

import requests

import crawler


class FakeResponse:
    def __init__(self, text: str, *, status_code: int = 200):
        self.text = text
        self.status_code = status_code

    def raise_for_status(self) -> None:
        if self.status_code >= 400:
            raise requests.HTTPError(f"{self.status_code} error")


class FakeSession:
    def __init__(self, responses):
        self.responses = list(responses)
        self.requested_urls: list[str] = []

    def get(self, url, timeout):
        self.requested_urls.append(url)
        response = self.responses.pop(0)
        if isinstance(response, Exception):
            raise response
        return response


def test_crawl_site_follows_next_links_and_respects_delay():
    first_page = """
    <html><head><title>Quotes page 1</title></head>
    <body><div class="quote">Good friends are valuable.</div>
    <li class="next"><a href="/page/2/">Next</a></li></body></html>
    """
    second_page = """
    <html><head><title>Quotes page 2</title></head>
    <body><div class="quote">Another quote.</div></body></html>
    """
    fake_session = FakeSession([FakeResponse(first_page), FakeResponse(second_page)])
    sleeps: list[float] = []

    pages = crawler.crawl_site(
        "https://quotes.toscrape.com/",
        delay_seconds=6,
        session=fake_session,
        sleep_func=sleeps.append,
    )

    assert [page.url for page in pages] == [
        "https://quotes.toscrape.com/",
        "https://quotes.toscrape.com/page/2/",
    ]
    assert pages[0].title == "Quotes page 1"
    assert "Good friends" in pages[0].text
    assert sleeps == [6]


def test_crawl_site_handles_request_failure_without_crashing(capsys):
    fake_session = FakeSession([requests.Timeout("timed out")])

    pages = crawler.crawl_site(
        "https://quotes.toscrape.com/",
        session=fake_session,
        sleep_func=lambda _seconds: None,
    )

    captured = capsys.readouterr()
    assert pages == []
    assert "Warning: failed to fetch" in captured.out


def test_extract_visible_text_ignores_script_content():
    title, text = crawler.extract_visible_text(
        "<html><head><title>Title</title><script>hidden()</script></head>"
        "<body><p>Visible words</p><style>.x{}</style></body></html>"
    )

    assert title == "Title"
    assert "Visible words" in text
    assert "hidden" not in text

