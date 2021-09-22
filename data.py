import json
import sys
from pathlib import Path
from wordcloud import WordCloud, STOPWORDS

n_suggestions = 50
n_user_activities = 50

def recommendations(community_podium):
    mark_podium = reversed(sorted((value,key) for (key,value) in community_podium.items()))
    community_podium = dict([(k,v) for v,k in mark_podium])
    firstNpairs = {k: community_podium[k] for k in list(community_podium)[:n_suggestions+1]}
    return firstNpairs

def community_p(dict_counter):
    community_podium = {}
    for user in dict_counter:
        marklist=reversed(sorted((value, key) for (key,value) in dict_counter[user].items()))
        dict_counter[user] = dict([(k,v) for v,k in marklist])
        first_ten = list(dict_counter[user])[:n_user_activities]
        point = n_user_activities
        for community in first_ten:
            if community in community_podium:
                community_podium[community] += point
            else:
                community_podium[community] = point
            point -= 1
    return community_podium

def dict_c(data_user):
    dict_counter = {}
    for user in data_user:
        try:
            name = user['name']
            if not name in dict_counter:
                dict_counter[name] = {}
                for community in user['subreddits']:
                    com = community.split('r/')[-1]
                    if com in dict_counter[name]:
                        dict_counter[name][com] += 1
                    else:
                        dict_counter[name][com] = 1
        except:
            continue
    return dict_counter

def execute(subreddit='cats'):
    user_path = './data/'+subreddit+'_user_data.json'

    if not Path(user_path).is_file():
        print('Falha ao acessar dados')
        print('Verifique se é um subreddit aberto e tente executar')
        print('>> python run_reddit.py  <subreddit>')
        print('>> python run_user.py  <subreddit>')
        exit()
    
    f_user = open(user_path)
    data_user = json.load(f_user)

    dict_counter = dict_c(data_user)
    community_podium = community_p(dict_counter)
    firstNpairs = recommendations(community_podium)

    text = []
    for i,(k,v) in enumerate(firstNpairs.items()):
        print(i+1,k,v)
        text += ([k] * v)
    text = ' '.join(text)

    wordcloud = WordCloud(width = 3000, height = 2000, random_state=1, background_color='black', colormap='Set3', collocations=False, stopwords = STOPWORDS).generate(text)
    wordcloud.to_file('./wordcloud/'+subreddit+'.png')


if __name__ == '__main__':
    if len(sys.argv) > 1:
        execute(subreddit=sys.argv[1])
    else:
        execute()