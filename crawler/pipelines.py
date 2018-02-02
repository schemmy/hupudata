# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exceptions import DropItem
import csv,codecs
import pickle



class HupuZhuanquPipeline(object):

    def open_spider(self, spider):
        filename = 'data/' + spider.dom + '.csv'
        self.f = codecs.open(filename, 'w', 'utf_8_sig') 
        self.writer = csv.writer(self.f) 

    def process_item(self, item, spider):

        line = [item['poster'],
                item['userId'], 
                item['name'], 
                item['url']
                ]
        self.writer.writerow(line)
        return item

    def close_spider(self, spider):
        self.f.close()



class HupudataPipeline(object):

    def __init__(self):
        self.file = open('data/hupu2.csv','a') 
        # self.file.write('user, fav_teams, level, active, since\n')

    def process_item(self, item, spider):

        line = [item['user'], 
                #item['name'], 
                item['fav_teams'], item['level'], item['active'],item['since']]
        newline = ','.join(line) + '\n'
        self.file.write(newline)
        return item

    def close_spider(self, spider):
        self.file.close()


class DuplicatesPipeline(object):

    def __init__(self):
        try:
            pickle_in = open('data/set2.pkl','rb')
            self.ids_seen = pickle.load(pickle_in)
        except Exception:
            self.ids_seen = set()

    def open_spider(self, spider):
        pass

    def process_item(self, item, spider):
        if item['user'] in self.ids_seen:
            raise DropItem("Duplicate item found: %s" % item)
        else:
            self.ids_seen.add(item['user'])
            return item

    def close_spider(self, spider):
        with open('data/set.pkl', 'wb') as handle:
            pickle.dump(self.ids_seen, handle, protocol=pickle.HIGHEST_PROTOCOL)

