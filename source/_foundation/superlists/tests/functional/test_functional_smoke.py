from playwright.sync_api import Page


def test_home_page_title(page: Page):
    page.goto("/")
    assert page.title() == "To-Do lists"
