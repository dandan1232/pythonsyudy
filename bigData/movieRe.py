# admin: 蛋宝
# time:2020/12/15 14:11
# content:
import requests
from fake_useragent import UserAgent
from random import randint
from time import sleep
import re


def get_html(url):
    headers = {
        # "User-Agent": UserAgent().chrome
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
    }
    # sleep(randint(3, 10))
    response = requests.get(url, headers=headers)
    response.encoding = 'utf-8'
    if response.status_code == 200:
        return response.text
    else:
        return None


def parse_index(html):
    all_url = re.findall(
        r'<a href="(/films/\d+)" target="_blank" data-act="movies-click" data-val="{movieId:\d+}">.*</a>', html)
    return ['https://maoyan.com{}'.format(url) for url in all_url]


def parse_info(html):
    name = re.findall(r'<h1 class="name">(.+)</h1>', html)
    # types = re.findall(r'<li class="ellipsis">\s+<a class="text-link" href="/films?(catId=\d+)" target="_blank"> (.+) </a>', html)[0]
    # types = re.findall(r'<li class="ellipsis">\s+<a class="text-link".+>(.+)</a>\s+<a.+>(.+)</a>\s+</li>', html)[0]
    types = re.findall(r'<a class="text-link" href="/films\?catId=\d+"  target="_blank"> (.+) </a>', html)
    # types = re.findall(r'<li class="ellipsis">\s+<a class="text-link" href="/films.+>(.+)</a>', html)
    actors = re.findall(r'<li class="celebrity actor".+>\s+<a href="/films/cel.+>\s+<img.+>\s'
                        r'+</a>\s+<div.+>\s+<a.+>\s+(.+)\s+</a>', html)
    actors = format_actors(actors)
    return {
        "name": name,
        "types": types,
        "actors": actors
    }


def format_actors(actors):
    actor_set = set()
    for actor in actors:
        actor_set.add(actor)
    return actor_set


def main():
    index_url = 'https://maoyan.com/films'
    html = get_html(index_url)
    movie_urls = parse_index(html)
    print(movie_urls)
    for url in movie_urls:
        movie_html = get_html(url)
        movie = parse_info(movie_html)
        print(movie)


if __name__ == '__main__':
    main()
