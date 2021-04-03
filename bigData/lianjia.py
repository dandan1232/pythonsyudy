import csv
import json
import requests
import re
from requests.exceptions import RequestException
from time import sleep


def get_one_page(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
    }
    try:
        response = requests.get(url, headers=headers)
        response.encoding = 'utf-8'
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None


def parse_one_page(html):
    # pattern = re.compile('<p class="content__list--item--title twoline">.*?>(.*?)</a>.*?'
    #                          '<p class="content__list--item--des">.*?>(.*?)</a>-.*?target="_blank">.*?</a>'
    #                          '.*?<i>/</i>(.*?)<i>/</i>.*?<i>/</i>(.*?)<span class="hide">.*?<span class="content__list--item-price">'
    #                           '<em>(.*?)</em>.*?</span>', re.S)
    pattern = re.compile('<p class="content__title">(.*?)</p>.*?'
                         '<a target="_blank" href=".*?">(.*?)</a>'
                         '<li><span class="label">.*?</span>(.*?)</li>'
                         '<li class="floor"><span class="label">。*？</span><span class="">(.*?)</span></li>'
                         '<div class="content__aside--title"><span>(.*?)</span>', re.S)
    items = re.findall(pattern, html)
    for items in items:
        yield {
            '标题': items[0].strip(),
            '地区': items[1].strip(),
            '房屋类型': items[2].strip(),
            '朝向楼层': items[3].strip(),
            '价格（元/月）': items[4]
        }


def analyseHTML(html):
    for item in parse_one_page(html):
        print(item)
        write_to_file(item)


def getTotalPage(html):
    pattern = re.compile('<a href="/zufang/pg\d+/#contentList" data-page="\d+">(.*?)</a>', re.S)
    num = re.findall(pattern, html)
    return num


# 保存在csv格式
def write_to_file(content):
    with open('链家租房.csv', 'a')as csvfile:
        fieldnames = ['标题', '地区', '房屋类型', '朝向楼层', '价格（元/月）']
        writer = csv.Dicwriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        #      writer = csv.writer(csvfile)
        writer.writerow(content)
        csvfile.close()


def main():
    # url = 'https://bj.lianjia.com/zufang/pg' +str(offest)
    # 种子
    # url = https://www.lianjia.com/city/

    # 得到每个城市二手房的链接

    # for循环每个城市二手房链接，第一步
    url = 'https://jn.lianjia.com/zufang'
    html = get_one_page(url)
    # 解析第一页
    analyseHTML(html)
    # 得到总页数
    totalpage = getTotalPage(html)
    for num in range(0, totalpage):
        url = 'https://jn.lianjia.com/zufang/pg' + str(num) + '/#contentList'
        html = get_one_page(url)
        analyseHTML(html)


if __name__ == '__main__':
    sleep(1)
    main()

# import csv
# import re
# import requests
#
#
# class HouseReptile(object):
#
#     def __init__(self):
#         self.headers = {
#             "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"}
#         self.base_url = "https://jn.lianjia.com/ershoufang/pg"
#         self.pg = 0
#         print("初始化~")
#
#     def read_house(self, url):
#         print("读取数据")
#         response = requests.get(url, self.headers)
#         self.parse_house(response.text)
#
#     def parse_house(self, html):
#         print("开始解析数据")
#         # 详情页  标题  小区名  规格  楼层 发布时间  总价 单价
#         mate = re.compile(
#             '''<div class="title"><a class="" href="(.*?)".*?data-is_focus="" data-sl="">(.*?)</a>.*?data-el="region">(.*?)</a> (.*?)<.*?</span>(.*?)<.*?starIcon"></span>(.*?)<.*?<span>(\d+)</span>万.*?<span>(.*?)</span>''',
#             re.S)
#         house_list = mate.findall(html)
#         self.write_house(house_list)
#
#     def write_house(self, house_list):
#         for house in house_list:
#             with open("链接二手房.csv", "a", newline="", encoding="utf-8") as f:
#                 writer = csv.writer(f)
#                 house = [
#                     house[0].strip(),
#                     house[1].strip(),
#                     house[2].strip(),
#                     house[3].strip(),
#                     house[4].strip(),
#                     house[5].strip(),
#                     house[6].strip(),
#                     house[7].strip()
#                 ]
#                 writer.writerow(house)
#
#     def crawl_house(self, number):
#         if self.pg == 0:
#             with open("链接二手房.csv", "a", newline="", encoding="utf-8") as f:
#                 writer = csv.writer(f)
#                 writer.writerow([
#                     "房屋详情链接",
#                     "标题",
#                     "小区名",
#                     "规格",
#                     "楼层",
#                     "发布时间",
#                     "总价(万)",
#                     "单价"
#                 ])
#
#         for i in range(0, number):
#             self.pg += 1
#             url = self.base_url + str(self.pg)
#             print("开始爬取：", url)
#             self.read_house(url)
#
#
# if __name__ == "__main__":
#     house = HouseReptile()
#     house.crawl_house(3)
#
