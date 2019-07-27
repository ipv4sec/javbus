# -*- coding: utf-8 -*-

import csv
import scrapy
from scrapy.exceptions import DropItem

class JavbusPipeline(object):

    def __init__(self, stats):
        self.stats = stats

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.stats)


    def open_spider(self, spider):
        with open('result.csv') as csvfile:
            csv_reader = csv.reader(csvfile)
            for row in csv_reader:
                if len(row) == 2:
                    self.stats.set_value(row[1], 1)

    def close_spider(self, spider):
        pass

    def process_item(self, item, spider):
        if item['name'] == 'name':
            return item
        if self.stats.get_value(item['name']) is not None:
            raise DropItem("movie passed %s" % self.stats.get_value(item['name']))
        return item
