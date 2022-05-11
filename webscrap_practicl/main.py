from bs4 import BeautifulSoup
import requests
import time
import json
from os.path import exists

def append_json(job_info, timestamp,technology) :
    with open(f'post/{technology}_job_{timestamp}.json', 'r+') as json_file :
        json_data = json.load(json_file)
        json_data["job_description"].append(job_info)
        json_file.seek(0)
        json.dump(json_data, json_file, indent = 4, sort_keys = True)

def add_first_json(job_info,timestamp,technology) :
    description_list = { "job_description" : [] }
    description_list["job_description"].append(job_info)
    with open(f'post/{technology}_job_{timestamp}.json','w')  as json_file:
        json.dump(description_list, json_file, indent = 4, sort_keys = True)


def find_jobs(technology,location_,pages, unfamiliar_skill="NULL") :
    #checking  if page size is <=12 . If it is > 12, A value error exception will be thrown.
    if pages <=12 :
        print(f'Valid! Page size is less than equal to 12! Proceeding ahead...\n')        
    else :
        raise ValueError('Page size should be less than equal to 12!! Please try again...')
    #Getting all the required job info for each job in each page.
    timestamp= int(time.time())
    for page_num in range(1,pages+1) :
        print(f'Parsing page {page_num}...')
        html_text = requests.get(f'https://www.timesjobs.com/candidate/job-search.html?from=submit&actualTxtKeywords={technology}&searchBy=0&rdoOperator=OR&searchType=personalizedSearch&txtLocation={location_}&luceneResultSize=25&postWeek=60&txtKeywords=Python&pDate=I&sequence={page_num}&startPage=1').text
        # print(html_text)
        soup = BeautifulSoup(html_text, 'html.parser')
        job_cards = soup.find_all('li', class_ = 'clearfix job-bx wht-shd-bx')
        for job in job_cards : 
            published_date = job.find('span', class_ = 'sim-posted').span.text.strip()

            # job.find('i', class_ = 'material-icons').extract() #for removing the materials icon tag for first li
            # job.find('i', class_ = 'material-icons').extract() #for removing the second materials icon tag
            # experience = job.find('ul', class_ = 'top-jd-dtl clearfix').li.text

            job_loc_exp = job.find('ul', class_ = 'top-jd-dtl clearfix') #getting job location and experiece
            job_loc_exp.find('li').find('i', class_ = 'material-icons').extract()   #for removing the materials icon tag for first li
            experience = job_loc_exp.find('li').text
            location=job_loc_exp.select_one(":nth-child(2)").span
            if location is None :
                location=job_loc_exp.select_one(":nth-child(3)").span
            job_location = location.text
            
            if 'few'  not in published_date:
                company_name = job.find('h3', class_ = 'joblist-comp-name' ).text.replace(' ', '').strip()
                skills = job.find('span', class_ = 'srp-skills').text.replace(' ', '').strip()
                more_info = job.header.h2.a['href'].strip()
                if unfamiliar_skill not in skills :
                    job_info = {'Company Name' : company_name,
                                'Experience Required' : experience,
                                'Location' : job_location,
                                'Key Skills' : skills,
                                'More Info' : more_info,
                                'Publishing Date' : published_date
                    
                    }

                    #Wrting to json file.
                    if exists(f'post/{technology}_job_{timestamp}.json') :
                        append_json(job_info,timestamp,technology)
                    else : 
                        add_first_json(job_info,timestamp,technology)

        if page_num != pages :
            print('Waiting for 10 seconds before moving to next page.....')
            print()
            time.sleep(10)
    
if __name__ == '__main__' :
    pages= 8
    technology= 'Python'
    location= 'India'
    find_jobs(technology,location,pages)

 