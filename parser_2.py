import requests
import bs4
from concurrent.futures import Future
# from concurrent.futures.thread import ThreadPoolExecutor as PoolExecutor
from concurrent.futures.process import ProcessPoolExecutor as PoolExecutor
import datetime
import multiprocessing


# Synchronous 3.084317
# with Future 0.709784
# with different processes 0.665417


def main():
    urls = [
        'https://talkpython.fm',
        'https://pythonbytes.fm',
        'https://google.com',
        'https://realpython.com',
        'https://training.talkpython.fm',
    ]
    t0 = datetime.datetime.now()
    work = []
    with PoolExecutor() as executor:

        for url in urls:
            # title = get_title(url)
            f: Future = executor.submit(get_title, url)
            work.append(f)
            # print(title, flush=True)
    for f in work:
        print(f.result())
    dt = datetime.datetime.now() - t0
    print(f'Done in {dt.total_seconds()}', flush=True)


def get_title(url: str) -> str:
    process = multiprocessing.current_process()
    print(f'Getting title from: '
          f'{url.replace("https://", "")}, PID: {process.pid}, ProcName: {process.name}', end='\n', flush=True)
    response = requests.get(url, headers={
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/113.0'})
    response.raise_for_status()
    html = response.text
    soup = bs4.BeautifulSoup(html, features='html.parser')
    tag: bs4.Tag = soup.select_one('h1')

    if not tag:
        return 'NONE'
    if not tag.text:
        a = tag.select_one('a')
        if a and a.text:
            return a.text
        elif a and 'title' in a.text:
            return a.attrs['title']
        else:
            return 'NONE'
    return tag.get_text(strip=True)


if __name__ == '__main__':
    main()
