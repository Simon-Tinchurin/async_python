import datetime
import colorama
import random
import time
import threading


def main():
    t0 = datetime.datetime.now()
    print(colorama.Fore.YELLOW + 'App started.', flush=True)

    data = []

    threads = [
        threading.Thread(target=generate_data, args=(20, data), daemon=True),
        threading.Thread(target=generate_data, args=(20, data), daemon=True),
        threading.Thread(target=process_data, args=(40, data), daemon=True)
    ]
    abort_thread = threading.Thread(target=check_cancel, daemon=True)
    abort_thread.start()

    [t.start() for t in threads]
    while any([t.is_alive() for t in threads]):
        [t.join(0.01) for t in threads]
        if not abort_thread.is_alive():
            print('Cancelling on your request...', flush=True)
            break
    dt = datetime.datetime.now() - t0
    print(colorama.Fore.WHITE + f'App exiting, total time: {dt.total_seconds()}')


def generate_data(num: int, data: list):
    for idx in range(1, num + 1):
        item = idx * idx
        data.append((item, datetime.datetime.now()))

        print(colorama.Fore.YELLOW + f'-- generated {idx} item {item}', flush=True)
        time.sleep(random.random() + 0.5)


def check_cancel():
    print(colorama.Fore.RED + 'Press enter to cancel...', flush=True)
    input()


def process_data(num: int, data: list):
    processed = 0
    while processed < num:
        item = data.pop()
        processed += 1
        value = item[0]
        t = item[1]
        dt = datetime.datetime.now() - t
        print(colorama.Fore.CYAN + f'+++ Processed value {value} after {dt.total_seconds()} sec.')
        time.sleep(0.5)


if __name__ == '__main__':
    main()
