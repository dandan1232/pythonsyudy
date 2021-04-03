# import re
# import requests
# from requests.exceptions import RequestException
#
# def get_one_page(url):
#     headers = {
#         "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
#     }
#     try:
#         response = requests.get(url, headers=headers)
#         response.encoding = 'utf-8'
#         if response.status_code == 200:
#             return response.text
#         return None
#     except RequestException:
#         return None
#
# def parse_index(html):
#     all_url = re.findall(r'<h3 class="listTit">.*?href="(.*?)".*?</a></h3>', html)
#     return ['https://nj.5i5j.com{}'.format(url) for url in all_url]
#
# def parse_one_page(html):
#     pattern = re.compile('<div class="listCon"><h3 class="listTit">.*?tarcegio_bi.*?>(.*?)</a>.*?'
#                          +'<i class="i_01"></i>(.*?)</p>.*?'
#                          +'i_02"></li>(.*?)<a href="/xiaoqu/\d+.html">(.*?)</a>(.*?).*?nofollow">(.*?)</a>.*?'
#                          +'i_03"></li>(.*?)</p>.*?redC"><strong>(\d+)</strong>(.*?)</p>.*?</div>', re.S)
#     #title = re.findall(r'<h1 class="house-tit">(.+)</h1>', html)
#     items = re.findall(pattern, html)
#     print(items)
#     # return {
#     #     '房源标题': title
#     #
#     # }
#
# def main():
#     index_url = 'https://nj.5i5j.com/zufang/'
#     html = get_one_page(index_url)
#     house_urls = parse_index(html)
#     print(house_urls)
#     for url in house_urls:
#         house_html = get_one_page(url)
#         house = parse_one_page(house_html)
#         print(house)
#
#
#
# if __name__ == '__main__':
#     main()

from random import random

import requests
import re
import json
import time
from urllib3 import *

# 得到单个页面的HTML代码
def getOnePage(url):
    session = requests.session()

    try:
        headers = {
            'Connection': 'keep-alive',
            'Accept': '*/*',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
        }
        # 发送请求（包含请求头）
        response = session.get(url, headers=headers)
        print(response.status_code)
        # 获取html代码
        data = response.text
        if response.status_code == 200:
            return data
        return None
    except Exception:
        return None



# 在所有房源信息的页面上，爬取所有的/zufang/44930753.html，项目根目录https://nj.5i5j.com
def getAllHref(html):
    # 使用正则表达式分析HTML代码
    # print(html)
    pattern = re.compile('<div class="listImg".*?<a href="(.*?)".*?</div>', re.S)
    return re.findall(pattern, html)




# 分析页面，如果是多个返回用yield，单个数据返回用return
def parseOnePage(html):
    # print(html)
    # 使用正则表达式分析HTML代码
    # rs.S是指“.”的作用扩展到整个字符串，包括\n,"."默认只针对一行有效
    # pattern = re.compile('<div class="details-view clear rent-detail">.*?<p class="de-price"><span>(.*?)</span>.*?'
		# + '<span class="yafu.*?</i>(.*?)</span>.*?<p class="houseinfor1">(.*?)</p>.*?>(.*?)</p>.*?'
		# + '<p class="houseinfor1">(.*?)<span>.*?<p class=houseinfor1>(.*?)</p>.*?houseinfor2">(.*?)</p>', re.S)
    pattern = re.compile('<div class="details-view clear rent-detail">.*?<p class="de-price"><span>(.*?)</span>.*?'	# 1.价格
	    +'<div class="jlyoubai fl jlyoubai1" >.*?<p class="houseinfor1">(.*?)</p>.*?'				# 2.房型
	    +'<div class="jlyoubai fl jlyoubai2" >.*?<p class="houseinfor1">(.*?)<span>.*?'			# 3.面积
	    +'<div class="jlyoubai fl jlyoubai3" >.*?<p class="houseinfor2">(.*?)</p>.*?'         # 4.建造时间
	    +'<div class="zushous">.*?<li.*?target="_blank">(.*?)</a></shd>.*?"elementname_var":"(.*?)",.*?"elementnametwo_var":"(.*?)"', re.S)
    items = re.search(pattern, html)
    # 当只有列表只有一个字符串元数时，遍历foreac遍历为字符串
    # print(items)
        # 将函数变成一个Generator,可以进行迭代
    return {
        '价格': items.group(1),
        '房型': items.group(2),
        '面积': items.group(3),
        '建造时间': items.group(4),
        '房源地址': str(items.group(6))+','+str(items.group(7))+','+str(items.group(5))
    }

# 保存抓取的数据
def save(content):
    with open('D:\\board.txt','a', encoding='utf-8') as f:
        # 将JSON对象转换成字符串，ensure_ascii为False,表示返回的值可以包含非ASCII字符
        f.write(json.dumps(content, ensure_ascii=False) + '\n')



# 根据偏移量，进行爬取
def getBoard(offset):
    url = 'https://nj.5i5j.com/zufang/n' + str(offset) + '/'
    # 得到网页的源码
    html = getOnePage(url)
    # 获得所有的a标签的href
    list = getAllHref(html)
    # print(list)
    for item in list:
        url = 'https://nj.5i5j.com'+str(item)
        print(url)
        # 获取具体房子信息的源码
        html = getOnePage(url)
        # print(html)

        print(json.dumps(parseOnePage(html), ensure_ascii=False))
        save(parseOnePage(html))
        time.sleep(1)

# 处理4页
for i in range(0,4):
    getBoard(i+1)


# test
# html = getOnePage('https://nj.5i5j.com/zufang/44604798.html')
# data = parseOnePage(html)
# print(json.dumps(data, ensure_ascii=False))