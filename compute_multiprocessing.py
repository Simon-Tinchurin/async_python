import datetime
import math
import multiprocessing


# first run Threaded in 6.52709 seconds
# first run Multiprocessing in 2.079365 seconds


def main():
    do_math(1)
    t0 = datetime.datetime.now()
    print(f'Doing math on {multiprocessing.cpu_count()} processors')
    processor_count = multiprocessing.cpu_count()
    pool = multiprocessing.Pool()
    for n in range(1, processor_count + 1):
        pool.apply_async(do_math, (30000000 * (n - 1) / processor_count,
                                   30000000 * n / processor_count))
    pool.close()
    pool.join()
    dt = datetime.datetime.now() - t0
    print(f'Done in {dt.total_seconds()}')


def do_math(start=0, num=10):
    pos = start
    k_sq = 1000 * 1000
    while pos < num:
        pos += 1
        math.sqrt((pos - k_sq) * (pos - k_sq))


if __name__ == '__main__':
    main()
