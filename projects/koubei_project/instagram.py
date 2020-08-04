# -*- coding: utf-8 -*-
import json
import requests
from lxml import etree
from urllib import parse

BASE_URL = "https://www.instagram.com/urnotchrislee/"
headers = {
    "Origin": "https://www.instagram.com/",
    "Referer": "https://www.instagram.com/urnotchrislee/",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36",
    "Host": "www.instagram.com",
}



def load_rest(table, has_next_page):
    rest = []
    while has_next_page:
        text = json.dumps(table)
        URL = 'https://www.instagram.com/graphql/query/?query_hash=42323d64886122307be10013ad2dcc44&variables=' + parse.quote(text)
        URL = URL.replace("%20", "")
        print(URL)
        res = requests.get(URL, headers=headers)
        dic = json.loads(res.content.decode(), encoding='utf-8')

        data = dic['data']['user']['edge_owner_to_timeline_media']
        nodes = data['edges']
        end_cursor = data['page_info']['end_cursor']
        print(end_cursor)
        has_next_page = data['page_info']['has_next_page']

        for node in nodes:
            rest.append(node['node']['display_url'])
            # print(node['node']['display_url'])
        table['after'] = end_cursor
        print('加载..')
    print('加载完成')
    return rest


if __name__ == '__main__':

    res = requests.get(BASE_URL, headers=headers)
    html = etree.HTML(res.content.decode())
    h = html.xpath('//script[@type="text/javascript"]')[3].text.replace('window._sharedData = ', '').strip()[:-1]
    dic = json.loads(h, encoding='utf-8')

    print(dic)

    data = dic['entry_data']['ProfilePage'][0]['graphql']['user']["edge_owner_to_timeline_media"]
    nodes = data['edges']
    end_cursor = data['page_info']['end_cursor']
    has_next_page = data['page_info']['has_next_page']
    lee_id = nodes[0]['node']["owner"]["id"]  # '1161353543'

    src_list = []
    for node in nodes:
        src_list.append(node["node"]['display_url'])
        print(node["node"]['display_url'])
    print('加载')

    table = {
        'id':lee_id,
        'first':12,
        'after':end_cursor}
    rest = load_rest(table, has_next_page)
    src_list = src_list + rest
    print(len(src_list))

    #    with open('abc', 'w') as f:
    #    for s in src_list:
    #        f.write(s)
    #        f.write('\n')

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/58.0.3029.110 Safari/537.36", }
    for i in range(len(src_list)):
        url = src_list[i].strip()
        res = requests.get(url, headers=headers)
        with open('第' + str(i + 1) + '张.jpg', 'wb') as ff:
            ff.write(res.content)



# https://www.instagram.com/graphql/query/?query_hash=42323d64886122307be10013ad2dcc44&variables={"id"%3A"1161353543"%2C"first"%3A12%2C"after"%3A"AQBbheDFqxTXprhutCFJ7l55mriVItrm-8OtatcUQ2fHc-MSnjHSGIN7hj5zfO80fKQ5ouWdv9gTNK64SmIFo824MCBRJyz7TWJeV2z4l2pkpg"}
# https://www.instagram.com/graphql/query/?query_hash=42323d64886122307be10013ad2dcc44&variables={"id"%3A"1161353543"%2C"first"%3A12%2C"after"%3A"AQCbdb945wHVqrgu6pS33GN3ZPhHrEfQVNyXoe8zF7eVVQxbTbAZnZe1xZSxLARSJ236KqsKkVtr6EY-WEvluxA-yzFK-ya4a-HO1u3MjodNqg"}