import scrapy
import re
from bs4 import BeautifulSoup

from crawler.items import HupudataItem,HupuZhuanquItem


FILT = ['虎扑用户','的兴趣','更多']


class HupuZhuanquSpider(scrapy.Spider):

    name = 'zhuanqu'
    MAX_COUNT = 200000
    count = 0
    domain = 'https://bbs.hupu.com'
    min_page = 0
    max_page = 10
    def __init__(self, dom='', *args, **kwargs):
        self.dom = dom

    def start_requests(self):
        url = 'https://bbs.hupu.com/' + self.dom
        for i in range(self.max_page, self.min_page,-1):
            link = url + '-' + str(i)
            yield scrapy.Request(url=link, callback=self.parse)

    def parse(self, response):

        # if (self.count >= self.MAX_COUNT):
            # return

        if not response.url.split('/')[-1][0].isdigit():
            posts = response.xpath('//a[@class="truetit"]').css('a::attr(href)').extract()
            users_links = response.xpath('//a[@class="aulink"]/@href').extract()
            ids = [i.split('/')[-1] for i in users_links]
            names = response.xpath('//a[@class="aulink"]/text()').extract()
            replies = response.xpath('//span[@class="ansour box"]/text()').extract()
            
            for i in range(len(posts)):
                # fan = HupuZhuanquItem()
                # fan['userId'] = ids[i]
                # fan['name'] = names[i]
                # fan['poster'] = '1'
                # yield fan
                self.count += int(replies[i].split()[0])
                print (self.count)
                n_pages = (int(replies[i].split()[0]) - 1) // 20 + 1
                pts = posts[i].split('.')
                for j in range(n_pages):
                    url = self.domain + pts[0] + '-' + str(j+1) + '.' + pts[1]
                    yield scrapy.Request(url=url, callback=self.parse)
        else:
            ids = response.xpath('//div[@class="j_u"]/@uid').extract()
            names = response.xpath('//div[@class="j_u"]/@uname').extract()

            for i in range(len(ids)):
                fan = HupuZhuanquItem()
                fan['userId'] = ids[i]
                fan['name'] = names[i]
                fan['url'] = response.url.split('/')[-1].split('.')[0]
                if len(response.url.split('-')) == 1 and i == 0:
                    fan['poster'] = 'Y'
                else:
                    fan['poster'] = 'N'
                yield fan




class HupudataSpider(scrapy.Spider):

    name = 'hupu'
    MAX_COUNT = 200000
    count = 0
    # def __init__(self):
    try:
        pickle_in = open('data/set2.pkl','rb')
        seen = pickle.load(pickle_in)
    except Exception:
        seen = set()

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
        # item['name'] = response.xpath('//div[@class="left"]/text()')[0].extract()

        teams_link = response.xpath('//span[@itemprop="affiliation"]/a/@href').extract()
        if len(teams_link) == 0:
            return 
        teams = [i.split('/')[-1] for i in teams_link]
        item['fav_teams'] = '＋'.join(teams)

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
            next_user = url.split('/')[-1]
            if next_user not in self.seen:
                self.seen.add(next_user)
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
