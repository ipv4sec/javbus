# -*- coding: utf-8 -*-


import scrapy
import requests
import re
from pyquery import PyQuery as pq
from javbus.items import JavbusItem


class CdnbusSpider(scrapy.Spider):

    name = 'cdnbus'
    allowed_domains = ['www.busdmm.men']
    start_urls = ['https://www.busdmm.men/genre/hd/1']

    headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
            'referer': 'https://www.busdmm.men/'
    }

    def parse(self, response):
        movies = response.xpath('//a[@class="movie-box"]')
        for movie in movies:
            detail_url = movie.xpath('@href').extract()[0]
            yield scrapy.Request(detail_url, callback=self.parse_item, meta= {'name': detail_url[23:]})
        next_page = response.xpath('//*[@id="next"]/@href').extract_first()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)

    def parse_item(self, response):
        gid = re.search('(\d{11})(?=;)', response.text).group()
        magnet_request_url = 'https://www.busdmm.men/ajax/uncledatoolsbyajax.php?gid=' + gid + '&uc=0'
        res = requests.get(magnet_request_url, headers=self.headers)
        d = pq(res.text)
        for value in d("a").items():
            if value.attr("class") == "btn btn-mini-new btn-primary disabled":
                magnet = value.parent().children("a").attr("href")[:60]
                yield JavbusItem(name=response.meta['name'], magnet=magnet)

