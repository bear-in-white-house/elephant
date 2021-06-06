import gevent
from gevent import monkey
monkey.patch_all()

import requests
import itertools


KEY_WORLD = '彩票'
URL_LIST = []


class CrawlLotteryWebsite:

    @staticmethod
    def generate_website():
        selected_str = '10ab6c9def2ghij4klm3no5pq8rst7uvwxyz'
        for length in range(3, 10):
            yield itertools.permutations(selected_str, length)

    def urls(self):
        for permutation in self.generate_website():
            for url in permutation:
                url = ''.join(url)
                yield f'http://{url}.com'


def send_request(url_generator):
    while True:
        try:
            url = next(url_generator)
        except StopIteration:
            break
        try:
            res = requests.get(url, timeout=(2, 2))
        except Exception as e:
            continue
        parse_rep(res.text, url)


def write_and_send_file():
    with open('./result.txt') as f:
        f.write('\n'.join(URL_LIST))

    url = 'https://api.telegram.org/bot711166180:AAErNuMGY5LU72YP7ZeOBwH53jRKSp5NeXY/sendDocument'
    files = {"document": open('./result.txt')}
    data = {'chat_id': -398945112}
    URL_LIST.clear()
    requests.post(url, data=data, files=files)


def parse_rep(rsp, url):
    if KEY_WORLD in rsp:
        URL_LIST.append(url)
    if len(URL_LIST) >= 50000:
        write_and_send_file()


if __name__ == '__main__':
    craw = CrawlLotteryWebsite()
    urls = craw.urls()
    g_list = []
    for i in range(1000):
        g = gevent.spawn(send_request, urls)
        g_list.append(g)
    gevent.joinall(g_list)
