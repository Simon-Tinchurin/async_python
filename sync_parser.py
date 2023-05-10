import requests
import bs4
from colorama import Fore


def get_html(episode_number: int) -> str:
    print(Fore.YELLOW + f'Getting HTML for episode {episode_number}', flush=True)

    url = f'https://talkpython.fm/{episode_number}'
    response = requests.get(url)
    response.raise_for_status()
    return response.text


def get_title(html: str, episode_number: int) -> str:
    print(Fore.CYAN + f'Getting TITLE for episode {episode_number}', flush=True)
    soup = bs4.BeautifulSoup(html, 'html.parser')
    header = soup.select_one('h1')
    if not header:
        return 'MISSING'
    return header.text.strip()


def main():
    get_title_range()
    print("Done.")


def get_title_range():
    for n in range(10, 20):
        html = get_html(n)
        title = get_title(html, n)
        print(Fore.WHITE+ f'Title found: {title}', flush=True)


if __name__ == '__main__':
    main()