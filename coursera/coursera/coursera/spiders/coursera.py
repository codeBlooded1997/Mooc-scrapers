import scrapy
from scrapy.crawler import  CrawlerProcess

class DC_Chapter_Spider( scrapy.Spider ):
    name = "scraper"

    def start_requests( self ):
        try:
            base_url = 'https://www.coursera.org/courses'
            yield scrapy.Request( url=base_url, callback=self.parse_front )
        except HTTPError as e:
            print(e)

    def parse_front( self, response ):
        # Narrow in to list of courses
        try:
            discovery_course = response.css( 'ul.ais-InfiniteHits-list' )
            print('Directory FOUNDDDDDDDD!!!')
        except AttributeError as e:
            print('Something seems to be missing with the tag')

        # Directing to courses
        try:
            courses = discovery_course.css('li')
            print('COURSES LIST CREATED!!!')
        except AttributeError as e:
            print('Failed to created list of courses.')

        # Iterating through courses
        for course in courses:
            # Extracting course title
            try:
                course_title = course.css("h2::text").extract_first()
                course_rating = course.css('span.ratings-text::text').extract_first()
                course_url = course.css('a::attr(href)').extract_first()

                print(course_title)
                print(course_rating)
                print(course_url)
                print()
                print()
                print()
                print()
            except AttributeError as e:
                print(e)


    def parse_pages( self, response ):
        pass



dc_dict = dict()
