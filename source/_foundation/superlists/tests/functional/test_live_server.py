import urllib.request


def test_live_server_serves_home_page(live_server_url):
    with urllib.request.urlopen(live_server_url) as response:
        body = response.read().decode()
    assert "<h1>To-Do</h1>" in body
