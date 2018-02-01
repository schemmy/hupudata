import scrapy
import re
from bs4 import BeautifulSoup

from hupudata.items import HupudataItem


FILT = ['虎扑用户','的兴趣','更多']


class HupudataSpider(scrapy.Spider):

    name = 'hupu'
    MAX_COUNT = 100000
    count = 0
    # def __init__(self):

    def start_requests(self):
        urls = [
            'https://my.hupu.com/176192780288726',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):

        if (self.count >= self.MAX_COUNT):
            return

        item = HupudataItem()
        # try:
        item['user'] = response.url.split('/')[-1]
        item['name'] = response.xpath('//div[@class="left"]/text()')[0].extract()

        teams_link = response.xpath('//span[@itemprop="affiliation"]/a/@href').extract()
        if len(teams_link) == 0:
            return 
        teams = [i.split('/')[-1] for i in teams_link]
        item['fav_teams'] = '_'.join(teams)

        personal = response.xpath('//div[@class="personalinfo"]').extract()[0].split()
        idx = [i for i, s in enumerate(personal) if '社区等级' in s]
        value = personal[idx[0]].split('</span>')[1]
        item['level'] = re.sub('[^0-9]', '', value)
        idx = [i for i, s in enumerate(personal) if '在线' in s]
        value = personal[idx[0]].split('</span>')[1]
        item['active'] = re.sub('[^0-9]', '', value)
        idx = [i for i, s in enumerate(personal) if '加入' in s]
        value = personal[idx[0]].split('</span>')[1]
        item['since'] = value
        self.count += 1
        yield item

        follow = response.css('div#following.indexfriend')[0].css('a::attr(href)').extract()
        follow_link = [i for i in follow if i.startswith('http')]

        # print (follow_link)
        for url in follow_link:
            yield scrapy.Request(url, callback=self.parse)

        # except Exception:
        #     pass



    # def parse(self, response):

    #     item = HupudataItem()
    #     try:
    #         item['user'] = response.url.split('/')[-1]

    #         interest = response.css('div.brief')[0].extract()
    #         words = re.findall('[\u4e00-\u9fff]+', interest)
    #         teams = [i for i in words if not any(j in i for j in FILT)]
    #         item['fav_teams'] = '_'.join(teams)
    #         self.count += 1
    #         yield item

    #         follow = response.css('div#following.indexfriend')[0].css('a::attr(href)').extract()
    #         follow_link = [i for i in follow if i.startswith('http')]

    #         # print (follow_link)
    #         # if (self.count < self.COUNT_MAX):
    #         for url in follow_link:
    #             yield scrapy.Request(url, callback=self.parse)

    #     except Exception:
    #         pass
