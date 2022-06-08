import pandas as pd
import requests
import concurrent.futures
import time

# count time:
start = time.perf_counter()

class FetchData():
    def __init__(self):
        self.companies_name = []
        self.companies_ric_code = []
        
    
    def request_url(self, url):
        """define a method to request to a specefic url and get the result content formated in json."""
        url = str(url)
        r = requests.get(url)
        result = r.json()
        return result

    def get_all_ric_code(self):
        """get all of the ricCode from endpoint."""

        result = self.request_url('https://www.refinitiv.com/bin/esg/esgsearchsuggestions')
       
        for i in range(len(result)):
            self.companies_name.append(result[i]["companyName"])
        
        for i in range(len(result)):
            self.companies_ric_code.append(result[i]["ricCode"])
        
        return self.companies_name, self.companies_ric_code

    def fetch_esg_result(self, num: int = 100):
        """Fetch each company esg-scores."""
        
        self.get_all_ric_code()
        responses = []
        urls = []
        self.companies_name = self.companies_name[0:num]
        self.companies_ric_code = self.companies_ric_code[0:num]
        for ric_code in self.companies_ric_code:
            urls.append('https://www.refinitiv.com/bin/esg/esgsearchresult?ricCode={}'.format(ric_code))
        # fetch responses in multythread:
        with concurrent.futures.ThreadPoolExecutor() as executor:
            results = executor.map(self.request_url, urls)
            
            for result in results:
                responses.append(result)

        return responses

    def esg_as_csv(self, num: int=100):
        """save data in csv file."""
        esg_scores = []
        environment_scores = []
        social_scores = []
        governance_scores = []
        ranks = []
        total_industries  = []

        responses = self.fetch_esg_result(num)

        df = pd.DataFrame()
        df['company_name'] = self.companies_name
        df['ric_code'] = self.companies_ric_code

        for response in responses:
            esg_scores.append(response['esgScore'].get('TR.TRESG').get('score'))
            environment_scores.append(response['esgScore'].get('TR.EnvironmentPillar').get('score'))
            social_scores.append(response['esgScore'].get('TR.SocialPillar').get('score'))
            governance_scores.append(response['esgScore'].get('TR.GovernancePillar').get('score'))
            ranks.append(response['industryComparison'].get('rank'))
            total_industries.append(response['industryComparison'].get('totalIndustries'))

        df['esg_score'] = esg_scores
        df['environment_scores'] = environment_scores
        df['social_scores'] = social_scores
        df['governance_scores'] = governance_scores
        df['ranks'] = ranks
        df['total_industries'] = total_industries

        df.to_csv('utils/esg_result.csv', encoding='utf-8', index=False)


if __name__ == '__main__':
    result_csv = FetchData()
    result_csv.esg_as_csv(999)

finish = time.perf_counter()
print('Finished in {} seconds.'.format(round(finish - start, 2)))
