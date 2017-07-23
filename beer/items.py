# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class BeerItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    style = Field()
    description = Field()
    image = Field()
    url = Field()
    min_color = Field()
    max_color = Field()  
    min_ibu = Field()
    max_ibu = Field()
    min_abv = Field()
    max_abv = Field()
    min_temp = Field()
    max_temp = Field()
    glassware = Field()
    examples = Field()
    pairings = Field()
    category = Field()
    
