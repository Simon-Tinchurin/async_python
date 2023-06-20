import asyncio
import aiohttp
import bs4
from colorama import Fore

# TODO 10.79


async def get_html(episode_number: int) -> str:
    print(Fore.YELLOW + f'Getting HTML for episode {episode_number}', flush=True)

    url = f'https://talkpython.fm/{episode_number}'

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            response.raise_for_status()
            return await response.text()


def get_title(html: str, episode_number: int) -> str:
    print(Fore.CYAN + f'Getting TITLE for episode {episode_number}', flush=True)
    soup = bs4.BeautifulSoup(html, 'html.parser')
    header = soup.select_one('h1')
    if not header:
        return 'MISSING'
    return header.text.strip()


def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(get_title_range())
    print("Done.")


async def get_title_range():
    tasks = []
    for n in range(10, 20):
        tasks.append((n, asyncio.create_task(get_html(n))))

    for n, t in tasks:
        html = await t
        title = get_title(html, n)
        print(Fore.WHITE + f'Title found: {title}', flush=True)


if __name__ == '__main__':
    main()
