from superlists import app


async def test_home_page_returns_html():
    client = app.test_client()
    response = await client.get("/")
    assert response.status_code == 200
    assert "<h1>To-Do</h1>" in await response.get_data(as_text=True)
