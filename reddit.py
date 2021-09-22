import scrapy

class RedditScraperSpider(scrapy.Spider):
    name = 'RedditScraper'
    
#     custom_settings = {
#     'LOG_ENABLED': False,
#   }
    def __init__(self, subreddit):
        self.start_urls = {'https://old.reddit.com/r/'+subreddit}

    def parse(self, response):
        
        user =      response.css('a.author.may-blank::text').extract()
        title =     response.css('a.title.may-blank::text').extract()
        votes =     response.css('div.score.unvoted::text').extract()
        comments =  response.css('a.comments.may-blank::text').extract()
        age =       response.css('time.live-timestamp::text').extract()
        for item in zip(user, title, votes, comments, age):
            all_items = {
                'user':     item[0],
                'title':    item[1],
                'votes':     item[2],
                'comments': item[3],
                'age':      item[4],
            }
            yield all_items
        next_url = response.css('span.next-button > a::attr(href)').extract_first()
        if '?count=500&' not in next_url:
            yield scrapy.Request(url=next_url, callback=self.parse)