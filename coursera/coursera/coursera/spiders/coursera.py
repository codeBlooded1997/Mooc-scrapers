import scrapy
from scrapy.crawler import  CrawlerProcess
# Prevents server errors
from time import sleep
# For saving scraped data into a CSV
import pandas as pd

class DC_Chapter_Spider( scrapy.Spider ):
    name = "scraper"

    base_url = 'https://www.coursera.org/courses?page={}&index=prod_all_products_term_optimization'
    course_titles = []
    course_ratings = []
    students_nums = []
    course_urls = []


    def start_requests( self ):
        """
        This method requests the first page to start scraping.
        """
        try:
            yield scrapy.Request( url=self.base_url.format(1), callback=self.parse_front )
        except HTTPError as e:
            print(e)

    def parse_front( self, response ):
        """
        This method scrapes the frist page of the url,
        Scrapes courses info,
        Goes to the next page to scrape if it's availble and
        Saves the extracted data in CSV format.
        """
        # Narrow in to list of courses
        try:
            discovery_course = response.css( 'ul.ais-InfiniteHits-list' )
        except AttributeError as e:
            print( 'Something seems to be missing with the tag' )

        # Directing to courses
        try:
            courses = discovery_course.css( 'li' )
        except AttributeError as e:
            print( 'Failed to created list of courses.' )

        count = 1
        # Iterating through courses
        for course in courses:
            # Scraping courses data form page
            try:
                # Extracting course title
                if course.css( "h2" ):
                    course_title = course.css( "h2::text" ).extract_first()
                else:
                    course_title = "N / A"

                # Extracting course rating
                if course.css( 'span.ratings-text' ):
                    course_rating = course.css( 'span.ratings-text::text' ).extract_first()
                else:
                    course_rating = "N / A"

                # Extracting students quantity
                if course.css( 'span.enrollment-number' ):
                    students_num = course.css( 'span.enrollment-number::text' ).extract_first()
                else:
                    students_num = "N / A"

                # Extracting course url
                if course.css( 'a::attr(href)' ):
                    course_url = course.css( 'a::attr(href)' ).extract_first()
                else:
                    course_url = "N / A"
                    pass

                self.course_titles.append(course_title)
                self.course_ratings.append(course_rating)
                self.students_nums.append(students_num)
                self.course_urls.append(course_url)
                # Saving extracted data in a table (CSV)
                #self.item['course_title'] = course_title
                #self.item['url'] = course_url
                #self.item['rating'] = course_rating
                #self.item['enrollment'] = students_num

                print('\n'+ str(count) + ('  |')+('<'*3)+('-'*7)+ ' ' + course_title +('-'*7)+('>'*3)+('|')+'\n')
                print( course_rating )
                print( course_url )
                print( students_num )
                print()
                print()
                count += 1
            except AttributeError as e:
                print(e)

        # Directing to pageiation section.
        pages = response.css( "div.pagination-controls-container" )
        if pages.xpath( '//button[contains(@class, "current")]' ) and pages.css( 'button#pagination_number_box_button::text' ):
            # Extracting current page number.
            current_page = pages.xpath( '//button[contains(@class, "current")]/text()' ).extract_first()
            # Extrating last page number.
            last_page = pages.css( 'button#pagination_number_box_button::text' ).extract()[-1]

        else:
            print("NOT FUCKIIIIING FOUND")
        # Checking if it is the last page.
        if int( current_page ) < int( last_page ):
            # Gettin to next page and start scraping it.
            print("Getting page {} to scrape...".format(int(current_page)+1))
            sleep(5)
            yield scrapy.Request( url=self.base_url.format(int(current_page)+1), callback=self.parse_front )
        else:
            print( "Page {} is last page.".format(current_page) )
            pass

        result = pd.DataFrame(
            {
                'Course Title' : self.course_titles,
                'Course Rating' : self.course_ratings,
                'Course Enrollment' : self.students_nums,
                'Course URL' : self.course_urls,
            })

        result.to_csv('result.csv', index=False)


    def parse_pages( self, response ):
        """
        This method can be updated to scrape the inner page
        for each course to scrape other details.
        """
        pass


dc_dict = dict()
