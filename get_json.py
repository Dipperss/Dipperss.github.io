import urllib.request
import json
def get_record(url):
    resp = urllib.request.urlopen(url)
    ele_json = json.loads(resp.read())

    return ele_json['result']
    

if __name__ == '__main__':
    pages = int(get_record('http://ncov.news.dragon-yuan.me/api/news?search=&page=')['pages'])

    json_list = []

    print('新闻页数：',pages)

    for i in range(1,pages+1):

        json_list += get_record('http://ncov.news.dragon-yuan.me/api/news?search=&page={}'.format(i))['list']
        print('当前页数：', i)

    with open('./news.json','w') as f:
        json.dump(json_list,f) 