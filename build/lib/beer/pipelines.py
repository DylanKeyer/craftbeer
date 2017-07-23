# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
from scrapy.conf import settings
from scrapy.exceptions import DropItem
import logging

class MongoPipeline(object):    
    def __init__(self):
        connection = pymongo.MongoClient(settings['MONGODB_URI'])
        
        self.db = connection[settings['MONGODB_DB']]

    def open_spider(self, spider):
        self.collection = self.db[settings['MONGODB_COLLECTIONS'][spider.collection]]
        if self.collection == 'styles':
            self.collection.create_index('styles', unique=True)
            logging.info('INDEX {} CREATED'.format(self.collection))


    def process_item(self, item, spider):
        valid = True
        for data in item:
            if not data:
                valid = False
                raise DropItem('Missing {0}!'.format(data))
        if valid:
            self.collection.update_one({'style': item['style']}, {'$set': dict(item)}, upsert=True)
            #logging.INFO("Beer added to MongoDB database!")
        return item
        
