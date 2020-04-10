import scrapy
from scrapy.crawler import  CrawlerProcess
from pdf_url.items import CourseraItem    # importing the data type we defined in the items.py file
from time import sleep

class DC_Chapter_Spider( scrapy.Spider ):
    name = "scraper"

    base_url = 'https://www.coursera.org/courses?page={}&index=prod_all_products_term_optimization'

    def start_requests( self ):
        try:
            #for page in range(1, 100):
            #    print("SCRAPING PAGE {} ...".format(page))
            #    print("-"*15)
            #    print("*"*15)
            #    print("-"*15)
            #    print("*"*15)
            #    sleep(5)
            yield scrapy.Request( url=self.base_url.format(1), callback=self.parse_front )
        except HTTPError as e:
            print(e)

    def parse_front( self, response ):
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

                print('\n'+ str(count) + ('  |')+('<'*3)+('-'*7)+ ' ' + course_title +('-'*7)+('>'*3)+('|')+'\n')
                print( course_rating )
                print( course_url )
                print( students_num )
                print()
                print()
                print()
                print()
                count += 1
            except AttributeError as e:
                print(e)

        # Directing to pageiation section.
        pages = response.css( "div.pagination-controls-container" )
        # Extracting current page number.
        current_page = pages.xpath( '//button[contains(@class, "current")]' ).extract_first()
        # Extrating last page number.
        last_page = pages.css( 'button#pagination_number_box_button::text' ).extract()[-1]
        # Checking if it is the last page.
        if int( current_page ) < int( last_page ):
            print( "Going to last page..." )
            # Gettin to next page and start scraping it.
            print("Getting page {} to scrape...")
            sleep(5)
            yield ( url=self.base_url.format(current_page+1), callback=self.parse_front )
        else:
            print( "Page {} is last page.".format(current_page) )
        #try:
        #    yield scrapy.Request( url=base_url.format(1), callback=self.parse_front )
        #except:

    def parse_pages( self, response ):
        pass


dc_dict = dict()
