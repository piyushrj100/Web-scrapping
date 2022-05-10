from bs4 import BeautifulSoup
import requests
print('Put some skill that you are not familiar with')
unfamiliar_skill = input('>')
print(f'Filtering out {unfamiliar_skill}')

html_text = requests.get('https://www.timesjobs.com/candidate/job-search.html?searchType=personalizedSearch&from=submit&txtKeywords=Python&txtLocation=India').text
# print(html_text)
soup = BeautifulSoup(html_text, 'html.parser')
job_cards = soup.find_all('li', class_ = 'clearfix job-bx wht-shd-bx')
for job in job_cards : 
    published_date = job.find('span', class_ = 'sim-posted').span.text
    if 'few'  not in published_date:
        company_name = job.find('h3', class_ = 'joblist-comp-name' ).text.replace(' ', '')
        skills = job.find('span', class_ = 'srp-skills').text.replace(' ', '')
        more_info = job.header.h2.a['href']
        if unfamiliar_skill not in skills :
            # print(published_date)
            print(f'Company Name : {company_name.strip()}')
            print(f'Required Skills : {skills.strip()}')
            print(f'Post made : {published_date.strip()}')
            print(f'Link : {more_info.strip()}')
            
            print()

 