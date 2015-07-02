# -*- coding: utf-8 -*-

import io
import requests
import facebook
import json
# import csv
import unicodecsv as csv
import sys
import urllib3
import tablib

# disable ssl sucurity warning
urllib3.disable_warnings()

app_id = "134166843582122"
app_secret = "170da3cdee8456942fe1867e6c397fa0"

access_token_url = "https://graph.facebook.com/oauth/access_token?client_id=" + app_id + "&client_secret=" + app_secret + "&grant_type=client_credentials"

r = requests.get(access_token_url)

access_token = r.text.split('=')[1]

graph = facebook.GraphAPI(access_token=access_token, version='2.2')



# _fan_page_id = "283092135094363"
_fan_page_id = "652438848137404"
_feeds = graph.get_connections(id=_fan_page_id, connection_name='feed')
# previous_url = feeds['paging']['previous']


def get_comments(feeds, file_name):

    fieldnames = ['commenter_id', 'commenter_name', 'commenter_message', 'commenter_message_created_time', 'replier_id', 'replier_name', 'replier_message', 'replier_message_created_time']
    headers = ('commenter_id', 'commenter_name', 'commenter_message', 'commenter_message_created_time', 'replier_id', 'replier_name', 'replier_message', 'replier_message_created_time')

    try:
        # 針對每一則貼文
        for ele in feeds['data']:

            # break

            csv_file = open(ele['id'].split('_')[1] + '.xls', 'wb')
            # csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            # csv_writer.writeheader()

            data = []

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
                            r = requests.get(next_comments_url)
                            json_obj = json.loads(r.text)
                            comments = json_obj['data']

                            if 'next' in json_obj['paging']:
                                next_comments_url = json_obj['paging']['next']
                            else:
                                next_comments_url = ''

                    for comment in comments:
                        # print json.dumps(comment, ensure_ascii=False)

                        # 寫入 csv
                        commenter_name = json.dumps(comment['from']['name'], ensure_ascii=False)
                        commenter_id = json.dumps(comment['from']['id'], ensure_ascii=False)
                        commenter_message = json.dumps(comment['message'], ensure_ascii=False)
                        commenter_message_created_time = json.dumps(comment['created_time'], ensure_ascii=False)

                        # self.writer.writerow([unicode(s).encode("utf-8") for s in row])
                        print 'commenter_name: %s' % commenter_name
                        # csv_writer.writerow({'commenter_id': '', 'commenter_name': commenter_name, 'commenter_message': '', 'commenter_message_created_time': '', 'replier_id': '', 'replier_name': '', 'replier_message': '', 'replier_message_created_time': ''})
                        data.append(('', commenter_name, '', '', '', '', '', ''))


                        #check whether has replies or not
                        # 查看留言是否有回覆
                        r = graph.get_connections(id=comment['id'], connection_name="comments")

                        # try:
                        #     r = graph.get_connections(id=comment['id'], connection_name="comments")
                        # except:
                        #     get_comments_successfully = False
                        #     while not get_comments_successfully:
                        #         r = graph.get_connections(id=comment['id'], connection_name="comments")
                        #         if 'data' in r:
                        #             get_comments_successfully = True

                        print "Get replies data:"
                        print json.dumps(r, ensure_ascii=False)

                        next_replies_url = ''
                        if 'paging' in r:
                            if 'next' in r['paging']:
                                next_replies_url = r['paging']['next']

                        is_first_round_in_replies = True

                        while True:
                            if is_first_round_in_replies:
                                replies = r['data']
                                is_first_round_in_replies = False
                            else:
                                if next_replies_url != '':
                                    r = requests.get(next_replies_url)
                                    json_obj = json.loads(r.text)
                                    replies = json_obj['data']
                                    next_replies_url = ''
                                    if 'paging' in json_obj:
                                        if 'next' in json_obj['paging']:
                                            next_replies_url = json_obj['paging']['next']

                            for reply in replies:
                                # 名稱/id/內容/時間
                                replier_name = json.dumps(reply['from']['name'], ensure_ascii=False)
                                replier_id = json.dumps(reply['from']['id'], ensure_ascii=False)
                                replier_message = json.dumps(reply['message'], ensure_ascii=False)
                                replier_message_created_time = json.dumps(reply['created_time'], ensure_ascii=False)
                                # csv_writer.writerow({'replier_name': replier_name})
                                data.append(('', '', '', '', '', replier_name, '', ''))

                                print "=============== reply data ============="
                                print json.dumps(reply, ensure_ascii=False)
                                print "=============== reply data ============="

                            if next_replies_url == '':
                                break

                    # 如果沒有下一頁的 comment， 就 break while 迴圈
                    if next_comments_url == '':
                        break

                # print "Did not got comment!"
            # print json.dumps(ele, ensure_ascii=False)

            # print '--------------------------------------'
        # with io.open(file_name, 'w', encoding='UTF-8') as file:
            # file.write(json.dumps(feeds, ensure_ascii=False))

            data = tablib.Dataset(*data, headers=headers)
            csv_file.write(data.xls)
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
    except:
        data = tablib.Dataset(*data, headers=headers)
        csv_file.write(data.xls)
        csv_file.close()



get_comments(_feeds, "")


sys.exit(0)

