from bs4 import BeautifulSoup

with open('home.html', 'r')  as html_file:
    content=html_file.read()
    soup = BeautifulSoup(content, 'html.parser')
    # tags = soup.find('h5') #finds the first occurence of h5 tag and stops
    # courses_html_tags = soup.find_all('h5') #will create a list
    # print(courses_html_tags)
    
    #below will print the text inside the tags
    # for course in courses_html_tags :
    #     print(course.text)
    
    course_cards = soup.find_all('div', class_='card') #adding the div class name 
    for course in course_cards :
        # print(course)
        #will print course name present inside the h5 tags
         course_name=course.h5.text
         course_price = course.a.text.split()[-1]
         print(f' {course_name} costs {course_price}')






