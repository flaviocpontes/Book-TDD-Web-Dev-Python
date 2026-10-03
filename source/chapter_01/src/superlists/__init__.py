from quart import Quart

app = Quart(__name__)


@app.get("/")
async def home_page():
    return "<html><title>To-Do lists</title><h1>To-Do</h1></html>"
