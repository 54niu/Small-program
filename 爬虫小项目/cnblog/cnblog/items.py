# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CnblogItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class BokeItem(scrapy.Item):
    url = scrapy.Field()
    title = scrapy.Field()
    industry = scrapy.Field()
    content = scrapy.Field()
    auther = scrapy.Field()
    date_pub = scrapy.Field()
    recommand = scrapy.Field()
    read_num = scrapy.Field()
    common_num = scrapy.Field()
    img_url = scrapy.Field()  # 图片的url地址
    img_path = scrapy.Field()  # 本地图片的路径
    tag = scrapy.Field()  # 标签
    crawl_time = scrapy.Field()  # 抓取时间
