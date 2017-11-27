# -*- coding: utf-8 -*-
import scrapy
from urllib import parse
from cnblog.items import BokeItem
import datetime
from scrapy.loader import ItemLoader

class BokeSpider(scrapy.Spider):
    name = 'boke'
    allowed_domains = ['cnblogs.com']
    start_urls = ['https://www.cnblogs.com/cate/python/1']

    # 解析列表页
    def parse(self, response):
        article_list = response.xpath('div[@class="post_item"]')
        for article in article_list:
            cnitem = BokeItem()
            item_loader = BokeItem(item=cnitem, selector=article)
            # 文章链接
            url = article.xpath('.//h3/a/@href').extract()[0]
            item_loader.add_xpath('url', '//h3/a/@href')
            # 文章标题
            title = article.xpath('title', './/h3/a/text()')
            # 获取文章简介
            item_loader.add_xpath('industry', './/p[@class="port_item_summary"]/text()')
            # 作者
            item_loader.add_xpath('auther', './/a[@class="lightblue"]/text()')
            # 获取文章发布日期
            item_loader.add_xpath('date_pub', './/div[@class="post_item_foot"]/text()')
            # 推荐数
            item_loader.add_xpath('recommand_num', './/span[@class="diggnum"]/text()')
            # 阅读数
            item_loader.add_xpath('read_num', './/span[@class="article_view"]/a/text()')
            # 评论数
            item_loader.add_xpath('common_num', './/span[@class="article_comment"]/a/text()')
            # 头像img_url
            item_loader.add_xpath('img_url', './/img[@class="pfs"]/@src')

            # 详情页请求加入队列
            yield scrapy.Request(url, callback=self.parse_detail, meta={'item_loader': item_loader})

        # 获取下一页链接
        next_url = response.xpath('//div[@class="pager"]/a/@href').extract()[-1]
        next_url = parse.urljoin(response.url, next_url)

        # 加入请求队列
        yield scrapy.Request(next_url,callback=self.parse)

    def parse_detail(self, response):
        item_loader = response.meta['item_loader']
        selecter = response.xpath('/*')
        item_loader.selecter = selecter

        # 获取文章内容
        item_loader.add_xpath('content', '//div[@class="post"]')
        # 获取文章标签
        item_loader.add_xpath('tag', '//div[@id="EntryTag"]/a/text()')
        # 加入爬取时间
        crawl_time = datetime.datetime.now().strftime('%Y-%m-%d')
        item_loader.add_value('crawl_time', crawl_time)
        # 管道文件
        yield item_loader.load_item()




