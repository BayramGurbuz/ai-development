from main import fetch_joke

async def test_fetch_joke_returns_nonempty_string():
    joke = await fetch_joke()
    assert isinstance(joke, str)
    assert len(joke) > 0
    assert "—" in joke  # setup ve punchline'ı ayıran karakter
