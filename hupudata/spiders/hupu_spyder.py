import scrapy
import re
from bs4 import BeautifulSoup


FILT = ['的兴趣','更多']


class QuotesSpider(scrapy.Spider):
    name = "users"

    def __init__(self):
        self.visited = []
        self.nv = 0
        file = open('teams.txt', 'wb')

    def start_requests(self):
        urls = [
            'https://my.hupu.com/SmithKobe',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):

        try:
            username = response.url.split("/")[-1]

            if username not in self.visited:
                self.visited.append(username)
                self.nv += 1
                interest = response.css('div.brief')[0].extract()
                words = re.findall('[\u4e00-\u9fff]+', interest)
                teams = [i for i in words if not any(j in i for j in FILT)]
                print (self.nv, teams)
                file.write(','.join(teams))
                file.write('\n')

                follow = response.css('div#following.indexfriend')[0]
                follow = follow.css('a::attr(href)').extract()
                follow_link = [i for i in follow if i.startswith('http')]

                # print (follow_link)
                for url in follow_link:
                    yield scrapy.Request(url, callback=self.parse)
        except Exception:
            pass


        # z = wrap.css('div.contain')
        # print (response.url.split("/"))
        # filename = '%s.html' % username
        # with open(filename, 'wb') as f:
        #     f.write(response.body)
        # self.log('Saved file %s' % filename)