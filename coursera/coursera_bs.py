# Step1
# Importing packages
from urllib.request import urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup

# Step 2
# Create Generic URL retrieval function
def get_site_file(url):
    """
    url - base url to access desired web file
    """
    try:
        html = urlopen(url)
        bs = BeautifulSoup(html, 'html.parser')
        return bs

    except HTTPError as e:
        print(e)

# Step 3
# Assign variable to Generic URL
# Coursera courses
page_content = get_site_file('https://www.coursera.org/courses')

# Step 4
# Navigate to list of courses
try:
    discovery_course = page_content.find("ul", {'class':'ais-InfiniteHits-list'})
except AttributeError as e:
    print('Something seems to be missing with the tag')

# Step 5
# Parse Data
if page_content == None:
    print('The file could not be found')
else:
    courses = page_content.find_all('li', {'class': 'ais-InfiniteHits-item'})
    for course in courses:
        try:
            course_title = course.h2.get_text()
            course_rating = course.find('span',{'class': 'ratings-text'}).get_text()
            print(f"Course Title: \t {course_title}")
            print(f"Course Rating: \t {course_rating}")
            print('\n'+('|')+('<'*3)+('-'*7)+' New Course ' +('-'*7)+('>'*3)+('|')+'\n')
        except AttributeError as e:
            print(e)
