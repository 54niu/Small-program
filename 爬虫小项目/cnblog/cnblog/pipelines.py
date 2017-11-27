# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
from scrapy.pipelines.images import ImagesPipeline


class CnblogImagesPipline(ImagesPipeline):
    # results获取下载结果
    def item_completed(self, results, item, info):
        if results:
            item['img_path'] = results[0][1]['path']
        else:
            item['img_path'] = ''
        return item


class MysqlPipeline(object):
    def __init__(self):
        self.conn = pymysql.connect('127.0.0.1', 'root', '951109', 'temp', charset='utf8')
        self.cursor = self.conn.cursor()

    def close_spider(self, spider):
        self.cursor.close()
        self.conn.close()


class CnblogMysqlPipeline(object):
    def process_item(self, item, spider):
        sql = 'insert into cnblogs(url,title,industry,content,author,date_pub,recommand_num,read_num,common_num,' \
              'img_path,tag,crawl_time) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) on duplicate key UPDATE ' \
              'content=VALUES(content),recommand_num=VALUES(recommand_num),read_num=VALUES(read_num),common_num=' \
              'VALUES(common_num)'
        try:
            self.cursor.execute(sql,(
                item['url'],item['title'],item['industry'],item['content'],item['auther'],item['date_pub'],
                item['recommand_num'], item['read_num'], item['common_num'],item['img_path'],item['tag'],item['crawl_time']
            ))
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            print(e)
            print('执行语句失败')
            # 返回交给下一个管道文件处理
        return item
