# -*- coding: utf-8 -*-

import csv
import scrapy

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
                print(row)
                self.stats.set_value(row[1], 1)

    def close_spider(self, spider):
        pass

    def process_item(self, item, spider):
        # print('Alreday Has Done')
        # if item == 'magnet,name':
        #     return item
        # print(self.stats)
        # print(item[85:-2])
        # print(self.stats.get_value(item[85:-2]))
        # if self.stats.get_value(item[85:-2]) is None:
        #     print('Alreday Has Done')
        #     print(self.stats.get_value(item[85:-2]))
        #     scrapy.spiders.crawl.CrawlSpider.close(spider, "Alreday Has Done")
        return item