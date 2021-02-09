import scrapy
import json


class Myspider(scrapy.Spider):
    name = 'mybot'
    start_urls = [
        'https://www.timeshighereducation.com/world-university-rankings/2020/world-ranking#!/page/0/length/25/sort_by/rank/sort_order/asc/cols/stats'
    ]
    headers = {
        "Accept": "application/json,text/javascript,*/*;q=0.01",
        "Accept-Encoding": "gzip,deflate,br",
        "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
        "Referer": "https://www.timeshighereducation.com/world-university-rankings/2020/world-ranking",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "x-requested-with": "XMLHttpRequest"
    }

    def parse(self, response, **kwargs):
        url = 'https://www.timeshighereducation.com/sites/default/files/the_data_rankings/world_university_rankings_2020_0__24cc3874b05eea134ee2716dbf93f11a.json'

        yield scrapy.Request(url, callback=self.parse_api, headers=self.headers)

    def parse_api(self, response):
        raw_data = response.body
        data_ = json.loads(raw_data)

        for data in data_['data']:

            yield {
                'UniversityRank': data['rank'],
                'UniversityName': data['name'],
                'Country': data['location'],
                'Total_Num_of_Students': data['stats_number_students'],
                'StudentStaffRatio': data['stats_student_staff_ratio'],
                'Num_of_Intl_students': data['stats_pc_intl_students'],
                'FemaletoMaleRatio': data['stats_female_male_ratio'],
                'scores_overall': data['scores_overall'],
                'scores_overall_rank': data['scores_overall_rank'],
                'scores_teaching': data['scores_teaching'],
                'scores_teaching_rank': data['scores_teaching_rank'],
                'scores_research': data['scores_research'],
                'scores_research_rank': data['scores_research_rank'],
                'scores_citations': data['scores_citations'],
                'scores_citations_rank': data['scores_citations_rank'],
                'scores_industry_income': data['scores_industry_income'],
                'scores_industry_income_rank': data['scores_industry_income_rank'],
                'scores_international_outlook': data['scores_international_outlook'],
                'scores_international_outlook_rank': data['scores_international_outlook_rank'],
                'subjects_offered': data['subjects_offered']

            }


# /html/body/div[6]/div/section/div/div[3]/div/div[1]/div[1]/div/div[3]/table/tbody/tr[1]/td[3]

# /html/body/div[6]/div/section/div/div[3]/div/div[1]/div[1]/div/div[3]/table/tbody/tr[1]/td[1]

# document.querySelector("#rmjs-1 > p:nth-child(1)")
# table wur-hash-processed wur-cols-processed wur-pagelen-processed dataTable no-footer rank-only stats usr-processed tbody

# https://www.timeshighereducation.com/sites/default/files/the_data_rankings/world_university_rankings_2021_0__fa224219a267a5b9c4287386a97c70ea.json

'''
'scores_overall': data['scores_overall'],
                'scores_overall_rank': data['scores_overall_rank'],
                'scores_teaching': data['scores_teaching'],
                'score_teaching_rank': data['score_teaching_rank'],
                'scores_research': data['scores_research'],
                'scores_research_rank': data['scores_research_rank'],
                'scores_citations': data['scores_citations'],
                'scores_citations_rank': data['scores_citations_rank'],
                ''
'''
