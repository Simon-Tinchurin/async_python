import asyncio
import datetime
import colorama
import random
import time


def main():
    loop = asyncio.get_event_loop()

    t0 = datetime.datetime.now()
    print(colorama.Fore.YELLOW + 'App started.', flush=True)
    data = asyncio.Queue()

    task1 = loop.create_task(generate_data(20, data))
    task2 = loop.create_task(generate_data(20, data))
    task3 = loop.create_task(process_data(40, data))

    final_task = asyncio.gather(task1, task2, task3)
    loop.run_until_complete(final_task)

    dt = datetime.datetime.now() - t0
    print(colorama.Fore.WHITE + f'App exiting, total time: {dt.total_seconds()}')


async def generate_data(num: int, data: asyncio.Queue):
    for idx in range(1, num + 1):
        item = idx * idx
        await data.put((item, datetime.datetime.now()))

        print(colorama.Fore.YELLOW + f'-- generated {idx} item {item}', flush=True)
        await asyncio.sleep(random.random() + 0.5)


async def process_data(num: int, data: asyncio.Queue):
    processed = 0
    while processed < num:
        item = await data.get()
        processed += 1
        value = item[0]
        t = item[1]
        dt = datetime.datetime.now() - t
        print(colorama.Fore.CYAN + f'+++ Processed value {value} after {dt.total_seconds()} sec.')
        await asyncio.sleep(0.5)


if __name__ == '__main__':
    main()
