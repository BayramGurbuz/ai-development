from main import fetch_joke, fetch_multiple_jokes

async def test_fetch_joke_returns_nonempty_string():
    joke = await fetch_joke()
    assert isinstance(joke, str)
    assert len(joke) > 0
    assert "—" in joke  # setup ve punchline'ı ayıran karakter


async def test_fetch_multiple_jokes_returns_requested_count():
    jokes = await fetch_multiple_jokes(3)
    assert len(jokes) == 3
    assert all(isinstance(j, str) and len(j) > 0 for j in jokes)
