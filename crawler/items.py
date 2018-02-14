# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class HupudataItem(scrapy.Item):
    # define the fields for your item here like:
    user = scrapy.Field()
    # name = scrapy.Field()
    fav_teams = scrapy.Field()
    level = scrapy.Field()
    active = scrapy.Field()
    since = scrapy.Field()

    

class HupuZhuanquItem(scrapy.Item):
    # define the fields for your item here like:
    userId = scrapy.Field()
    name = scrapy.Field()
    poster = scrapy.Field()
    url = scrapy.Field()
    time = scrapy.Field()
