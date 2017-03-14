# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
# 项目中的 piplines 文件

class TutorialPipeline(object):
    def process_item(self, item, spider):
        return item
