import json
import os
import sys
from user import UserScraperSpider
from scrapy.crawler import CrawlerProcess
from pathlib import Path

def execute(subreddit='cats'):

    file_path = './data/'+subreddit+'_user_data.json'
    reddit_file = './data/'+subreddit+'_data.json'
    if not Path(reddit_file).is_file():
        print('Falha ao acessar dados')
        print('Verifique se é um subreddit aberto e tente executar')
        print('>> python run_reddit.py <subreddit>')
    else:
        if Path(file_path).is_file():
            os.remove(file_path)
        process_settings = {
            'FEEDS': {
                file_path:{'format':'json'},
            }
        }
        f = open(reddit_file)
        data = json.load(f)
        users = []

        for i in data:
            users.append(i['user'])

        process = CrawlerProcess(settings=process_settings)
        process.crawl(UserScraperSpider,users)
        process.start()

if __name__ == '__main__':
    if len(sys.argv) > 1:
        execute(subreddit=sys.argv[1])
    else:
        execute()