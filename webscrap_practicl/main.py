from bs4 import BeautifulSoup
import requests
import time
import json

print('Put some skill that you are not familiar with')
unfamiliar_skill = input('>')
print(f'Filtering out {unfamiliar_skill}')

def find_jobs() :
    description ={'job_description' : [] } #to create array of json obj
    html_text = requests.get('https://www.timesjobs.com/candidate/job-search.html?searchType=personalizedSearch&from=submit&txtKeywords=Python&txtLocation=India').text
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
                description['job_description'].append(job_info)
    timestamp = int(time.time())

    #writing to the json file created.
    with open(f'post/file_{timestamp}.json','w') as f :
        json.dump(description,f, indent = 4, sort_keys=True)
    print(f'Saved to File : post/file_{timestamp}.json' )
    print('Clearing dictionary')
    description.clear()
    print()
                

if __name__ == '__main__' :
    while True :
        find_jobs()
        time_wait = 60
        print(f'Waiting {time_wait} minutes...')
        time.sleep(time_wait*60)
        print("Resuming....")

 