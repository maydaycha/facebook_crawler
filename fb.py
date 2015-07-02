# -*- coding: utf-8 -*-

import io
import requests
import facebook
import json
# import csv
import unicodecsv as csv
import sys
import urllib3

# disable ssl sucurity warning
urllib3.disable_warnings()

app_id = "134166843582122"
app_secret = "170da3cdee8456942fe1867e6c397fa0"

access_token_url = "https://graph.facebook.com/oauth/access_token?client_id=" + app_id + "&client_secret=" + app_secret + "&grant_type=client_credentials"

r = requests.get(access_token_url)

access_token = r.text.split('=')[1]

graph = facebook.GraphAPI(access_token=access_token, version='2.2')


# post = graph.get_object(id="283092135094363")
# print json.dumps(post, ensure_ascii=False)


_fan_page_id = "283092135094363"
# fan_page_id = "652438848137404"
_feeds = graph.get_connections(id=_fan_page_id, connection_name='feed')
# previous_url = feeds['paging']['previous']


def get_comments(feeds, file_name):

    fieldnames = ['commenter_id', 'commenter_name', 'commenter_message', 'commenter_message_created_time', 'replier_id', 'replier_name', 'replier_message', 'replier_message_created_time']

    # 針對每一則貼文
    for ele in feeds['data']:

        # break

        csv_file = open(ele['id'].split('_')[1] + '.csv', 'w')
        csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        csv_writer.writeheader()

        # 每一則貼文中的留言
        next_comments_url = ""

        is_first = True

        if 'comments' in ele:
            print "Got comment!"
            # need to get reply if exist
            print "@@@@@@@@@@@@@@@@"
            print json.dumps(ele, ensure_ascii=False)
            print "@@@@@@@@@@@@@@@@"
            if 'next' in ele['comments']['paging']:
                next_comments_url = ele['comments']['paging']['next']
            else:
                next_comments_url = ''

            print "next_comments_url: %s" % next_comments_url

            while True:
                if is_first:
                    comments = ele['comments']['data']
                    is_first = False
                else:
                    if next_comments_url != '':
                        r = requests.get(next_url)
                        json_obj = json.loads(r.text)
                        comments = json_obj['data']
                        next_comments_url = json_obj['paging']['next']

                for comment in comments:
                    # print json.dumps(comment, ensure_ascii=False)

                    # 寫入 csv
                    # commenter_name = unicode(json.dumps(comment['from']['name'], ensure_ascii=False)).encode('UTF-8')
                    commenter_name = json.dumps(comment['from']['name'], ensure_ascii=False)
                    # self.writer.writerow([unicode(s).encode("utf-8") for s in row])
                    print 'commenter_name: %s' % commenter_name
                    csv_writer.writerow({'commenter_id': '', 'commenter_name': commenter_name, 'commenter_message': '', 'commenter_message_created_time': '', 'replier_id': '', 'replier_name': '', 'replier_message': '', 'replier_message_created_time': ''})


                    #check whether has replies or not
                    # 查看留言是否有回覆
                    r = graph.get_connections(id=comment['id'], connection_name="comments")

                    for reply in r['data']:
                        # 名稱/id/內容/時間
                        replier_name = json.dumps(reply['from']['name'])
                        replier_id = json.dumps(reply['from']['id'])
                        replier_message = json.dumps(reply['message'])
                        replier_message_created_time = json.dumps(reply['created_time'])
                        csv_writer.writerow({'replier_name': replier_name})
                        # comment.update({"replies" : r})

                        print "=============== reply data ============="
                        print json.loads(json.dumps(reply, ensure_ascii=False), encoding="utf-8")
                        print "=============== reply data ============="

                if next_comments_url == '':
                    break
            # print "Did not got comment!"
        # print json.dumps(ele, ensure_ascii=False)

        # print '--------------------------------------'
    # with io.open(file_name, 'w', encoding='UTF-8') as file:
        # file.write(json.dumps(feeds, ensure_ascii=False))

        csv_file.close()

    next_url = ""
    if 'paging' in feeds:
        if 'next' in feeds['paging']:
            next_url = feeds['paging']['next']

    print "next url (feeds): %s" % next_url

    if next_url != '':
        r = requests.get(next_url)
        get_comments(json.loads(r.text), "")
    else:
        print "end!!!!"



get_comments(_feeds, "")



# r = requests.get(next_url)
# with io.open('next_result.json', 'w', encoding='UTF-8') as file:
    # file.write(json.dumps(json.loads(r.text), ensure_ascii=False))


# with io.open('result.json', 'w', encoding='UTF-8') as file:
    # file.write(json.dumps(feeds, ensure_ascii=False))

sys.exit(0)

# print feeds['data']

# with io.open('result.json', 'w', encoding='UTF-8') as file:
    # file.write(json.dumps(feeds, ensure_ascii=False))

# comment_id = '874027102667527_874374989299405'
# comment_id = '877895362280701_877916398945264'
# r = graph.get_connections(id=comment_id, connection_name="comments")
# print json.dumps(r, ensure_ascii=False)

# print s

def save_comment_and_replies(comment, csv_writer):
    pass

