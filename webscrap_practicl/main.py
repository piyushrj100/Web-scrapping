from bs4 import BeautifulSoup
import requests
import time

print('Put some skill that you are not familiar with')
unfamiliar_skill = input('>')
print(f'Filtering out {unfamiliar_skill}')

def find_jobs() :
    html_text = requests.get('https://www.timesjobs.com/candidate/job-search.html?searchType=personalizedSearch&from=submit&txtKeywords=Python&txtLocation=India').text
    # print(html_text)
    soup = BeautifulSoup(html_text, 'html.parser')
    job_cards = soup.find_all('li', class_ = 'clearfix job-bx wht-shd-bx')
    for index,job in enumerate(job_cards) : 
        published_date = job.find('span', class_ = 'sim-posted').span.text

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
        print(job_location, experience)
        
        # if 'few'  not in published_date:
        #     company_name = job.find('h3', class_ = 'joblist-comp-name' ).text.replace(' ', '')
        #     skills = job.find('span', class_ = 'srp-skills').text.replace(' ', '')
        #     more_info = job.header.h2.a['href']
        #     if unfamiliar_skill not in skills :
        #         with open(f'post/{index}.txt','w') as f :
        #             f.write(f'Company Name : {company_name.strip()}\n')
        #             f.write(f'Required Skills : {skills.strip()}\n')
        #             f.write(f'Post made : {published_date.strip()}\n')
        #             f.write(f'Link : {more_info.strip()}\n')
        #             f.write()
        #         print('File Saved')
                

if __name__ == '__main__' :
    while True :
        find_jobs()
        time_wait = 10
        print(f'Waiting {time_wait} minutes...')
        time.sleep(time_wait*60)

 