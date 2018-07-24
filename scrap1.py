# -*- coding: utf-8 -*-
import scrapy
import re
from ..items import OmimItem


class Scrap1Spider(scrapy.Spider):
    custom_settings = {
        'ITEM_PIPELINES': {
            'omim.pipelines.OmimPipeline': 300
        }
    }

    name = 'scrap1'
    allowed_domains = ['omim.org']
    start_urls = ['http://omim.org/']


    def parse(self, response):
        url_start = 'https://omim.org/search/?index=entry&search=prefix%3A%23&sort=number+asc&start='
        url_end = '&limit=10'
        for num in xrange(3):
            all_url = url_start + str(num+1) + url_end
            print all_url
            yield scrapy.Request(all_url, callback=self.parse_gene_page)
        # yield scrapy.Request("https://omim.org/search/?index=entry&search=prefix%3A%23&sort=number+asc&start=30&limit=100", callback=self.parse_gene_page)



    def parse_gene_page(self, response):
        # tbody = response.xpath('//*[@id="phenotypeMapFold_3"]/table/tbody').extract()[0]
        # print "crawing spider----------------------------------------------/--------------------"
        # print tbody

        # all_tbody = response.xpath('//*[@id="content"]/div[1]/div[7]/div[2]/div/table/tbody')
        # 每页10 个列表：
        url = response.url
        page_num = re.findall('start=(\d+)',url)[0]
        print "=============crawing page %s================"%page_num
        tr_ctx = ""
        all_trs = response.xpath('//*[@id="content"]/div[1]/div[*]/div[2]/div/table[@class="table table-bordered table-condensed small mim-table-padding"]/tbody/tr')
        Location =""
        Phenotype =""
        Phenotype_MIM_number = ""
        Inheritance = ""
        Phenotype_mapping_key = ""
        Gene_Locus = ""
        Gene_Locus_MIM_number= ""
        for tr in all_trs:
            try:
                Location = tr.xpath('td[1]/span/a/text()').extract()[0].strip()
            except:
                print("++++++++++++++++++++++Location wrong 1111 +++++++++++++++++++++++++++++++++++++++++++")
                Location = 'None'
                print(Location + "\t" +Phenotype + "\t" +Phenotype_MIM_number )


            try:
                Phenotype = tr.xpath('td[2]/span/text()').extract()[0].strip()
            except:
                print("++++++++++++++++++++++Phenotype wrong 1111 +++++++++++++++++++++++++++++++++++++++++++")
                Phenotype = 'None'
                print(Location + "\t" +Phenotype + "\t" +Phenotype_MIM_number )

            try:
                Phenotype_MIM_number = tr.xpath('td[3]/span/a/text()').extract()[0].strip()
            except:
                print("++++++++++++++++++++++Phenotype_MIM_number wrong 1111 +++++++++++++++++++++++++++++++++++++++++++")
                Phenotype_MIM_number = 'None'
                print(Location + "\t" +Phenotype + "\t" +Phenotype_MIM_number )


            try:
                Inheritance = tr.xpath('td[4]/span/abbr/text()').extract()[0].strip()
            except:
                print("++++++++++++++++++++++Inheritance wrong 1111 +++++++++++++++++++++++++++++++++++++++++++")
                print(Location + "\t" +Phenotype + "\t" +Phenotype_MIM_number )
                Inheritance = 'None'

            try:
                Phenotype_mapping_key = tr.xpath('td[5]/span/abbr/text()').extract()[0].strip()
            except:
                print("++++++++++++++++++++++Phenotype_mapping_key wrong 1111 +++++++++++++++++++++++++++++++++++++++++++")
                print(Location + "\t" +Phenotype + "\t" +Phenotype_MIM_number )
                Phenotype_mapping_key = "None"

            try:
                Gene_Locus = tr.xpath('td[6]/span/text()').extract()[0].strip()
            except:
                print("++++++++++++++++++++++Gene_Locus wrong 1111 +++++++++++++++++++++++++++++++++++++++++++")
                print(Location + "\t" +Phenotype + "\t" +Phenotype_MIM_number )
                Gene_Locus = "None"

            try:
                Gene_Locus_MIM_number = tr.xpath('td[7]/span/a/text()').extract()[0].strip()
            except:
                print("++++++++++++++++++++++Gene_Locus_MIM_number wrong 1111 +++++++++++++++++++++++++++++++++++++++++++")
                print(Location + "\t" +Phenotype + "\t" +Phenotype_MIM_number )
                Gene_Locus_MIM_number = "None"

            tr_ctx += Location + "\t" + Phenotype + "\t" + Phenotype_MIM_number + "\t" + Inheritance + "\t" + \
                      "\t" + Phenotype_mapping_key + "\t" + Gene_Locus + "\t" + Gene_Locus_MIM_number + '\t' + page_num+"\n"

        item = OmimItem()
        item['ctx'] = tr_ctx
        print "crawing in spider ------------------------------------------------------------------"

        yield item
