# admin: 蛋宝
# time:2020/04/02 16:41
# content:
import json
from multiprocessing import Pool
import re
import requests
from requests.exceptions import RequestException


# 得到指定一个URL的网页内容
def get_one_page(url):  # 模拟浏览器头部信息，向豆瓣服务器发送消息
    head = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
    }
    try:
        response = requests.get(url, headers=head)
        response.encoding = 'utf-8'
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None


def parse_one_page(baseurl):
    # 逐一解析数据
    pattern = re.compile(
        '<div class="item">.*?>(\d+)</em>.*?<span class="title">(.*?)</span>.*?<div class="bd">.*?>(.*?)</p>.*?</div>',
        re.S)
    item = re.findall(pattern, baseurl)
    # print(type(item))
    # print(item)
    for item in item:
        yield {
            '序号：': item[0].strip(),
            '电影名': item[1].strip(),
            '人员': item[2].strip()[3:]
        }


# 写入scv
def write_to_file(content):
    with open('豆瓣TOP250', 'a', encoding='utf-8') as f:
        f.write(json.dumps(content, ensure_ascii=False) + "\n")
        f.close()


# 保存数据
def main(start):
    url = 'https://movie.douban.com/top250?start=' + str(start)
    html = get_one_page(url)
    # print(html)
    for item in parse_one_page(html):
        print(item)
        write_to_file(item)


if __name__ == '__main__':
    for i in range(25):
        main(i * 25)
    pool = Pool()
    pool.map(main, [i * 25 for i in range(25)])
