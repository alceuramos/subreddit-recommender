from reddit import RedditScraperSpider
from scrapy.crawler import CrawlerProcess
import os
import sys
from pathlib import Path

def execute(subreddit='cats'):
    file_path = './data/'+subreddit+'_data.json'
    if Path(file_path).is_file():
        os.remove(file_path)
    process_settings = {
        'FEEDS': {
            file_path:{'format':'json'},
        }
    }
    process = CrawlerProcess(settings=process_settings)
    process.crawl(RedditScraperSpider,subreddit)
    process.start()
    
    if len(open(file_path).read()) == 0:
        os.remove(file_path)

    
if __name__ == '__main__':
    try:
        execute(subreddit=sys.argv[1])
    except:
        execute()