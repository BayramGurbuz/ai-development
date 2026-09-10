import asyncio
import httpx

async def get_joke() -> str:
    async with httpx.AsyncClient() as client:
        response = await client.get("https://official-joke-api.appspot.com/random_joke")
        response.raise_for_status() # HTTP hatası varsa (404, 500 vb.) exception fırlatır
        data = response.json()
        return f"{data['setup']} - {data['punchline']}"


async def fetch_multiple_jokes(n: int = 3) -> list[str]:
    async with httpx.AsyncClient() as client:
        tasks = [client.get("https://official-joke-api.appspot.com/random_joke") for _ in range(n)]
        responses = await asyncio.gather(*tasks)  # hepsini AYNI ANDA bekler
        return [f"{r.json()['setup']} — {r.json()['punchline']}" for r in responses]

async def main():
    #joke = await get_joke()
    #print(joke)
    jokes = await fetch_multiple_jokes(5)
    for j in jokes:
        print(j)

if __name__ == "__main__":
    asyncio.run(main())