# admin: 蛋宝
# time:2020/12/8 11:03
# content:
import json
from multiprocessing import Pool
import re
import requests
from requests.exceptions import RequestException
def get_one_page(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
    }
    try:
        response = requests.get(url, headers=headers)
        response.encoding= 'utf-8'
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None

def parse_one_page(html):
    pattern = re.compile('<dd>.*?board-index.*?>(\d+)</i>.*?data-src="(.*?)".*?name"><a'
                         +'.*?>(.*?)</a>.*?star">(.*?)</p>.*?releasetime">(.*?)</p>'
                         +'.*?integer">(.*?)</i>.*?fraction">(.*?)</i>.*?</dd>', re.S)
    items =re.findall(pattern,html)
    #print(items)
    for items in items:
        yield {
            'index': items[0],
            'image': items[1],
            'title': items[2],
            'actor': items[3].strip()[3:],
            'time': items[4].strip()[5:],
            'score': items[5]+items[6]
        }

def write_to_file(content):
    with open('Maoyantop100.txt', 'a', encoding='utf-8') as f:
        f.write(json.dumps(content, ensure_ascii=False) + '\n')
        f.close()

def main(offset):
    url = 'http://maoyan.com/board/4?offset=' + str(offset)
    html = get_one_page(url)
   # print(html)
    #parse_one_page(html)
    for item in parse_one_page(html):
        print(item)
        write_to_file(item)

if __name__ ==  '__main__':
    for i in range(10):
        main(i*10)
    pool = Pool()
    pool.map(main, [i*10 for i in range(10)])


