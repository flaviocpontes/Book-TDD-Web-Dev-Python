from playwright.sync_api import Page


def test_can_visit_the_site(page: Page):
    page.goto("http://localhost:8000")

    assert "To-Do" in page.title()
