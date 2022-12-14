import scrapy, json,os

from scrapy.utils.project import get_project_settings


class jobItemSpider(scrapy.Spider):

    name = 'lp_jobcard'

    # custom_settings = {
    #     'ITEM_PIPELINES':{
    #         'lp_job.pipelines.JobCardPipeline': 300
    #     }
    # }

    # settings = get_project_settings()
    # print(os.getcwd())
    # print(settings.get('PROXY_SETTINGS'))

    def __init__(self,key_word,city, file_mark=False):

        self.url = "https://apic.liepin.com/api/com.liepin.searchfront4c.pc-search-job"
        self.file_mark = file_mark
        self.key_word = key_word
        self.city = city


        self.request_body = {
            "data": {
                "mainSearchPcConditionForm": {
                    "city": str(self.city),
                    "dq": str(self.city),
                    "pubTime": "1",
                    "currentPage": 0,
                    "pageSize": 40,
                    "key": self.key_word,
                    "workYearCode": "0",
                    "compId": "",
                    "compName": "",
                    "compTag": "",
                    "industry": "",
                    "salary": "",
                    "jobKind": "",
                    "compScale": "",
                    "compKind": "",
                    "compStage": "",
                    "eduLevel": "",
                    "otherCity": ""
                },
                "passThroughForm": {
                    "scene": "page"
                }
            }
        }
        self.request_headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'zh-CN,zh;q=0.9,en-GB;q=0.8,en;q=0.7,ja;q=0.6',
            'Connection': 'keep-alive',
            'Content-Type': 'application/json;charset=UTF-8;',
            'Origin': 'https://www.liepin.com',
            'Referer': 'https://www.liepin.com/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-site',
            'User-Agent':
            'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Mobile Safari/537.36',
            'X-Client-Type': 'web',
            'X-Fscp-Bi-Stat':
            '{"location": "https://www.liepin.com/zhaopin/?inputFrom=head_navigation&scene=init&workYearCode=0&ckId=auhhsozt91vnk37d0kjbrxymzqr7ah29"}',
            'X-Fscp-Fe-Version': '07aeb7f',
            'X-Fscp-Std-Info': '{"client_id": "40108"}',
            'X-Fscp-Trace-Id': '0dde402e-46d1-4237-9313-5ec81d99143c',
            'X-Fscp-Version': '1.1',
            'X-Requested-With': 'XMLHttpRequest'
        }

    def start_requests(self):

        yield scrapy.Request(url=self.url,
                             method='POST',
                             body=json.dumps(self.request_body),
                             headers=self.request_headers,
                             callback=self.basic_parse)
        pass

    def basic_parse(self, response):

        r_data = json.loads(response.text)
        main_data = r_data.get('data').get('data')
        page_data = r_data.get('data').get('pagination')
        jobCard_data = main_data.get('jobCardList')

        for each_job in jobCard_data:
            # ?????????????????????
            yield ({'item':each_job,'key_word':self.key_word})
            # print({'item':each_job,'key_word':self.key_word})

        cur_page = page_data.get('currentPage')
        total_page = page_data.get('totalPage')

        if cur_page < total_page - 1:

            self.request_body['data']['mainSearchPcConditionForm'][
                'currentPage'] += 1
            print(self.request_body)
            yield scrapy.Request(url=self.url,
                                 method='POST',
                                 body=json.dumps(self.request_body),
                                 headers=self.request_headers,
                                 callback=self.basic_parse)

class JobDetailSpider(scrapy.Spider):

    name = "lp_jobdetail"

    # custom_settings = {
    #     'ITEM_PIPELINES':{
    #         'lp_job.pipelines.JobDetailPipeline': 400
    #     }
    # }

    def __init__(self,link,job_id):

        self.link = link
        self.job_id = job_id

    def start_requests(self):
        yield scrapy.Request(url=self.link,method='GET',callback=self.basic_parse)

    def basic_parse(self,response):

        job_detail = ';'.join(response.css('.paragraph dd::text').getall())
        yield({'job_id':self.job_id,'job_detail':job_detail})