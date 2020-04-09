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

        count = 1
        # Iterating through courses
        for course in courses:
            # Extracting course title
            try:
                # Extracting course title
                if course.css("h2"):
                    course_title = course.css("h2::text").extract_first()
                else:
                    course_title = "N / A"

                # Extracting course rating
                if course.css('span.ratings-text'):
                    course_rating = course.css('span.ratings-text::text').extract_first()
                else:
                    course_rating = "N / A"

                # Extracting students quantity
                if course.css('span.enrollment-number'):
                    students_num = course.css('span.enrollment-number::text').extract_first()
                else:
                    students_num = "N / A"

                # Extracting course url
                if course.css('a::attr(href)'):
                    course_url = course.css('a::attr(href)').extract_first()
                else:
                    course_url = "N / A"
                    pass



                print('\n'+ str(count) + ('  |')+('<'*3)+('-'*7)+ ' ' + course_title +('-'*7)+('>'*3)+('|')+'\n')
                #print(course_title)
                print(course_rating)
                print(course_url)
                print(students_num)
                print()
                print()
                print()
                print()
                count += 1
            except AttributeError as e:
                print(e)


    def parse_pages( self, response ):
        pass


dc_dict = dict()
