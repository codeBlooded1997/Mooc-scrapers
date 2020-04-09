# Imorting packages
from urllib.request import Request, urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup
from time import sleep

# Create Generic URL retrieval function
def get_site_file(url):
    """
    url - base url to access desired web file
    """
    try:
        # Getting url
        hdr = {'User-Agent': 'Mozilla/5.0'}
        req = Request(url, headers=hdr)
        # Defining soup object
        page = urlopen(req)
        soup = BeautifulSoup(page, "html.parser")
        print('Spup created ...')
        return soup

    except HTTPError as e:
        print("Error is : ", e)

def parse_page(soup):
  """
  This function takes soup object as an argument.
  It will parse the first page in the given object.
  """
  # Directin to course section
  course_sec = soup.find('div', {'class':'top-classes'})
  # Creating list of courses
  courses_list = course_sec.findAll('div', {'class':'top-classes-container'})

  if courses_list == None:
      print('The courses list could not be found')
  else:
      for list in courses_list:
          try:
              # Directing to title
              category_title = list.find('h2', {'class':'left'})
              print('\n'+('|')+('<'*3)+('-'*7)+' '+ category_title.text +' '+('-'*7)+('>'*3)+('|')+'\n')
              # Creating list of course blocks in each list of categories
              blocks = list.find('ul').findAll("div",{"class":"ss-card ss-class"})
              # Iterating in blocks list
              for block in blocks:
                  # Extracting to course title
                  course_title = block.find("p", {"class":"ss-card__title"}).find('a')
                  # Extracting course teacher
                  course_techer = block.find("div", {"class":"ss-card__teacher-placeholder"}).find('a')
                  # Extracting students quantity
                  course_students = block.find("div", {"class":"ss-class__stats"}).find("span")
                  # Extracting URL
                  course_url = block.find("p", {"class":"ss-card__title"}).find('a').attrs['href']
                  print('\n'+(' '*4)+('|')+('-'*7)+('>'*3)+' '+ course_title.text.strip())
                  print((' '*16)+ course_url)
                  print((' '*16)+ course_students.text.strip())
                  print((' '*16)+ course_techer.text.strip())
          except AttributeError as e:
              print(e)

# Saving scraped data

base_url = 'https://www.skillshare.com/browse?via=header'
soup = get_site_file(base_url)
data = parse_page(soup)
