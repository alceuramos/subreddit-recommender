import scrapy


class UserScraperSpider(scrapy.Spider):
    name = 'UserScraper'
    start_urls = []
#     custom_settings = {
#     'LOG_ENABLED': False,
#   }

    def __init__(self, users):
        self.start_urls = ['https://old.reddit.com/user/'+user for user in users]


    def parse(self, response):
        karma =      response.css('span.karma::text').extract_first()
        comment_karma =     response.css('span.karma.comment-karma::text').extract_first()
        name =     response.css('span.pagename::text').extract_first()
        age =  response.css('span.age > time::text').extract_first()
        subreddits = response.css('a.subreddit::text').extract()
        user = {
            'name': name,
            'age': age,
            'karma': karma,
            'comment_karma': comment_karma,
            'subreddits': subreddits
        }
        yield user
        next_url = response.css('span.next-button > a::attr(href)').extract_first()
        if '?count=100&' not in next_url:
            yield scrapy.Request(url=next_url, callback=self.parse)