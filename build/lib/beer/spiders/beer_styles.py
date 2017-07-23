# -*- coding: utf-8 -*-
from scrapy import Spider, Request
from scrapy.http import HtmlResponse
from scrapy.selector import Selector

from beer.items import BeerItem

import time

class BeerStylesSpider(Spider):
    name = 'beer-styles'
    allowed_domains = ['www.craftbeer.com']
    start_urls = ['http://www.craftbeer.com/beer-styles/']

    def __init__(self):
        self.collection = 'styles'
        self.table = 'styles'

    def parse(self, response):
#        styles = Selector(response).xpath('//*[@id="styles"]/li')
#        for style in styles: 
#            item['style'] = style.xpath(
#                    'h2/a/text()').extract()[0]
        urls = Selector(response).xpath('//*[@id="styles"]/li/h2/a/@href').extract()
        for url in urls:
            yield Request(url=url, callback=self.parse_more)
                                       
    def parse_more(self, response):
        item = BeerItem()
        
        item['style'] = Selector(response).xpath('//*[@class="entry-title"]/text()').extract()[0]
                        
        item['description'] = Selector(response).xpath('//*[@class="entry-content"]/p/text()').extract()[0]
            
        item['category'] = Selector(response).xpath('//*[@id="knowledge"]/h3/a/@data-title').extract()[0]
        
        color = Selector(response).xpath('//*[@id="srm"]/span/text()').extract()[0].replace('(Color)', '').strip()
        color = color.split('SRM')[0]
        try:
            item['min_color'] =  float(color.split('-')[0].strip())
            item['max_color'] = float(color.split('-')[1].strip())
        except:
            item['min_color'] = color.split('-')[0].strip()
            item['max_color'] = color.split('-')[1].strip()
        
        ibu = Selector(response).xpath('//*[@data-title="International Bitterness Units (IBU)"]/span/text()').extract()[0].replace('(Bitterness)', '').strip()
        ibu = ibu.split('IBU')[0]
        try:
            item['min_ibu'] = float(ibu.split('-')[0].strip())
            item['max_ibu'] = float(ibu.split('-')[1].strip())
        except:
            item['min_ibu'] = ibu.split('-')[0].strip()
            item['max_ibu'] = ibu.split('-')[1].strip()
        
        alcohol = Selector(response).xpath('//*[@data-title="Alcohol by Volume (ABV)"]/span/text()').extract()[0].replace('(Alcohol)', '').strip()
        alcohol = alcohol.split('ABV')[0]
        try:
            item['min_abv'] = float(alcohol.split('-')[0].replace('%','').strip())
            item['max_abv'] = float(alcohol.split('-')[1].replace('%','').strip())
        except:
            item['min_abv'] = alcohol.split('-')[0].replace('%','').strip()
            item['max_abv'] = alcohol.split('-')[1].replace('%','').strip()
                
        pairings = Selector(response).xpath('//*[@id="pairings"]/ul/li/text()').extract()
        
        item['pairings'] = {}
        for ct, pairing in enumerate(pairings):
            item['pairings'][str(ct)] = pairing
            
        item['glassware'] = Selector(response).xpath('//*[@class="glass"]/text()').extract()[0]
        
        try:
            item['min_temp'] = float(alcohol.split('-')[0].replace('°F','').strip())
            item['max_temp'] = float(alcohol.split('-')[1].replace('°F','').strip())
        except:
            item['min_temp'] = alcohol.split('-')[0].replace('°F','').strip()
            item['max_temp'] = alcohol.split('-')[1].replace('°F','').strip()
            
        examples = Selector(response).xpath('//section[@id="winners"]/ul/li/text()').extract()
        
        item['examples'] = {}
        for ct, example in enumerate(examples):
            item['examples'][str(ct)] = example
            
        
            
        yield item