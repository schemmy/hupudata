# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exceptions import DropItem
import csv
import pickle


class HupudataPipeline(object):

    def __init__(self):
        self.file = open('hupu.csv','w') 

    def process_item(self, item, spider):

        self.file.write(item['user'] + ',' +
                        item['name'] + ',' +
                        item['fav_teams'] + ',' +
                        item['level'] + ',' +
                        item['active'] + ',' +
                        item['since'] + '\n'
                        )
        return item

    def spider_closed(self, spider):
        self.file.close()




class DuplicatesPipeline(object):

    def __init__(self):
        self.ids_seen = set()

    def process_item(self, item, spider):
        if item['user'] in self.ids_seen:
            raise DropItem("Duplicate item found: %s" % item)
        else:
            self.ids_seen.add(item['user'])
            return item


    def spider_closed(self, spider):
        with open('set.pickle', 'wb') as handle:
            pickle.dump(self.ids_seen, handle, protocol=pickle.HIGHEST_PROTOCOL)

