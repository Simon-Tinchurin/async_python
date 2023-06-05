import aiohttp
import asyncio
from unsync import unsync
import requests
import math
import datetime


# 1.556708 seconds


def main():
    t0 = datetime.datetime.now()

    tasks = [
        compute_some(),
        compute_some(),
        compute_some(),
        download_some(),
        download_some(),
        download_some_more(),
        download_some_more(),
        wait_some(),
        wait_some(),
        wait_some(),
        wait_some(),
    ]

    [t.result() for t in tasks]

    dt = datetime.datetime.now() - t0
    print(f'Asynchronous version done in {dt.total_seconds()} seconds')


@unsync(cpu_bound=True)
def compute_some():
    print('Computing...')
    for _ in range(1, 10_000_000):
        math.sqrt(25 ** 25 + .01)


@unsync()
async def download_some():
    print('Downloading...')
    url = 'https://talkpython.fm/episodes/show/174/coming-into-python-from-another-industry-part-2'
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
        async with session.get(url) as resp:
            resp.raise_for_status()
            text = await resp.text()
            print(f'Downloaded {len(text)} characters')


@unsync()
def download_some_more():
    print('Downloading more...')
    url = 'https://talkpython.fm/episodes/show/387/build-all-the-things-with-pants-build-system '
    resp = requests.get(url)
    resp.raise_for_status()
    text = resp.text
    print(f'Downloaded more {len(text)} characters')


@unsync()
async def wait_some():
    print('Waiting...')
    for _ in range(1, 1000):
        await asyncio.sleep(.001)


if __name__ == '__main__':
    main()
