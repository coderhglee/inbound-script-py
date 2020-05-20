import json
import time

import requests

# page = 0
size = 10
date = '20160511'
token = '65f63ce3-bgf7-4j5f-3772-ev98gjd089a3'


def getContent(page):
    print('get New Contents Page ==>' + str(page))
    time.sleep(1)
    body = requests.get(
        'https://news.chosun.com/svc/news/arc/contents.html?token=%s&date=%s&page=%s&size=%s' % (
            token, date, page, size))
    # print(body.text)
    json_body = json.loads(body.text)
    # print()
    page_body = json_body['page']
    for content in json_body['contents']:
        # print(content['relatedData']['id'])
        contid = content['relatedData']['id']
        # print(contid)
        # print(type(contid) is str)
        if type(contid) is str:
            time.sleep(1)
            related_body = requests.get(
                'https://news.chosun.com/svc/news/arc/related/content.html?contid=%s&token=%s&type=json' % (
                    contid, token))

            related_json_body = json.loads(related_body.text)
            for related_content in related_json_body['relatedContentList']['relatedContent']:
                print(related_content['id'])
                print(related_content['href'])

    if page < page_body['totalPages']:
        getContent(page=page + 1)
    # print(page)


getContent(page=0)
