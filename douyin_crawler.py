# -*- coding: utf-8 -*-
# @Author : lihuiwen
# @file : douyin_crawler
# @Email : huiwennear@163.com
# @Time : 2024/5/23 16:58

"""
    抖音评论爬取
"""
from utils.common_utils import CommonUtils
import copy
import json

import requests
from urllib.parse import urlparse, parse_qs

class DyComment:

    def __init__(self):

        self.common_utils = CommonUtils()
        self.comment_list_headers = {
            'sec-ch-ua':'"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
            'Accept':'application/json, text/plain, */*',
            'sec-ch-ua-mobile':'?0',
            'User-Agent':self.common_utils.user_agent,
            'sec-ch-ua-platform':'"Windows"',
            'Sec-Fetch-Site':'same-origin',
            'Sec-Fetch-Mode':'cors',
            'Sec-Fetch-Dest':'empty',
            'Accept-Language':'zh-CN,zh;q=0.9,en;q=0.8',
        }

    def get_comment_list(self, req_url):
        if ('modal_id' in req_url):
            aweme_id = parse_qs(urlparse(req_url).query).get('modal_id')[0]
        else:
            aweme_id = urlparse(req_url).path.split("/")[-1]
        referer_url = f"https://www.douyin.com/discover?modal_id={aweme_id}"
        ms_token = self.common_utils.get_ms_token()
        ttwid_str, webid = self.common_utils.get_ttwid_webid(referer_url)
        comment_lsit_req_url = f"https://www.douyin.com/aweme/v1/web/comment/list/?device_platform=webapp&aid=6383&channel=channel_pc_web&aweme_id={aweme_id}&cursor=0&count=20&item_type=0&insert_ids=&whale_cut_token=&cut_version=1&rcFT=&update_version_code=170400&pc_client_type=1&version_code=170400&version_name=17.4.0&cookie_enabled=true&screen_width=1920&screen_height=1080&browser_language=zh-CN&browser_platform=Win32&browser_name=Chrome&browser_version=123.0.0.0&browser_online=true&engine_name=Blink&engine_version=123.0.0.0&os_name=Windows&os_version=10&cpu_core_num=16&device_memory=8&platform=PC&downlink=10&effective_type=4g&round_trip_time=50&webid={webid}&verifyFp=verify_lwg2oa43_Ga6DRjOO_v2cd_4NL7_AHTp_qMKyKlDdoqra&fp=verify_lwg2oa43_Ga6DRjOO_v2cd_4NL7_AHTp_qMKyKlDdoqra&msToken={ms_token}"
        comment_list_headers1 = copy.deepcopy(self.comment_list_headers)
        comment_list_headers1['Referer'] = referer_url
        comment_list_headers1['Cookie'] = f'ttwid={ttwid_str};'
        abogus = self.common_utils.get_abogus(comment_lsit_req_url, self.common_utils.user_agent)
        url = comment_lsit_req_url + "&a_bogus=" + abogus
        response = requests.request("GET", url, headers=comment_list_headers1,verify=False, timeout=3)
        if (response.text):
            req_json = response.json()
            total = req_json.get('total')
            comments = req_json.get('comments')
            if (comments):
                for comment_index in range(len(comments)):
                    comment_item = comments[comment_index]
                    print(f"爬取成功：{comment_item.get('user').get('nickname')}：{comment_item.get('text')}")
            else:
                print(f"爬取结束：评论数={total}")
        else:
            print(f"爬取失败或没有评论")


if __name__ == '__main__':
    req_url = "https://www.douyin.com/discover?modal_id=7258913772092296485"
    dy_comment = DyComment()
    dy_comment.get_comment_list(req_url)